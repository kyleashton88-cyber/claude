---
name: staff-standup-tracker
description: Monitor staff, DM each team member a daily standup, and keep a Slack List to-do/tracker in sync for the whole team. Pulls the roster from Whop team members, messages staff in Slack, records tasks/blockers, and posts a daily summary. Use when the user asks to run standup, check in with staff, chase blockers, build or update a team task tracker, or "see what everyone is working on".
---

# Staff Standup Tracker

Run a daily standup for the team: pull the staff roster from **Whop**, DM each
person in **Slack**, capture what they finished / are doing / are blocked on into
a **Slack List** tracker, and post a summary. Any agent can run this by following
the steps below and using `scripts/standup.py` for the deterministic work
(message text, tracker operations, summaries, overdue detection).

> Operational tooling for internal team coordination. Not financial advice.

## Tools this skill drives

- **Whop MCP** — `team-members_list` (roster). Needs `account_id` (`biz_…`); find
  it with `accounts_list` if you don't have it. `email` needs the
  `company:authorized_user:email:read` scope; it's `null` otherwise.
- **Slack MCP** — `slack_search_users` (email → Slack `user_id`),
  `slack_create_list` / `slack_read_list` / `slack_add_list_record` /
  `slack_update_list_record` (the tracker), `slack_send_message` (DM a user by
  passing their `user_id` as `channel_id`; post the summary to a channel),
  `slack_read_thread` (read replies).

## Data model (Slack List columns)

`Task` (text, primary) · `Owner` (user) · `Status` (select: To Do / In Progress /
Blocked / Done) · `Priority` (select: High / Medium / Low) · `Due Date` (date) ·
`Blocker` (text) · `Last Update` (date) · `Notes` (rich_text).

`scripts/standup.py list-schema` prints this exact schema as JSON for
`slack_create_list`.

## The helper script

Stdlib Python, no side effects. Every command reads JSON from `--file`/stdin and
writes JSON or markdown, so you can pipe MCP output through it.

| Command | In | Out |
|---|---|---|
| `list-schema` | — | Slack List `name`/`description`/`columns` for `slack_create_list` |
| `roster [--joined-only]` | `team-members_list` result | normalised roster (`slack_user_id` null, you fill it) |
| `dm [--owner U --name N]` | `{roster, records}` (or single owner) | DM text per person, ready for `slack_send_message` |
| `parse [--text ...]` | staff reply text | `{done, today, blocked}` buckets |
| `plan --owner U` | `{records, reply|parsed}` | `{updates:[{record_id,updated_columns}], adds:[{columns}]}` |
| `summary` | `{records}` | markdown summary for a channel |
| `overdue [--stale-days N]` | `{records}` | `{overdue, stale}` rows |

Pass `--today YYYY-MM-DD` to any command for deterministic dates (tests/dry-runs).

## Setup (once)

1. Resolve the Whop `account_id` (`accounts_list` if needed).
2. `team-members_list(account_id=…, status="joined")` → pipe into
   `standup.py roster --joined-only`.
3. For each roster entry, `slack_search_users` by email → set `slack_user_id`.
   Skip anyone with no matching Slack user and report them.
4. Create the tracker: `slack_create_list` with the output of
   `standup.py list-schema`. Save the returned `list_id`.
5. Seed any known in-flight work with `slack_add_list_record`.

## Daily run

1. Read current rows: `slack_read_list(list_id)` → build `{roster, records}`
   (each record must include its `Record ID`, `Owner` = Slack `user_id`, `Task`,
   `Status`, `Due Date`, `Last Update`).
2. `standup.py dm` on that object → for each person, `slack_send_message`
   (`channel_id` = their `slack_user_id`). Keep the returned `ts` per person.
3. When a member replies (`slack_read_thread` on their DM), run
   `standup.py parse` then `standup.py plan --owner <user_id>` with
   `{records, reply}`. Apply the result: `slack_update_list_record` for each
   `updates` entry, `slack_add_list_record` for each `adds` entry.
4. After everyone replies (or a cutoff), `standup.py summary` on the refreshed
   records → post to the team channel with `slack_send_message`. DM overdue
   owners from `standup.py overdue` if you want targeted nudges.

## Guardrails

- **Never DM real staff or create/modify Slack Lists without the user's go-ahead**
  the first time you run in a workspace. Show the composed DMs and the tracker
  schema for a one-word confirm, unless the user says "run without asking".
- Match staff to Slack users by **email**; never guess a `user_id`. Report
  unmatched people instead of messaging the wrong person.
- One row per task; update existing rows rather than duplicating. `plan` matches
  fuzzily on the title and only ever touches the given owner's rows.
- Keep DMs short and specific. No performance or financial claims.
- Respect Slack Connect limits (can't DM external users) and Whop scope limits
  (email may be `null`).

## Verify / dry-run

`cd scripts && python3 -m unittest -v` runs the logic tests. For an end-to-end
dry run without touching Slack, feed `references/sample_tracker.json`:

```
python3 scripts/standup.py dm --file references/sample_tracker.json --today 2026-09-26
python3 scripts/standup.py summary --file references/sample_tracker.json --today 2026-09-26
echo '{"records": <rows>, "owner":"U1", "reply":"Done: ship onboarding email\nToday: draft module 3 script"}' \
  | python3 scripts/standup.py plan --owner U1 --today 2026-09-26
```
