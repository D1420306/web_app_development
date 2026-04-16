from flask import Blueprint, render_template, redirect, url_for, flash, g
from app.routes.auth import login_required
from app.models.user import get_all_users

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users')
@login_required
def users():
    """僅具有 admin 權限的人員可檢視總註冊名單"""
    if g.user['role'] != 'admin':
        flash("不好意思，您沒有權限訪問後台管理區塊。", "danger")
        return redirect(url_for('expense.dashboard'))
        
    users_list = get_all_users()
    return render_template('admin/users.html', users=users_list)
