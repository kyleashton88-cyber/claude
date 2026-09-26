#!/usr/bin/env python3
"""Deterministic helpers for the staff-standup-tracker skill.

Stdlib only. The skill (SKILL.md) drives the live Whop + Slack MCP tools; this
script owns the deterministic, side-effect-free logic so it is testable and
reproducible:

  list-schema  Print the Slack List column schema (JSON) to create the tracker.
  roster       Normalise a Whop `team-members_list` response into a roster.
  dm           Compose the daily-standup DM for one staff member.
  parse        Parse a staff member's free-form standup reply into buckets.
  plan         Turn a parsed reply into Slack List add/update operations.
  summary      Build the end-of-standup summary (markdown).
  overdue      Flag overdue / stale tracker rows.

Every command reads JSON from --file (or stdin) where noted and writes JSON or
markdown to stdout, so an agent can pipe MCP tool output straight through.

Not financial advice — operational tooling for internal team coordination only.
"""
import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta

# --- Slack List tracker schema -------------------------------------------------
# Column display names are the contract used across every command and in the
# SKILL. `Owner` is a Slack user column (holds a user id like U0ABC123).
STATUSES = ["To Do", "In Progress", "Blocked", "Done"]
PRIORITIES = ["High", "Medium", "Low"]

LIST_NAME = "Staff Standup Tracker"
LIST_DESCRIPTION = (
    "Daily standup tracker for the team. One row per task: who owns it, its "
    "status, when it's due, and any blocker. Updated from daily standup DMs."
)
COLUMNS = [
    {"name": "Task", "type": "text"},
    {"name": "Owner", "type": "user"},
    {"name": "Status", "type": "select", "options": STATUSES},
    {"name": "Priority", "type": "select", "options": PRIORITIES},
    {"name": "Due Date", "type": "date"},
    {"name": "Blocker", "type": "text"},
    {"name": "Last Update", "type": "date"},
    {"name": "Notes", "type": "rich_text"},
]


def _today(args):
    return args.today or date.today().isoformat()


def _load(args):
    """Load JSON from --file or stdin."""
    if getattr(args, "file", None):
        with open(args.file, "r", encoding="utf-8") as fh:
            return json.load(fh)
    data = sys.stdin.read()
    if not data.strip():
        return {}
    return json.loads(data)


def _first_name(name):
    return (name or "there").strip().split()[0] if (name or "").strip() else "there"


# --- text matching -------------------------------------------------------------
_WORD = re.compile(r"[a-z0-9]+")


def _norm(text):
    return " ".join(_WORD.findall((text or "").lower()))


def _tokens(text):
    return set(_WORD.findall((text or "").lower()))


def match_task(a, b):
    """Fuzzy title match: exact-normalised, substring, or high token overlap."""
    na, nb = _norm(a), _norm(b)
    if not na or not nb:
        return False
    if na == nb or na in nb or nb in na:
        return True
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return False
    overlap = len(ta & tb) / len(ta | tb)
    return overlap >= 0.6


# --- roster --------------------------------------------------------------------
def cmd_roster(args):
    """Normalise a Whop team-members_list response into roster entries.

    Accepts the raw tool result (an object with `data`/`members`/`nodes`, or a
    bare list). Emits one entry per member with the fields the standup flow
    needs. `slack_user_id` is left null for the agent to fill via
    slack_search_users (match on email).
    """
    payload = _load(args)
    members = payload
    for key in ("data", "members", "nodes", "team_members"):
        if isinstance(payload, dict) and key in payload:
            members = payload[key]
            break
    if isinstance(members, dict):
        members = members.get("nodes", members.get("data", []))

    roster = []
    for m in members or []:
        if not isinstance(m, dict):
            continue
        user = m.get("user") or {}
        name = (
            m.get("name")
            or user.get("name")
            or user.get("username")
            or m.get("username")
            or ""
        )
        roster.append({
            "whop_member_id": m.get("id"),
            "name": name,
            "email": m.get("email") or user.get("email"),
            "role": m.get("role"),
            "status": m.get("status"),
            "slack_user_id": None,
        })
    if args.joined_only:
        roster = [r for r in roster if r.get("status") in (None, "joined")]
    print(json.dumps(roster, indent=2))


# --- daily standup DM ----------------------------------------------------------
def _open_tasks_for(records, owner_id):
    out = []
    for r in records:
        if r.get("Owner") != owner_id:
            continue
        if r.get("Status") == "Done":
            continue
        out.append(r)
    order = {s: i for i, s in enumerate(["Blocked", "In Progress", "To Do"])}
    out.sort(key=lambda r: (order.get(r.get("Status"), 9), r.get("Due Date") or "9999"))
    return out


