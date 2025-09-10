# Architecture (1-pager)

**Goal:** Demonstrate the NuSkill accountability flow end-to-end without real secrets.

## Components
- **Flask API** (`backend/`): Auth, deposit intent (mock), progress tracking, refund.
- **DB**: SQLite for demo; Snowflake connector path retained (disabled by default).
- **Payments client**: Abstraction with `PAYMENTS_MOCK=1` support.
- **Frontend samples**: Non-running illustrative React components for reviewers.

## Key Design Choices
- **Abstractions**: `payments.py` hides external API; easily swapped from mock → real.
- **Security**: Hashed passwords, JWT-based auth, parameterized queries.
- **Idempotency**: `MERGE`-like upserts for progress (emulated in SQLite).

## Sequence Diagram
See the Mermaid diagram in the root README.
