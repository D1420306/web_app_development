import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import create_user, get_user_by_email, get_user_by_id

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """每次 Request 前，檢查 session 並將 user 放進全域 g 變數中"""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)

def login_required(view):
    """
    登入驗證共用裝飾器。
    若 g.user 為空則導回登入頁。
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("請先登入系統以訪問該頁面。", "warning")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """註冊畫面與處理"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        error = None

        if not username or not email or not password:
            error = "請填寫所有欄位。"
        elif get_user_by_email(email) is not None:
            error = "此信箱已經被註冊過。"

        if error is None:
            pwd_hash = generate_password_hash(password)
            user_id = create_user(username, email, pwd_hash)
            if user_id:
                flash("註冊成功！麻煩請您登入。", "success")
                return redirect(url_for('auth.login'))
            else:
                error = "系統發生異常，暫時無法完成註冊。"

        flash(error, "danger")
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """登入畫面與處理"""
    if g.user is not None:
        return redirect(url_for('expense.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error = None
        user = get_user_by_email(email)

        if user is None:
            error = '帳號錯誤或無此使用者。'
        elif not check_password_hash(user['password_hash'], password):
            error = '密碼錯誤。'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('expense.dashboard'))

        flash(error, 'danger')
    return render_template('auth/login.html')

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """登出功能"""
    session.clear()
    return redirect(url_for('auth.login'))
