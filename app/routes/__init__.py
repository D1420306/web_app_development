def register_routes(app):
    """
    接收 Flask app 實例，負責註冊並掛載所有的 Blueprints
    """
    from . import auth, expense, category, admin

    app.register_blueprint(auth.bp)
    app.register_blueprint(expense.bp)
    app.register_blueprint(category.bp)
    app.register_blueprint(admin.bp)
