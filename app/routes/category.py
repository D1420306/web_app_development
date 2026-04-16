from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.routes.auth import login_required
from app.models.category import get_categories_by_user, create_category, delete_category

bp = Blueprint('category', __name__, url_prefix='/categories')

@bp.route('/')
@login_required
def index():
    """顯示分類清單"""
    categories = get_categories_by_user(g.user['id'])
    return render_template('category/index.html', categories=categories)

@bp.route('/add', methods=['POST'])
@login_required
def add():
    """處理接收新增分類的表單資訊"""
    name = request.form.get('name')
    type_val = request.form.get('type')
    
    if not name or type_val not in ['income', 'expense']:
        flash("請輸入有效的分類名稱與選擇類別。 (需為 income 或 expense)", "danger")
    else:
        if create_category(g.user['id'], name, type_val):
            flash("新增個人分類成功！", "success")
        else:
            flash("抱歉，分類新增操作失敗，可能有系統問題。", "danger")
            
    return redirect(url_for('category.index'))

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """處理刪除分類的操作"""
    if delete_category(id, g.user['id']):
        flash("已成功清理該分類。", "success")
    else:
        flash("無法刪除。這可能是系統預設公用分類，或是內部產生了錯誤。", "danger")
    return redirect(url_for('category.index'))
