from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    輸入:
        GET: 無
        POST: form (username, email, password)
    邏輯:
        GET: 顯示註冊頁面。
        POST: 驗證欄位是否空白。檢查信箱是否已存在。將密碼進行 Hash。呼叫 create_user。
    輸出:
        GET: render_template('auth/register.html')
        POST: 成功則 redirect 到登入頁，失敗則 flash 錯誤並重新 render form。
    """
    pass

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    輸入:
        GET: 無
        POST: form (email, password)
    邏輯:
        GET: 顯示登入頁面。若已在 session 中有 user_id 則直接跳轉到 dashboard `/`。
        POST: 根據 email 尋找 user。驗證 password_hash。將 user_id 寫入 session。
    輸出:
        GET: render_template('auth/login.html')
        POST: 成功則 redirect 到 /，失敗則 flash 錯誤並重新 render form。
    """
    pass

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    輸入: 無
    邏輯: 從 session 中移除 user_id。
    輸出: redirect 到 /auth/login。
    """
    pass
