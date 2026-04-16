from app.models.db import get_db

def create_category(user_id, name, type):
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

def get_categories_by_user(user_id):
    """
    取得該使用者的專屬分類以及系統預設 (user_id IS NULL) 的分類
    """
    db = get_db()
    categories = db.execute(
        "SELECT * FROM categories WHERE user_id = ? OR user_id IS NULL ORDER BY user_id, id",
        (user_id,)
    ).fetchall()
    db.close()
    return [dict(c) for c in categories]

def get_category_by_id(category_id):
    db = get_db()
    category = db.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
    db.close()
    return dict(category) if category else None

def delete_category(category_id, user_id):
    """
    僅允許刪除該使用者的專屬分類，不可刪除系統分類
    """
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
