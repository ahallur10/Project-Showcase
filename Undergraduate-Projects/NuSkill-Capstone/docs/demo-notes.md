# Demo notes (optional)
- Use an API client (Postman/Insomnia) to call:
  - `POST /api/auth/register` {email, password}
  - `POST /api/auth/login` -> get JWT token
  - `POST /api/payments/intent` (Authorization: Bearer <token>)
  - `POST /api/tutorials/progress` {uid, tutorial_id, percent}
  - `POST /api/tutorials/refund` {uid}