def compose_dm(name, tasks, today):
    first = _first_name(name)
    lines = [f"Good morning, {first} :sunny: — quick daily standup."]
    if tasks:
        lines.append("")
        lines.append("*Your open tasks:*")
        for t in tasks:
            bits = [f"• *{t.get('Task', '(untitled)')}*", f"— {t.get('Status', 'To Do')}"]
            if t.get("Due Date"):
                overdue = t["Due Date"] < today and t.get("Status") != "Done"
                bits.append(f"(due {t['Due Date']}{' — *overdue*' if overdue else ''})")
            if t.get("Status") == "Blocked" and t.get("Blocker"):
                bits.append(f"— blocked: {t['Blocker']}")
            lines.append(" ".join(bits))
    else:
        lines.append("")
        lines.append("_No open tasks on the tracker for you right now._")
    lines += [
        "",
        "Reply in this format so I can update the tracker:",
        "> *Done:* things you finished",
        "> *Today:* what you're working on",
        "> *Blocked:* anything in your way (or 'none')",
    ]
    return "\n".join(lines)


def cmd_dm(args):
    data = _load(args)
    records = data.get("records", []) if isinstance(data, dict) else []
    today = _today(args)
    if args.owner:
        tasks = _open_tasks_for(records, args.owner)
        print(compose_dm(args.name or "", tasks, today))
        return
    # Batch: one DM per owner present in the roster.
    roster = data.get("roster", []) if isinstance(data, dict) else []
    out = []
    for person in roster:
        uid = person.get("slack_user_id")
        if not uid:
            continue
        tasks = _open_tasks_for(records, uid)
        out.append({
            "slack_user_id": uid,
            "name": person.get("name"),
            "message": compose_dm(person.get("name", ""), tasks, today),
        })
    print(json.dumps(out, indent=2))


# --- reply parsing -------------------------------------------------------------
_HEADERS = {
    "done": ["done", "completed", "finished", "shipped", "yesterday"],
    "today": ["today", "working on", "in progress", "doing", "plan", "will"],
    "blocked": ["blocked", "blocker", "blockers", "stuck", "waiting on", "help"],
}
_NONE = {"none", "n/a", "na", "nothing", "no", "nope", "-", "none."}


def _bucket_for(line):
    low = line.lower().strip()
    head = re.split(r"[:\-–]", low, 1)[0].strip()
    for bucket, kws in _HEADERS.items():
        if any(head == kw or head.startswith(kw) for kw in kws):
            return bucket
    return None


def _clean_item(text):
    return re.sub(r"^[\s\-\*•·>0-9\.\)]+", "", text).strip()


def parse_reply(text):
    """Parse a free-form standup reply into done/today/blocked item lists."""
    result = {"done": [], "today": [], "blocked": []}
    current = "today"  # default bucket if the writer omits headers
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        bucket = _bucket_for(line)
        if bucket:
            current = bucket
            after = re.split(r"[:\-–]", line, 1)
            rest = _clean_item(after[1]) if len(after) > 1 else ""
            if rest and rest.lower() not in _NONE:
                result[bucket].append(rest)
            continue
        item = _clean_item(line)
        if item and item.lower() not in _NONE:
            result[current].append(item)
    return result


def cmd_parse(args):
    if getattr(args, "text", None) is not None:
        text = args.text
    else:
        text = sys.stdin.read()
    print(json.dumps(parse_reply(text), indent=2))


# --- plan: parsed reply -> Slack List operations -------------------------------
def plan_updates(records, owner_id, parsed, today):
    """Compute add/update operations for one owner's standup reply.

    Returns {"updates": [...], "adds": [...]}, where each update is
    {record_id, updated_columns} and each add is {columns}. Matching against
    existing rows is fuzzy on the task title; unmatched items become new rows.
    """
    owned = [r for r in records if r.get("Owner") == owner_id]
    used = set()
    updates, adds = [], []

    def find(title):
        for r in owned:
            rid = r.get("Record ID")
            if rid in used:
                continue
            if match_task(title, r.get("Task", "")):
                used.add(rid)
                return r
        return None

    for title in parsed.get("done", []):
        row = find(title)
        if row:
            updates.append({
                "record_id": row.get("Record ID"),
                "updated_columns": {"Status": "Done", "Last Update": today},
            })
        else:
            adds.append({"columns": {
                "Task": title, "Owner": owner_id, "Status": "Done",
                "Last Update": today,
            }})

    for title in parsed.get("today", []):
        row = find(title)
        if row:
            updates.append({
                "record_id": row.get("Record ID"),
                "updated_columns": {"Status": "In Progress", "Last Update": today},
            })
        else:
            adds.append({"columns": {
                "Task": title, "Owner": owner_id, "Status": "In Progress",
                "Priority": "Medium", "Last Update": today,
            }})

    for title in parsed.get("blocked", []):
        row = find(title)
        if row:
            updates.append({
                "record_id": row.get("Record ID"),
                "updated_columns": {
                    "Status": "Blocked", "Blocker": title, "Last Update": today,
                },
            })
        else:
            adds.append({"columns": {
                "Task": title, "Owner": owner_id, "Status": "Blocked",
                "Blocker": title, "Priority": "High", "Last Update": today,
            }})
    return {"updates": updates, "adds": adds}


