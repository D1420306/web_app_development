import os
from flask import Flask
from config import Config

def create_app(test_config=None):
    """
    Flask Application Factory
    建立與設定 Flask App，並完成所有初始化。
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    if test_config is None:
        # 在非測試情況下，嘗試載入 instance 的設定檔（如果存在）
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 目錄存在以放置 SQLite DB
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 負責資料庫建立與初始化
    from app.models.db import init_db
    init_db()

    # 掛載註冊的 Blueprints
    from app.routes import register_routes
    register_routes(app)

    return app
