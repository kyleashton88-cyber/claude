# Review record

Append-only. Do not edit lines already written.
`publish_allowed` is computed from the ledger. Nothing here publishes.

## 1. init

```json
{
  "type": "init",
  "id": "synthetic-short",
  "format": "short",
  "master": "test-outputs/master.mp4",
  "master_hash": "cfef9ad6a0d1e916ef6048ec2f856e32a9c5b1a1e2d310c8d4b274aebb675174",
  "seq": 1
}
```

After this event, publish allowed is **false**.

## 2. qa

```json
{
  "type": "qa",
  "result": "pass",
  "master_hash": "cfef9ad6a0d1e916ef6048ec2f856e32a9c5b1a1e2d310c8d4b274aebb675174",
  "report": "test-outputs/qa-report.json",
  "report_hash": "c3502b772c0f1c9c00e9d13ac48328754ac8f90f28c49f657d4bb5f5ba13e465",
  "failed": [],
  "seq": 2
}
```

After this event, publish allowed is **false**.

## 3. compliance

```json
{
  "type": "compliance",
  "status": "pending legal review",
  "content_result": "pass",
  "content_hash": "demo-synthetic-script",
  "flag_count": 0,
  "report": "test-outputs/compliance-report.json",
  "report_hash": "9aee30860f0cd3d6a3e7dceb71c6d2b7c3b05a7b1c887639234184034a07de8e",
  "seq": 3
}
```

After this event, publish allowed is **false**.

## 4. legal

```json
{
  "type": "legal",
  "decision": "approved",
  "name": "Demo Counsel",
  "date": "2026-11-13",
  "content_hash": "demo-synthetic-script",
  "content_result": "pass",
  "seq": 4
}
```

After this event, publish allowed is **false**.

## 5. stewart

```json
{
  "type": "stewart",
  "decision": "yes",
  "name": "Stewart Crown",
  "date": "2026-11-13",
  "notified": false,
  "seq": 5
}
```

After this event, publish allowed is **true**.

