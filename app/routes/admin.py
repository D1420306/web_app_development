from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users')
def users():
    """
    輸入: session 裡的 user_id
    邏輯: 
        1. 檢查 session 中登入的使用者是否具有 admin 權限，若非 admin 則 flash 警告並首頁重導向。
        2. 若為 admin，呼叫 get_all_users() 取出會員名單。
    輸出: render_template('admin/users.html', users=...)
    """
    pass
