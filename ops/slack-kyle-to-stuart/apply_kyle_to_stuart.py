#!/usr/bin/env python3
"""In-place Kyle → Stuart edits for Audience Asset Co Slack.

Spelling for this job is Stuart / Stuart's. Never rewrite Stewart, and never
rewrite account paths such as kyle-ashton.

Default mode is dry-run: it writes CHANGELOG.md and does not call Slack.
chat.update runs only with --apply and a user token (xoxp-) for U0BNNB7C0V6.
The tool never deletes messages and never posts a correction copy.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

OWNER_ID = "U0BNNB7C0V6"
KYLE_WORD = re.compile(r"\bKyle\b")
STEWART_WORD = re.compile(r"\bStewart\b")
TOKEN_ENVS = ("SLACK_USER_TOKEN", "SLACK_XOX_TOKEN", "SLACK_TOKEN")

PDFS = [
    {
        "file": "VA_DM_Setting_Closing_SOP.pdf",
        "id": "F0CA4FJ0TBM",
        "preview": "Prepared for: Kyle Ashton… Waiting on Kyle… Pending Kyle's final decision",
    },
    {
        "file": "Lead_Flow_and_Typeforms_v2.pdf",
        "id": "F0CAALJ6G0J",
        "preview": "Prepared for Kyle Ashton… Pending Kyle…",
    },
    {
        "file": "How to interact with AI and Slack",
        "id": "F0CAB712WUR",
        "preview": "What they won't do without Kyle… until Kyle says go",
    },
    {
        "file": "Stewart-Reel-Hooks-CTAs-DNA.pdf",
        "id": "F0CCD00JVN2",
        "preview": "DRAFT for Kyle to review. Not for publishing until Kyle…",
    },
]


def replace_kyle(text: str) -> str:
    """Replace the owner name Kyle / Kyle's / Kyle’s. Leave Stewart and kyle-ashton."""
    return KYLE_WORD.sub("Stuart", text)


def load_inventory(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    if not isinstance(data, list):
        raise SystemExit(f"{path} is not a JSON list")
    return data


def classify(rows: list[dict]) -> dict[str, list[dict]]:
    editable, blocked, leave = [], [], []
    for row in rows:
        kind = row.get("hit_kind")
        if kind == "account_path" or not row.get("editable_by_us"):
            if kind == "account_path":
                leave.append(row)
            else:
                blocked.append(row)
        elif kind == "prose" and row.get("author_id") == OWNER_ID:
            editable.append(row)
        else:
            blocked.append(row)
    return {"editable": editable, "blocked": blocked, "leave": leave}


def snippet_pair(row: dict) -> tuple[str, str]:
    before = row.get("original_snippet") or ""
    return before, replace_kyle(before)


def find_token() -> str | None:
    for name in TOKEN_ENVS:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return None


def slack_api(token: str, method: str, params: dict) -> dict:
    body = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        f"https://slack.com/api/{method}",
        data=body,
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:500]
        raise SystemExit(f"Slack HTTP {exc.code} on {method}: {detail}") from exc
    if not payload.get("ok"):
        raise SystemExit(f"Slack {method} failed: {payload.get('error')}")
    return payload


def thread_ts_from_permalink(permalink: str, message_ts: str) -> str | None:
    query = urllib.parse.urlparse(permalink).query
    values = urllib.parse.parse_qs(query)
    found = (values.get("thread_ts") or [None])[0]
    if found and found != message_ts:
        return found
    return None


def replace_strings(node):
    """Replace Kyle inside Slack text and block trees. Returns (new, changed)."""
    if isinstance(node, str):
        updated = replace_kyle(node)
        return updated, updated != node
    if isinstance(node, list):
        changed = False
        out = []
        for item in node:
            new, did = replace_strings(item)
            changed = changed or did
            out.append(new)
        return out, changed
    if isinstance(node, dict):
        changed = False
        out = {}
        for key, value in node.items():
            if key in {"text", "fallback", "title", "name", "verbatim"} or isinstance(
                value, (dict, list, str)
            ):
                new, did = replace_strings(value)
                # Only rewrite human-readable fields and nested structures.
                # Leave ids, timestamps, and user ids untouched by walking
                # strings everywhere, which is safe: user ids do not contain Kyle.
                changed = changed or did
                out[key] = new
            else:
                out[key] = value
        return out, changed
    return node, False


