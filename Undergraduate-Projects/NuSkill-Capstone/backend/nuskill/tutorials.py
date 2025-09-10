from flask import Blueprint, request, jsonify
from .models import fetch_one, fetch_all, execute

tuts_bp = Blueprint("tuts", __name__, url_prefix="/api/tutorials")

@tuts_bp.post("/progress")
def record_progress():
    data = request.get_json() or {}
    uid = int(data.get("uid", 0))
    tutorial_id = int(data.get("tutorial_id", 0))
    pct = float(data.get("percent", 0))
    if not uid or not tutorial_id:
        return jsonify(ok=False, error="uid and tutorial_id required"), 400

    existing = fetch_one("SELECT percent FROM progress WHERE user_id=? AND tutorial_id=?", (uid, tutorial_id))
    if existing:
        execute("UPDATE progress SET percent=? WHERE user_id=? AND tutorial_id=?", (pct, uid, tutorial_id))
    else:
        execute("INSERT INTO progress (user_id, tutorial_id, percent) VALUES (?, ?, ?)", (uid, tutorial_id, pct))

    if pct >= 100:
        execute("UPDATE deposits SET refund_eligible=1 WHERE user_id=? AND consumed=0", (uid,))
    return jsonify(ok=True, percent=pct)

@tuts_bp.post("/refund")
def refund():
    data = request.get_json() or {}
    uid = int(data.get("uid", 0))
    if not uid:
        return jsonify(ok=False, error="uid required"), 400
    dep = fetch_one("SELECT id, amount_usd FROM deposits WHERE user_id=? AND refund_eligible=1 AND consumed=0", (uid,))
    if not dep:
        return jsonify(ok=False, error="no refundable deposit"), 400
    execute("UPDATE deposits SET consumed=1 WHERE id=?", (dep["id"],))
    return jsonify(ok=True, refunded=float(dep["amount_usd"]))
