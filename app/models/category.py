import sqlite3
from app.models.db import get_db

def create_category(user_id, name, type):
    """
    新增分類記錄
    參數: user_id (若為 Null 則是預設分類), name, type ('income' or 'expense')
    回傳: 成功傳回 category_id，失敗則為 None
    """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO categories (user_id, name, type) VALUES (?, ?, ?)",
            (user_id, name, type)
        )
        db.commit()
        category_id = cursor.lastrowid
        db.close()
        return category_id
    except sqlite3.Error as e:
        print(f"Database error in create_category: {e}")
        return None

def get_categories_by_user(user_id):
    """
    取得該使用者的專屬分類以及系統預設 (user_id IS NULL) 的分類
    """
    try:
        db = get_db()
        categories = db.execute(
            "SELECT * FROM categories WHERE user_id = ? OR user_id IS NULL ORDER BY user_id, id",
            (user_id,)
        ).fetchall()
        db.close()
        return [dict(c) for c in categories]
    except sqlite3.Error as e:
        print(f"Database error in get_categories_by_user: {e}")
        return []

def get_category_by_id(category_id):
    """依據 ID 取得特定分類"""
    try:
        db = get_db()
        category = db.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
        db.close()
        return dict(category) if category else None
    except sqlite3.Error as e:
        print(f"Database error in get_category_by_id: {e}")
        return None

def update_category(category_id, user_id, name, type):
    """更新分類名稱或類型（必需同屬此使用者）"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE categories SET name = ?, type = ? WHERE id = ? AND user_id = ?",
            (name, type, category_id, user_id)
        )
        db.commit()
        success = cursor.rowcount > 0
        db.close()
        return success
    except sqlite3.Error as e:
        print(f"Database error in update_category: {e}")
        return False

def delete_category(category_id, user_id):
    """
    僅允許刪除該使用者的專屬分類，不可刪除系統自動庫
    """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM categories WHERE id = ? AND user_id = ?",
            (category_id, user_id)
        )
        db.commit()
        deleted_count = cursor.rowcount
        db.close()
        return deleted_count > 0
    except sqlite3.Error as e:
        print(f"Database error in delete_category: {e}")
        return False
