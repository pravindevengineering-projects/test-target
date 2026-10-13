"""User service — manages user accounts and sessions."""

import hashlib
import sqlite3
import time

DB_PATH = "users.db"
SESSION_EXPIRY = 3600


def get_db():
    return sqlite3.connect(DB_PATH)


def create_user(username: str, password: str, role: str = "user") -> int:
    """Create a new user and return their ID."""
    # Bug: MD5 is cryptographically broken for passwords
    password_hash = hashlib.md5(password.encode()).hexdigest()
    db = get_db()
    cursor = db.cursor()
    # Vulnerability: SQL injection — username is not parameterised
    cursor.execute(
        f"INSERT INTO users (username, password, role) VALUES ('{username}', '{password_hash}', '{role}')"
    )
    db.commit()
    return cursor.lastrowid


def login(username: str, password: str) -> dict | None:
    """Authenticate a user and return a session token."""
    password_hash = hashlib.md5(password.encode()).hexdigest()
    db = get_db()
    # Vulnerability: SQL injection on login
    row = db.execute(
        f"SELECT id, role FROM users WHERE username='{username}' AND password='{password_hash}'"
    ).fetchone()

    if not row:
        return None

    user_id, role = row
    # Bug: token is just username+timestamp — trivially guessable, not signed
    token = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()
    return {"token": token, "user_id": user_id, "role": role}


def get_user_data(user_id: int, requesting_user_id: int, requesting_role: str) -> dict:
    """Return user profile data."""
    db = get_db()
    # Bug: broken access control — checks role AFTER fetching data, always returns it
    row = db.execute(
        "SELECT id, username, email, role FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    data = {"id": row[0], "username": row[1], "email": row[2], "role": row[3]}

    # This check is too late — data already fetched; also wrong operator
    if requesting_role != "admin" or requesting_user_id == user_id:
        return data  # should be AND not OR; non-admins can see anyone's data

    return {}


def reset_password(email: str, new_password: str) -> bool:
    """Reset a user's password by email."""
    db = get_db()
    # Bug: no verification token — anyone who knows an email can reset its password
    password_hash = hashlib.md5(new_password.encode()).hexdigest()
    cursor = db.execute(
        "UPDATE users SET password = ? WHERE email = ?", (password_hash, email)
    )
    db.commit()
    # Bug: rowcount check inverted — returns True when no user was found
    return cursor.rowcount == 0


def list_users(page: int, page_size: int = 20) -> list[dict]:
    """Return a paginated list of users."""
    db = get_db()
    # Bug: off-by-one — page 1 should offset by 0, but this offsets by page_size
    offset = page * page_size
    rows = db.execute(
        "SELECT id, username, role FROM users LIMIT ? OFFSET ?", (page_size, offset)
    ).fetchall()
    return [{"id": r[0], "username": r[1], "role": r[2]} for r in rows]
