import json
from flask import Blueprint, request, jsonify

# Bring in mock flag and light utilities
from snowflake_db.snowflake_engine import (
    USE_MOCK, get_user, insert_user, get_user_deposited
)

# Real auth helpers (used only when not mocking)
from login.register import sign_up, id_login

user_services_handler = Blueprint('user_services_handler', __name__, template_folder='templates')


@user_services_handler.route("/user/register", methods=['POST'])
def register():
    data = request.get_json(force=True) or {}
    user_id = data.get('user_id') or data.get('id') or data.get('username') or data.get('walletId')
    password = data.get('password') or data.get('pw') or ""

    if not user_id:
        return jsonify({"status": 400, "body": "missing user_id"}), 400

    # --- MOCK MODE: create user in in-memory store, no hashing ---
    if USE_MOCK:
        if len(get_user(user_id)) == 0:
            insert_user(user_id, password)  # our mock just stores it in memory
            return jsonify({"status": 200, "body": "Success"}), 200
        else:
            return jsonify({"status": 200, "body": "ID already registered"}), 200

    # --- REAL MODE ---
    if len(get_user(user_id)) == 0:
        sign_up(user_id, password)  # whatever real flow does (hashing, DB insert)
        return jsonify({"status": 200, "body": "Success"}), 200
    else:
        return jsonify({"status": 200, "body": "ID already registered"}), 200


@user_services_handler.route("/user/login", methods=['POST'])
def login():
    data = request.get_json(force=True) or {}
    user_id = data.get('user_id') or data.get('id') or data.get('username') or data.get('walletId')
    password = data.get('password') or data.get('pw') or ""

    if not user_id:
        return jsonify({"status": 400, "body": "missing user_id"}), 400

    # --- MOCK MODE: skip hashing; succeed if the user exists in mock table ---
    if USE_MOCK:
        recs = get_user(user_id)  # [(id, stored_pw, total, balance)] or []
        if not recs:
            return jsonify({"status": 404, "body": "user not found"}), 404
        return jsonify({"status": 200, "body": "Success", "user": {"id": user_id}}), 200

    # --- REAL MODE: delegate to original function (hash check etc.) ---
    try:
        id_login(user_id, password)
        return jsonify({"status": 200, "body": "Success"}), 200
    except Exception:
        # Don’t leak internal errors (like invalid salt). Treat as bad creds.
        return jsonify({"status": 401, "body": "invalid credentials"}), 401


@user_services_handler.route("/user/status", methods=['POST'])
def status():
    data = request.get_json(force=True) or {}
    user_id = data.get('user_id') or data.get('id') or data.get('username') or data.get('walletId')
    if not user_id:
        return jsonify({"status": 400, "body": "missing user_id"}), 400

    # Works for both modes; in mock it returns the in-memory list
    return jsonify({"status": 200, "body": get_user_deposited(user_id)}), 200

