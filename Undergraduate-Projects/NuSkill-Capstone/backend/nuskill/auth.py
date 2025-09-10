from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import jwt, datetime, os
from .config import JWT_SECRET
from .models import fetch_one, execute

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not email or not password:
        return jsonify(ok=False, error="email and password required"), 400
    existing = fetch_one("SELECT id FROM users WHERE email=?", (email,))
    if existing:
        return jsonify(ok=False, error="email already registered"), 400
    pwd_hash = generate_password_hash(password)
    execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, pwd_hash))
    return jsonify(ok=True), 201

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    user = fetch_one("SELECT id, password_hash FROM users WHERE email=?", (email,))
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify(ok=False, error="invalid credentials"), 401
    token = jwt.encode(
        {"uid": user["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)},
        JWT_SECRET, algorithm="HS256"
    )
    return jsonify(ok=True, token=token)
