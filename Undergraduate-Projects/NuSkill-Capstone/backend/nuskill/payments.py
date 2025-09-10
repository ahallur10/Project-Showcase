import os, uuid
from flask import Blueprint, request, jsonify

payments_bp = Blueprint("payments", __name__, url_prefix="/api/payments")
MOCK = os.getenv("PAYMENTS_MOCK", "1") == "1"

@payments_bp.post("/intent")
def create_intent():
    data = request.get_json() or {}
    amount_usd = float(data.get("amount_usd", 10))
    if MOCK:
        return jsonify(ok=True, intent_id=f"mock_{uuid.uuid4()}", pay_url="https://example.com/pay", amount_usd=amount_usd)
    # In real mode, call your payments provider
    return jsonify(ok=False, error="real payments not configured"), 501
