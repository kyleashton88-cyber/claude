# Kyle → Stuart (Slack message text)

In-place rename of the owner name **Kyle** / **Kyle's** to **Stuart** / **Stuart's** in Audience Asset Co Slack. The display name Stewart Crown stays. Account paths `kyle-ashton` stay. Nothing is deleted and no correction message is posted.

## What is in this folder

| File | Role |
| --- | --- |
| `inventory.json` | 55 search rows (36 editable by `U0BNNB7C0V6`, 5 account-path rows left alone, the rest not editable with Stewart's user token) |
| `apply_kyle_to_stuart.py` | Dry-run changelog, or `chat.update` when a user token is present |
| `CHANGELOG.md` | Every intended edit: channel, ts, permalink, before snippet → after snippet |
| `test_replace.py` | Replacer and inventory-count checks |

## Blocker on this run

No `SLACK_USER_TOKEN` (and no `SLACK_XOX_TOKEN` or `SLACK_TOKEN`) was available in the environment. `chat.update` was not called.

## Apply when a token exists

The token must be a **user** token (`xoxp-`) for Stewart Crown (`U0BNNB7C0V6`) with `chat:write` plus history scopes for the channels and DMs in the inventory (`channels:history`, `groups:history`, `im:history`, `mpim:history`). A bot token cannot edit those messages.

```bash
export SLACK_USER_TOKEN=xoxp-...
python3 ops/slack-kyle-to-stuart/apply_kyle_to_stuart.py --apply
```

Dry-run (no network writes):

```bash
python3 ops/slack-kyle-to-stuart/apply_kyle_to_stuart.py
python3 ops/slack-kyle-to-stuart/test_replace.py
```

The apply path fetches each live message first and rewrites only the whole word Kyle, so a changelog snippet is never written back over the full body.

Messages authored by bots or other people are listed in the changelog and skipped. Slack only lets the author edit a message. Four PDFs that contain Kyle are listed and are not part of `chat.update`.