def fetch_message(token: str, row: dict) -> dict:
    channel = row["channel_id"]
    ts = row["ts"]
    parent = thread_ts_from_permalink(row.get("permalink") or "", ts)
    if parent:
        payload = slack_api(
            token,
            "conversations.replies",
            {"channel": channel, "ts": parent, "limit": "200"},
        )
        for message in payload.get("messages") or []:
            if message.get("ts") == ts:
                return message
        raise SystemExit(f"Reply {ts} not found in thread {parent}")
    payload = slack_api(
        token,
        "conversations.history",
        {
            "channel": channel,
            "latest": ts,
            "oldest": ts,
            "inclusive": "true",
            "limit": "1",
        },
    )
    messages = payload.get("messages") or []
    if messages and messages[0].get("ts") == ts:
        return messages[0]
    payload = slack_api(
        token,
        "conversations.replies",
        {"channel": channel, "ts": ts, "limit": "1"},
    )
    for message in payload.get("messages") or []:
        if message.get("ts") == ts:
            return message
    raise SystemExit(f"Message {channel} {ts} was not returned by Slack")


def apply_one(token: str, row: dict) -> dict:
    message = fetch_message(token, row)
    if message.get("user") != OWNER_ID:
        return {
            "ts": row["ts"],
            "status": "skipped",
            "reason": f"author is {message.get('user')}, not {OWNER_ID}",
        }
    new_text, text_changed = replace_strings(message.get("text") or "")
    new_blocks, blocks_changed = replace_strings(message.get("blocks") or [])
    if not text_changed and not blocks_changed:
        return {"ts": row["ts"], "status": "unchanged", "reason": "no Kyle word in live text"}
    params = {"channel": row["channel_id"], "ts": row["ts"], "text": new_text}
    if message.get("blocks"):
        params["blocks"] = json.dumps(new_blocks)
    slack_api(token, "chat.update", params)
    return {"ts": row["ts"], "status": "updated"}


