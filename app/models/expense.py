from app.models.db import get_db

def add_expense(user_id, category_id, amount, date, note):
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

def get_expenses_by_user(user_id, limit=50, offset=0):
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

def get_expense_by_id(expense_id, user_id):
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

def update_expense(expense_id, user_id, category_id, amount, date, note):
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

def delete_expense(expense_id, user_id):
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

def get_monthly_summary(user_id, year_month):
    """
    year_month 格式例如: '2026-04'
    """
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
        result[row['type']] = row['total']
    return result