def cmd_plan(args):
    data = _load(args)
    records = data.get("records", []) if isinstance(data, dict) else []
    parsed = data.get("parsed")
    if parsed is None and isinstance(data, dict):
        parsed = parse_reply(data.get("reply", ""))
    owner = args.owner or (data.get("owner") if isinstance(data, dict) else None)
    if not owner:
        sys.exit("plan: --owner (or an 'owner' field) is required")
    print(json.dumps(plan_updates(records, owner, parsed or {}, _today(args)), indent=2))


# --- overdue / stale -----------------------------------------------------------
def find_overdue(records, today, stale_days):
    stale_before = (date.fromisoformat(today) - timedelta(days=stale_days)).isoformat()
    overdue, stale = [], []
    for r in records:
        if r.get("Status") == "Done":
            continue
        due = r.get("Due Date")
        if due and due < today:
            overdue.append(r)
        last = r.get("Last Update")
        if last and last < stale_before:
            stale.append(r)
    return {"overdue": overdue, "stale": stale}


def cmd_overdue(args):
    data = _load(args)
    records = data.get("records", []) if isinstance(data, dict) else data
    print(json.dumps(find_overdue(records, _today(args), args.stale_days), indent=2))


# --- summary -------------------------------------------------------------------
def build_summary(records, today, stale_days=3):
    by_owner = {}
    for r in records:
        by_owner.setdefault(r.get("Owner") or "(unassigned)", []).append(r)

    flags = find_overdue(records, today, stale_days)
    overdue_ids = {r.get("Record ID") for r in flags["overdue"]}

    lines = [f"*Daily standup summary — {today}*", ""]
    totals = {s: 0 for s in STATUSES}
    for owner, rows in sorted(by_owner.items()):
        counts = {s: 0 for s in STATUSES}
        for r in rows:
            counts[r.get("Status", "To Do")] = counts.get(r.get("Status", "To Do"), 0) + 1
            totals[r.get("Status", "To Do")] = totals.get(r.get("Status", "To Do"), 0) + 1
        mention = f"<@{owner}>" if owner.startswith("U") else owner
        seg = (
            f"{counts['Done']} done · {counts['In Progress']} in progress · "
            f"{counts['Blocked']} blocked · {counts['To Do']} to do"
        )
        lines.append(f"• {mention}: {seg}")
        for r in rows:
            if r.get("Status") == "Blocked":
                lines.append(f"    :no_entry: blocked — *{r.get('Task')}*: {r.get('Blocker', '')}")
            elif r.get("Record ID") in overdue_ids:
                lines.append(f"    :alarm_clock: overdue — *{r.get('Task')}* (due {r.get('Due Date')})")

    lines += [
        "",
        (
            f"*Team totals:* {totals['Done']} done · {totals['In Progress']} in progress · "
            f"{totals['Blocked']} blocked · {totals['To Do']} to do · "
            f"{len(flags['overdue'])} overdue · {len(flags['stale'])} stale (>{stale_days}d)"
        ),
    ]
    return "\n".join(lines)


def cmd_summary(args):
    data = _load(args)
    records = data.get("records", []) if isinstance(data, dict) else data
    print(build_summary(records, _today(args), args.stale_days))


def cmd_list_schema(args):
    print(json.dumps({
        "name": LIST_NAME,
        "description": LIST_DESCRIPTION,
        "columns": COLUMNS,
    }, indent=2))


def build_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list-schema", help="print the Slack List schema JSON")
    s.set_defaults(func=cmd_list_schema)

    s = sub.add_parser("roster", help="normalise a Whop team-members response")
    s.add_argument("--file")
    s.add_argument("--joined-only", action="store_true", help="drop pending invites")
    s.set_defaults(func=cmd_roster)

    s = sub.add_parser("dm", help="compose daily standup DM(s)")
    s.add_argument("--file")
    s.add_argument("--owner", help="Slack user id for a single DM")
    s.add_argument("--name", help="staff name for a single DM")
    s.add_argument("--today")
    s.set_defaults(func=cmd_dm)

    s = sub.add_parser("parse", help="parse a free-form standup reply")
    s.add_argument("--text")
    s.set_defaults(func=cmd_parse)

    s = sub.add_parser("plan", help="parsed reply -> Slack List operations")
    s.add_argument("--file")
    s.add_argument("--owner")
    s.add_argument("--today")
    s.set_defaults(func=cmd_plan)

    s = sub.add_parser("overdue", help="flag overdue / stale rows")
    s.add_argument("--file")
    s.add_argument("--today")
    s.add_argument("--stale-days", type=int, default=3)
    s.set_defaults(func=cmd_overdue)

    s = sub.add_parser("summary", help="build the standup summary markdown")
    s.add_argument("--file")
    s.add_argument("--today")
    s.add_argument("--stale-days", type=int, default=3)
    s.set_defaults(func=cmd_summary)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
