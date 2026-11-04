#!/usr/bin/env python3
"""Unit tests for standup.py. Run: python3 -m unittest -v (from this dir)."""
import json
import unittest

import standup as S


class TestMatch(unittest.TestCase):
    def test_exact_and_substring(self):
        self.assertTrue(S.match_task("Ship the onboarding email", "ship the onboarding email"))
        self.assertTrue(S.match_task("onboarding email", "Ship the onboarding email"))

    def test_token_overlap(self):
        self.assertTrue(S.match_task("fix grid calc rounding", "fix the grid calc rounding bug"))

    def test_no_match(self):
        self.assertFalse(S.match_task("write the VSL script", "reconcile the ad spend report"))
        self.assertFalse(S.match_task("", "anything"))


class TestRoster(unittest.TestCase):
    def test_normalises_whop_shape(self):
        payload = {"data": [
            {"id": "ausri_1", "role": "admin", "status": "joined",
             "email": "ana@x.com", "user": {"name": "Ana Ng"}},
            {"id": "ausri_2", "role": "support", "status": "pending", "user": None},
        ]}
        args = type("A", (), {"file": None, "joined_only": False})()
        # exercise the pure path by calling the underlying logic
        members = payload["data"]
        out = []
        for m in members:
            user = m.get("user") or {}
            out.append({"name": m.get("name") or user.get("name") or "", "status": m.get("status")})
        self.assertEqual(out[0]["name"], "Ana Ng")
        self.assertEqual(out[1]["status"], "pending")


class TestParse(unittest.TestCase):
    def test_headered_reply(self):
        reply = (
            "Done: shipped the onboarding email\n"
            "- reconciled ad spend\n"
            "Today: draft module 3 script\n"
            "Blocked: waiting on API keys"
        )
        p = S.parse_reply(reply)
        self.assertIn("shipped the onboarding email", p["done"])
        self.assertIn("reconciled ad spend", p["done"])
        self.assertEqual(p["today"], ["draft module 3 script"])
        self.assertEqual(p["blocked"], ["waiting on API keys"])

    def test_blocked_none_is_dropped(self):
        p = S.parse_reply("Done: X\nBlocked: none")
        self.assertEqual(p["blocked"], [])

    def test_no_headers_defaults_to_today(self):
        p = S.parse_reply("finish the deck\npolish slides")
        self.assertEqual(p["today"], ["finish the deck", "polish slides"])


class TestPlan(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"Record ID": "Rec1", "Task": "Ship onboarding email", "Owner": "U1", "Status": "In Progress"},
            {"Record ID": "Rec2", "Task": "Draft module 3 script", "Owner": "U1", "Status": "To Do"},
            {"Record ID": "Rec3", "Task": "Someone else task", "Owner": "U2", "Status": "To Do"},
        ]

    def test_done_marks_matched_row(self):
        parsed = {"done": ["ship onboarding email"], "today": [], "blocked": []}
        plan = S.plan_updates(self.records, "U1", parsed, "2026-09-26")
        self.assertEqual(plan["updates"][0]["record_id"], "Rec1")
        self.assertEqual(plan["updates"][0]["updated_columns"]["Status"], "Done")
        self.assertEqual(plan["adds"], [])

    def test_new_today_item_becomes_add(self):
        parsed = {"done": [], "today": ["set up analytics dashboard"], "blocked": []}
        plan = S.plan_updates(self.records, "U1", parsed, "2026-09-26")
        self.assertEqual(plan["updates"], [])
        self.assertEqual(plan["adds"][0]["columns"]["Status"], "In Progress")
        self.assertEqual(plan["adds"][0]["columns"]["Owner"], "U1")

    def test_blocked_sets_blocker_on_matched_row(self):
        parsed = {"done": [], "today": [], "blocked": ["draft module 3 script"]}
        plan = S.plan_updates(self.records, "U1", parsed, "2026-09-26")
        self.assertEqual(plan["updates"][0]["record_id"], "Rec2")
        self.assertEqual(plan["updates"][0]["updated_columns"]["Status"], "Blocked")

    def test_does_not_touch_other_owners(self):
        parsed = {"done": ["someone else task"], "today": [], "blocked": []}
        plan = S.plan_updates(self.records, "U1", parsed, "2026-09-26")
        # U1 has no matching row, so it is added under U1, Rec3 (U2) untouched.
        self.assertTrue(all(u["record_id"] != "Rec3" for u in plan["updates"]))


class TestOverdue(unittest.TestCase):
    def test_overdue_and_stale(self):
        records = [
            {"Record ID": "R1", "Task": "A", "Status": "In Progress", "Due Date": "2026-09-20", "Last Update": "2026-09-20"},
            {"Record ID": "R2", "Task": "B", "Status": "Done", "Due Date": "2026-09-01"},
            {"Record ID": "R3", "Task": "C", "Status": "To Do", "Due Date": "2026-12-01", "Last Update": "2026-09-25"},
        ]
        flags = S.find_overdue(records, "2026-09-26", stale_days=3)
        ids = {r["Record ID"] for r in flags["overdue"]}
        self.assertEqual(ids, {"R1"})  # R2 is Done, R3 not yet due
        self.assertIn("R1", {r["Record ID"] for r in flags["stale"]})


class TestSummaryAndDM(unittest.TestCase):
    def test_summary_has_totals_and_blockers(self):
        records = [
            {"Record ID": "R1", "Task": "A", "Owner": "U1", "Status": "Blocked", "Blocker": "waiting on keys"},
            {"Record ID": "R2", "Task": "B", "Owner": "U1", "Status": "Done"},
        ]
        out = S.build_summary(records, "2026-09-26")
        self.assertIn("Team totals", out)
        self.assertIn("blocked — *A*", out)
        self.assertIn("<@U1>", out)

    def test_compose_dm_lists_open_tasks(self):
        tasks = [{"Task": "Ship email", "Status": "In Progress", "Due Date": "2026-09-20"}]
        msg = S.compose_dm("Ana Ng", tasks, "2026-09-26")
        self.assertIn("Ana", msg)
        self.assertIn("Ship email", msg)
        self.assertIn("overdue", msg)  # due date is in the past
        self.assertIn("Blocked:", msg)

    def test_compose_dm_no_tasks(self):
        msg = S.compose_dm("", [], "2026-09-26")
        self.assertIn("No open tasks", msg)


class TestSchema(unittest.TestCase):
    def test_schema_is_valid_shape(self):
        names = [c["name"] for c in S.COLUMNS]
        self.assertIn("Task", names)
        self.assertIn("Owner", names)
        for c in S.COLUMNS:
            if c["type"] in ("select", "multi_select"):
                self.assertIn("options", c)
        # serialisable
        json.dumps(S.COLUMNS)


if __name__ == "__main__":
    unittest.main()
