# PolicyDrift: Proof of What a Policy Page Used to Say

**Category:** Intelligent Contracts (standalone primitive)
**Files:** `policydrift.py` (contract), `test_flow.py` (call-sequence walkthrough)

## The problem

Terms of service, privacy and refund policies change quietly. A line like
"disputes go to binding arbitration" or "your plan renews automatically"
can appear between two visits with no announcement, and afterwards nobody
can show what the page said before. One AI summary is not evidence either:
it differs from run to run.

## The primitive

Register a policy page. Anyone can file a **snapshot**: every validator
fetches the page itself and marks which of 12 fixed clause types it contains
(arbitration, auto-renewal, data sale, refund window, and so on). The agreed
list is stored in an append-only history (max 6 snapshots). `get_drift`
compares any two snapshots: what was added, what was removed, and whether a
high-stakes clause changed.

## Consensus design: tiered set agreement

Validators agree on a **set**, and not every member counts equally:

- **Critical clauses** (binding arbitration, class-action waiver, auto
  renewal, data sale, unilateral changes) must match **exactly**. A split on
  one of these is the dispute itself, so no tolerance is allowed.
- **Routine clauses** (the other 7) may differ a little: the full sets must
  overlap by at least 75% (Jaccard).
- The taxonomy is closed, so there is no free text to manipulate. Unknown ids
  are rejected or filtered.

This is a different shape from a single field, a numeric band, an ordered
category, a per-source vector, or an order-swap check.

## Replay rules

- Append-only, numbered 1 to 6. Filing needs `expected_index` equal to the
  next number, so simultaneous filers cannot create duplicates and nobody can
  overwrite history.
- Max 6 snapshots per policy.
- An unreachable page never produces a snapshot.

## State

| Map | Key | Value |
|---|---|---|
| `policies` | `policy_id` | registrant, url, snapshot count |
| `snapshots` | `policy_id\|n` | clauses found, filer |

No page text is stored, only the clause list. `total_policies` and
`total_snapshots` are `u256` counters.

## Known limitations

- Only the first ~12,000 characters of text are read.
- "Clause present" is a model reading, not legal advice, and says nothing
  about how fair the wording is.
- No timestamps: order is the only clock.
- A site can serve different text to different visitors.
- Page text is untrusted; a determined author could try to steer the reading.

## Extending

- Let other contracts refuse to act while `critical_changed` is true.
- Add a notify/subscribe hook for a new critical clause.
- Extend the taxonomy per policy type.