def render_changelog(groups: dict[str, list[dict]], applied: bool, blocker: str) -> str:
    lines = [
        "# CHANGELOG — Kyle to Stuart",
        "",
        "In-place message text only. Nothing in this run was deleted, and no correction copy was posted.",
        "Replacement spelling is **Stuart** / **Stuart's**. The display name Stewart Crown is not part of the replacement.",
        "",
        f"- Inventory rows: {sum(len(v) for v in groups.values())}",
        f"- Intended edits (author {OWNER_ID}): {len(groups['editable'])}",
        f"- Not editable with that user token: {len(groups['blocked'])}",
        f"- Left unchanged (kyle-ashton account paths): {len(groups['leave'])}",
        f"- Applied via chat.update: {'yes' if applied else 'no'}",
        "",
    ]
    if blocker:
        lines += ["## Blocker", "", blocker, ""]
    lines += ["## Intended edits", ""]
    for index, row in enumerate(groups["editable"], start=1):
        before, after = snippet_pair(row)
        lines += [
            f"### {index}. {row['channel_name']}",
            "",
            f"- Channel id: `{row['channel_id']}`",
            f"- ts: `{row['ts']}`",
            f"- Author: {row.get('author_name')} (`{row.get('author_id')}`)",
            f"- Permalink: {row['permalink']}",
            f"- Before: {before}",
            f"- After: {after}",
            "",
        ]
    lines += [
        "## Not edited — Slack only allows the author to change a message",
        "",
        "These rows name Kyle, but the author is not U0BNNB7C0V6. A user token for Stewart cannot chat.update them. No delete and no repost.",
        "",
    ]
    for row in groups["blocked"]:
        before, after = snippet_pair(row)
        lines += [
            f"- {row['channel_name']} `{row['channel_id']}` ts `{row['ts']}` author {row.get('author_name')} (`{row.get('author_id')}`) kind `{row.get('hit_kind')}`. [permalink]({row['permalink']})",
            f"  - Before: {before}",
            f"  - Would become: {after}",
            "",
        ]
    lines += [
        "## Left unchanged — account paths",
        "",
        "Cursor DM hits are the Origin username `kyle-ashton` inside repo URLs. They are not the owner name in prose. Left as-is.",
        "",
    ]
    for row in groups["leave"]:
        lines.append(
            f"- {row['channel_name']} ts `{row['ts']}` [permalink]({row['permalink']}) — {row['original_snippet']}"
        )
    lines += [
        "",
        "## PDFs with Kyle in the file body",
        "",
        "These are files, not message bodies. chat.update does not change PDF bytes. Noted only.",
        "",
    ]
    for pdf in PDFS:
        lines.append(f"- `{pdf['file']}` (`{pdf['id']}`) — {pdf['preview']}")
    lines += [
        "",
        "## Skipped false positive",
        "",
        "- #video-creation `C0C3PAFRGNT` ts `1790433847.163959` — search hit on a Loom/Descript post whose message body has no whole-word Kyle. Not an edit.",
        "",
        "## How to apply later",
        "",
        "```bash",
        "export SLACK_USER_TOKEN=xoxp-...   # user token for U0BNNB7C0V6 with chat:write, channels:history, groups:history, im:history, mpim:history",
        "python3 ops/slack-kyle-to-stuart/apply_kyle_to_stuart.py --apply",
        "```",
        "",
        "The apply path loads each live message, rewrites only the whole word Kyle, and calls chat.update. It refuses a bot token and refuses a token whose auth.test user is not U0BNNB7C0V6.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=here / "inventory.json")
    parser.add_argument("--changelog", type=Path, default=here / "CHANGELOG.md")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Call chat.update. Requires SLACK_USER_TOKEN (xoxp-) for U0BNNB7C0V6.",
    )
    args = parser.parse_args(argv)
    groups = classify(load_inventory(args.inventory))
    token = find_token()
    applied = False
    blocker = ""
    if not args.apply:
        if token:
            blocker = (
                "A token is present in the environment, but this run did not pass --apply, so nothing was edited."
            )
        else:
            blocker = (
                "No Slack user token in SLACK_USER_TOKEN, SLACK_XOX_TOKEN, or SLACK_TOKEN. "
                "chat.update was not called. The 36 Stewart-authored messages are listed below as intended edits."
            )
    else:
        if not token:
            args.changelog.write_text(render_changelog(groups, False, "Apply requested but no user token is set."))
            print("BLOCKER: no Slack user token. CHANGELOG written. Nothing edited.", file=sys.stderr)
            return 2
        if not token.startswith("xoxp-"):
            print("BLOCKER: token is not a user token (xoxp-). Refusing to edit.", file=sys.stderr)
            return 2
        auth = slack_api(token, "auth.test", {})
        if auth.get("user_id") != OWNER_ID:
            print(
                f"BLOCKER: token user is {auth.get('user_id')}, expected {OWNER_ID}. Nothing edited.",
                file=sys.stderr,
            )
            return 2
        results = []
        for row in groups["editable"]:
            results.append(apply_one(token, row))
            print(results[-1]["status"], row["channel_id"], row["ts"])
        applied = any(item["status"] == "updated" for item in results)
        failed = [item for item in results if item["status"] not in {"updated", "unchanged"}]
        blocker = "" if not failed else f"Some rows were skipped: {failed}"
    args.changelog.write_text(render_changelog(groups, applied, blocker))
    print(
        f"editable={len(groups['editable'])} blocked={len(groups['blocked'])} "
        f"left={len(groups['leave'])} applied={applied}"
    )
    print(f"wrote {args.changelog}")
    if blocker:
        print("BLOCKER:", blocker)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
