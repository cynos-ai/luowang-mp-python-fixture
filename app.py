"""Disposable non-production account app for LuoWang's Python project acceptance."""

from __future__ import annotations

import hmac
import os
import re
import secrets
import sqlite3
from contextlib import closing
from pathlib import Path

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import Flask, jsonify, make_response, request


RUN_ID = re.compile(r"^[0-9A-HJKMNP-TV-Z]{26}$")
ARGON2ID = re.compile(r"^\$argon2id\$v=19\$m=\d+,t=\d+,p=\d+\$[A-Za-z0-9+/]+\$[A-Za-z0-9+/]+$")
HASHER = PasswordHasher()


def create_app(database_path: str, cleanup_token: str | None = None) -> Flask:
    if cleanup_token is not None and len(cleanup_token) < 32:
        raise ValueError("CYNOS_TEST_DATA_CLEANUP_TOKEN must contain at least 32 characters")
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    app = Flask(__name__)

    def connection() -> sqlite3.Connection:
        db = sqlite3.connect(path)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        return db

    with closing(connection()) as db, db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                display_name TEXT NOT NULL,
                password_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )

    def current_user(db: sqlite3.Connection):
        token = request.cookies.get("sid", "")
        if not token:
            return None
        return db.execute(
            "SELECT users.id, users.email, users.display_name FROM sessions "
            "JOIN users ON users.id = sessions.user_id WHERE sessions.token = ?",
            (token,),
        ).fetchone()

    def start_session(db: sqlite3.Connection, user_id: int, payload: dict):
        token = secrets.token_urlsafe(32)
        db.execute("INSERT INTO sessions(token, user_id) VALUES (?, ?)", (token, user_id))
        response = make_response(jsonify(payload), 201)
        response.set_cookie("sid", token, httponly=True, samesite="Lax", secure=False)
        return response

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/")
    def index():
        return """<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><title>Python 账号实验站</title>
<h1>Python 账号实验站</h1>
<form id="register"><label>昵称 <input name="displayName" required></label>
<label>邮箱 <input name="email" type="email" required></label>
<label>密码 <input name="password" type="password" minlength="12" required></label>
<button type="submit">注册</button></form>
<p id="message" role="status"></p><button id="delete" type="button">删除账号</button>
<script>
document.querySelector('#register').addEventListener('submit', async event => {
  event.preventDefault();
  const body = Object.fromEntries(new FormData(event.target));
  const response = await fetch('/api/auth/register', {
    method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify(body)
  });
  const result = await response.json();
  document.querySelector('#message').textContent = response.ok
    ? `Welcome, ${result.user.displayName}.` : result.error;
});
document.querySelector('#delete').addEventListener('click', async () => {
  const response = await fetch('/api/me', {method: 'DELETE'});
  document.querySelector('#message').textContent = response.ok ? '账号已删除。' : '删除失败。';
});
</script></html>"""

    @app.post("/api/auth/register")
    def register():
        data = request.get_json(silent=True) or {}
        email = str(data.get("email", "")).strip().lower()
        display_name = str(data.get("displayName", "")).strip()
        password = data.get("password", "")
        if not email or "@" not in email or not display_name or len(display_name) > 100:
            return jsonify({"error": "INVALID_ACCOUNT"}), 400
        if not isinstance(password, str) or len(password) < 12:
            return jsonify({"error": "WEAK_PASSWORD"}), 400
        with closing(connection()) as db, db:
            try:
                cursor = db.execute(
                    "INSERT INTO users(email, display_name, password_hash) VALUES (?, ?, ?)",
                    (email, display_name, HASHER.hash(password)),
                )
            except sqlite3.IntegrityError:
                return jsonify({"error": "ACCOUNT_EXISTS"}), 409
            payload = {"user": {"email": email, "displayName": display_name}}
            return start_session(db, cursor.lastrowid, payload)

    @app.post("/api/auth/login")
    def login():
        data = request.get_json(silent=True) or {}
        email = str(data.get("email", "")).strip().lower()
        password = data.get("password", "")
        with closing(connection()) as db, db:
            row = db.execute(
                "SELECT id, email, display_name, password_hash FROM users WHERE email = ?", (email,)
            ).fetchone()
            if row is None or not isinstance(password, str):
                return jsonify({"error": "INVALID_CREDENTIALS"}), 401
            try:
                HASHER.verify(row["password_hash"], password)
            except VerifyMismatchError:
                return jsonify({"error": "INVALID_CREDENTIALS"}), 401
            return start_session(
                db,
                row["id"],
                {"user": {"email": row["email"], "displayName": row["display_name"]}},
            )

    @app.get("/api/auth/status")
    def status():
        with closing(connection()) as db, db:
            user = current_user(db)
            if user is None:
                return jsonify({"authenticated": False})
            return jsonify(
                {"authenticated": True, "user": {"email": user["email"], "displayName": user["display_name"]}}
            )

    @app.delete("/api/me")
    def delete_me():
        with closing(connection()) as db, db:
            user = current_user(db)
            if user is None:
                return jsonify({"error": "UNAUTHORIZED"}), 401
            db.execute("DELETE FROM users WHERE id = ?", (user["id"],))
        response = make_response(jsonify({"deleted": True}))
        response.delete_cookie("sid")
        return response

    if cleanup_token is not None:
        def authorized() -> bool:
            return hmac.compare_digest(
                request.headers.get("Authorization", ""), f"Bearer {cleanup_token}"
            )

        def pattern(run_id: str) -> str:
            return f"luowang-{run_id.lower()}-%"

        @app.route("/api/luowang/test-data/<run_id>", methods=["GET", "DELETE"])
        def cleanup(run_id: str):
            if not authorized():
                return jsonify({"error": "UNAUTHORIZED"}), 401
            if not RUN_ID.fullmatch(run_id):
                return jsonify({"error": "INVALID_RUN_ID"}), 400
            with closing(connection()) as db, db:
                deleted = 0
                if request.method == "DELETE":
                    deleted = db.execute(
                        "DELETE FROM users WHERE lower(email) LIKE ? OR lower(display_name) LIKE ?",
                        (pattern(run_id), pattern(run_id)),
                    ).rowcount
                remaining = db.execute(
                    "SELECT count(*) FROM users WHERE lower(email) LIKE ? OR lower(display_name) LIKE ?",
                    (pattern(run_id), pattern(run_id)),
                ).fetchone()[0]
            return jsonify({"runId": run_id, "deleted": deleted, "remaining": remaining})

        @app.get("/api/luowang/test-data/<run_id>/storage")
        def storage(run_id: str):
            if not authorized():
                return jsonify({"error": "UNAUTHORIZED"}), 401
            if not RUN_ID.fullmatch(run_id):
                return jsonify({"error": "INVALID_RUN_ID"}), 400
            with closing(connection()) as db, db:
                rows = db.execute(
                    "SELECT password_hash FROM users WHERE lower(email) LIKE ? OR lower(display_name) LIKE ?",
                    (pattern(run_id), pattern(run_id)),
                ).fetchall()
            argon2id = sum(bool(ARGON2ID.fullmatch(row["password_hash"])) for row in rows)
            response = jsonify(
                {"runId": run_id, "accounts": len(rows), "argon2id": argon2id, "other": len(rows) - argon2id}
            )
            response.headers["Cache-Control"] = "no-store"
            return response

    return app


if __name__ == "__main__":
    app = create_app(
        str(Path(os.environ.get("APP_DATA_DIR", "/data")) / "fixture.db"),
        os.environ.get("CYNOS_TEST_DATA_CLEANUP_TOKEN") or None,
    )
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "3100")))
