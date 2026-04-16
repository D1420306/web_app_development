from flask import Blueprint

bp = Blueprint('expense', __name__) # 無 prefix

@bp.route('/')
def dashboard():
    """
    輸入: session user_id
    邏輯:
        1. 檢查是否登入，未登入 redirect 到 /auth/login。
        2. 呼叫 get_monthly_summary 取得本月概況。
        3. 呼叫 get_expenses_by_user 取前五筆紀錄作為近期一覽。
    輸出: render_template('expense/dashboard.html', summary=..., recent_expenses=...)
    """
    pass

@bp.route('/expenses')
def index():
    """
    輸入: query params (如 limit, offset 或是日期的搜尋條件)
    邏輯: 呼叫 get_expenses_by_user 取得收支清單。
    輸出: render_template('expense/index.html', expenses=...)
    """
    pass

@bp.route('/expenses/add', methods=['GET', 'POST'])
def add():
    """
    輸入:
        GET: 無
        POST: form (category_id, amount, date, note)
    邏輯:
        GET: 呼叫 get_categories_by_user 準備下拉選單。
        POST: 驗證欄位，呼叫 add_expense 存入 DB。
    輸出:
        GET: render_template('expense/add.html', categories=...)
        POST: redirect 到 /expenses
    """
    pass

@bp.route('/expenses/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    輸入: 
        GET: 紀錄 ID
        POST: form (category_id, amount, date, note)
    邏輯:
        GET: 確認該條紀錄為當前使用者所有 (get_expense_by_id)，取得清單並將紀錄預設填入表單。若無權則 404。
        POST: 確認歸屬權並呼叫 update_expense 更新內容。
    輸出:
        GET: render_template('expense/edit.html', expense=..., categories=...)
        POST: redirect 到 /expenses
    """
    pass

@bp.route('/expenses/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    輸入: 紀錄 ID
    邏輯: 刪除指定的收支，並在 DB 曾驗證只能刪除歸屬自己的紀錄。
    輸出: redirect 到 /expenses
    """
    pass

@bp.route('/reports')
def reports():
    """
    輸入: URL query 的月份設定 (預設為本月)
    邏輯: 整理當月所有的紀錄進行分類計算 (get_monthly_summary 等)，準備圖表資料。
    輸出: render_template('expense/reports.html', report_data=...)
    """
    pass
