# SAFE_NOTES

This portfolio-ready slice intentionally **removes/redacts** any sensitive information.

## Removed / Redacted
- Coinbase/Crypto API keys and webhooks
- Real Snowflake credentials, account names, warehouses
- Any non-public links, IDs, or organization-specific diagrams

## How to run safely (mock mode)
Set the following in your `.env` or shell:
```
PAYMENTS_MOCK=1
USE_SQLITE=1
JWT_SECRET=dev-secret
```

Then initialize the demo DB:
```
python -c "from nuskill.models import init_demo_db; init_demo_db()"
```

## Optional: connect to Snowflake (not required)
Provide these in `.env` if you want to try the Snowflake path:
```
SNOW_USER=...
SNOW_PASS=...
SNOW_ACCOUNT=...
SNOW_WH=...
SNOW_DB=...
SNOW_SCHEMA=PUBLIC
```
