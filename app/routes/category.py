from flask import Blueprint

bp = Blueprint('category', __name__, url_prefix='/categories')

@bp.route('/')
def index():
    """
    輸入: 無
    邏輯: 呼叫 get_categories_by_user 取得自己的專屬分類以及系統分類。
    輸出: render_template('category/index.html', categories=...)
    """
    pass

@bp.route('/add', methods=['POST'])
def add():
    """
    輸入: form (name, type)
    邏輯: 將該類別與當前的 session user_id 進行綁定，寫入資料表 (create_category)。
    輸出: redirect 到 /categories
    """
    pass

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    輸入: URL 中的 分類 id
    邏輯: 嘗試刪除 (delete_category)，僅能成功刪除同屬該使用者的類別。
    輸出: redirect 到 /categories
    """
    pass
