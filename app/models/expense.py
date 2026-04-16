import sqlite3
from app.models.db import get_db

def add_expense(user_id, category_id, amount, date, note):
    """
    新增一筆收支紀錄
    """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO expenses (user_id, category_id, amount, date, note) VALUES (?, ?, ?, ?, ?)",
            (user_id, category_id, amount, date, note)
        )
        db.commit()
        expense_id = cursor.lastrowid
        db.close()
        return expense_id
    except sqlite3.Error as e:
        print(f"Database error in add_expense: {e}")
        return None

def get_expenses_by_user(user_id, limit=50, offset=0):
    """
    取得該名使用者的收支列表，透過 JOIN 關聯取得分類名稱
    """
    try:
        db = get_db()
        query = """
            SELECT e.*, c.name as category_name, c.type as category_type
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.user_id = ?
            ORDER BY e.date DESC, e.created_at DESC
            LIMIT ? OFFSET ?
        """
        expenses = db.execute(query, (user_id, limit, offset)).fetchall()
        db.close()
        return [dict(e) for e in expenses]
    except sqlite3.Error as e:
        print(f"Database error in get_expenses_by_user: {e}")
        return []

def get_expense_by_id(expense_id, user_id):
    """取得單筆收支紀錄，需要驗證使用者身分"""
    try:
        db = get_db()
        query = """
            SELECT e.*, c.name as category_name, c.type as category_type
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.id = ? AND e.user_id = ?
        """
        expense = db.execute(query, (expense_id, user_id)).fetchone()
        db.close()
        return dict(expense) if expense else None
    except sqlite3.Error as e:
        print(f"Database error in get_expense_by_id: {e}")
        return None

def update_expense(expense_id, user_id, category_id, amount, date, note):
    """更新收支紀錄"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            UPDATE expenses 
            SET category_id = ?, amount = ?, date = ?, note = ?
            WHERE id = ? AND user_id = ?
            """,
            (category_id, amount, date, note, expense_id, user_id)
        )
        db.commit()
        updated_count = cursor.rowcount
        db.close()
        return updated_count > 0
    except sqlite3.Error as e:
        print(f"Database error in update_expense: {e}")
        return False

def delete_expense(expense_id, user_id):
    """刪除收支紀錄"""
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM expenses WHERE id = ? AND user_id = ?",
            (expense_id, user_id)
        )
        db.commit()
        deleted_count = cursor.rowcount
        db.close()
        return deleted_count > 0
    except sqlite3.Error as e:
        print(f"Database error in delete_expense: {e}")
        return False

def get_monthly_summary(user_id, year_month):
    """
    按月取得收支摘要，year_month 格式例如: '2026-04'
    """
    try:
        db = get_db()
        query = """
            SELECT c.type, SUM(e.amount) as total
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE e.user_id = ? AND e.date LIKE ?
            GROUP BY c.type
        """
        summary = db.execute(query, (user_id, year_month + '%')).fetchall()
        db.close()
        
        result = {'income': 0.0, 'expense': 0.0}
        for row in summary:
            if row['total'] is not None:
                result[row['type']] = float(row['total'])
        return result
    except sqlite3.Error as e:
        print(f"Database error in get_monthly_summary: {e}")
        return {'income': 0.0, 'expense': 0.0}
