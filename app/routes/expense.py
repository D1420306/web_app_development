from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.routes.auth import login_required
from app.models.expense import add_expense, get_expenses_by_user, get_expense_by_id, update_expense, delete_expense, get_monthly_summary
from app.models.category import get_categories_by_user
import datetime

bp = Blueprint('expense', __name__)

@bp.route('/')
@login_required
def dashboard():
    """儀表板 (首頁)，必須登入"""
    today = datetime.date.today()
    current_month = today.strftime('%Y-%m')
    summary = get_monthly_summary(g.user['id'], current_month)
    recent_expenses = get_expenses_by_user(g.user['id'], limit=5)
    return render_template('expense/dashboard.html', summary=summary, recent_expenses=recent_expenses, current_month=current_month)

@bp.route('/expenses')
@login_required
def index():
    """所有收支列表清單"""
    expenses = get_expenses_by_user(g.user['id'])
    return render_template('expense/index.html', expenses=expenses)

@bp.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def add():
    """新增一筆紀錄"""
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        date = request.form.get('date')
        note = request.form.get('note')
        error = None

        if not category_id or not amount or not date:
            error = "必須填寫分類、金額與日期。"
        
        if error is None:
            if add_expense(g.user['id'], category_id, amount, date, note):
                flash('新增一筆紀錄成功！', 'success')
                return redirect(url_for('expense.index'))
            else:
                error = '新增紀錄發生系統錯誤，請稍後再試。'

        flash(error, 'danger')

    categories = get_categories_by_user(g.user['id'])
    return render_template('expense/add.html', categories=categories)

@bp.route('/expenses/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """編輯指定的紀錄"""
    expense = get_expense_by_id(id, g.user['id'])
    if not expense:
        flash("找不到該筆紀錄或無權限修改。", "danger")
        return redirect(url_for('expense.index'))

    if request.method == 'POST':
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        date = request.form.get('date')
        note = request.form.get('note')
        error = None

        if not category_id or not amount or not date:
            error = "必須填寫分類、金額與日期。"
        
        if error is None:
            if update_expense(id, g.user['id'], category_id, amount, date, note):
                flash('已成功更新本筆紀錄！', 'success')
                return redirect(url_for('expense.index'))
            else:
                error = '編輯紀錄發生錯誤。'
                
        flash(error, 'danger')

    categories = get_categories_by_user(g.user['id'])
    return render_template('expense/edit.html', expense=expense, categories=categories)

@bp.route('/expenses/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """刪除指定紀錄"""
    if delete_expense(id, g.user['id']):
        flash("紀錄已成功刪除。", "success")
    else:
        flash("刪除失敗或您無權限刪除。", "danger")
    return redirect(url_for('expense.index'))

@bp.route('/reports')
@login_required
def reports():
    """查看每月圖表報表"""
    month = request.args.get('month', datetime.date.today().strftime('%Y-%m'))
    report_data = get_monthly_summary(g.user['id'], month)
    return render_template('expense/reports.html', report_data=report_data, selected_month=month)
