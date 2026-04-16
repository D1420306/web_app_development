import sqlite3
from app.models.db import get_db

def create_user(username, email, password_hash, role='user'):
    """
    新增一位使用者。
    參數: username, email, password_hash, role
    回傳: 成功傳回 user_id，失敗傳回 None
    """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, role)
        )
        db.commit()
        user_id = cursor.lastrowid
        db.close()
        return user_id
    except sqlite3.Error as e:
        print(f"Database error in create_user: {e}")
        return None

def get_user_by_id(user_id):
    """取得單一使用者 (依據 ID)"""
    try:
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        db.close()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"Database error in get_user_by_id: {e}")
        return None

def get_user_by_username(username):
    """取得單一使用者 (依據 username)"""
    try:
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        db.close()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"Database error in get_user_by_username: {e}")
        return None

def get_user_by_email(email):
    """取得單一使用者 (依據 email)"""
    try:
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        db.close()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"Database error in get_user_by_email: {e}")
        return None

def get_all_users():
    """取得所有使用者列表 (通常供管理員使用)"""
    try:
        db = get_db()
        users = db.execute("SELECT id, username, email, role, created_at FROM users").fetchall()
        db.close()
        return [dict(u) for u in users]
    except sqlite3.Error as e:
        print(f"Database error in get_all_users: {e}")
        return []

def update_user(user_id, username, email, password_hash, role):
    """更新使用者資訊"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, email = ?, password_hash = ?, role = ? WHERE id = ?",
            (username, email, password_hash, role, user_id)
        )
        db.commit()
        success = cursor.rowcount > 0
        db.close()
        return success
    except sqlite3.Error as e:
        print(f"Database error in update_user: {e}")
        return False

def delete_user(user_id):
    """刪除使用者"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()
        success = cursor.rowcount > 0
        db.close()
        return success
    except sqlite3.Error as e:
        print(f"Database error in delete_user: {e}")
        return False
