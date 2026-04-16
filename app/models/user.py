from app.models.db import get_db

def create_user(username, email, password_hash):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash)
    )
    db.commit()
    user_id = cursor.lastrowid
    db.close()
    return user_id

def get_user_by_id(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()
    return dict(user) if user else None

def get_user_by_username(username):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    db.close()
    return dict(user) if user else None

def get_user_by_email(email):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    db.close()
    return dict(user) if user else None

def get_all_users():
    db = get_db()
    users = db.execute("SELECT id, username, email, role, created_at FROM users").fetchall()
    db.close()
    return [dict(u) for u in users]
