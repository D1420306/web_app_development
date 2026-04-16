import sqlite3
import os

# 根據目前檔案的路徑，推導到 instance/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DATABASE_PATH = os.path.join(INSTANCE_DIR, 'database.db')

def get_db():
    """
    取得 SQLite 資料庫連線
    回傳：sqlite3.Connection
    """
    db = sqlite3.connect(DATABASE_PATH)
    
    # 讓查詢出的結果可以使用 dictionary index 存取名稱 (如 row['id'])
    db.row_factory = sqlite3.Row
    
    # 啟用 Foreign Key 約束
    db.execute('PRAGMA foreign_keys = ON')
    
    return db

def init_db():
    """
    如果資料庫與目錄不存在，則從 schema 建立資料庫。
    (實務中可於 Flask init 時或單獨管理使用)
    """
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)
        
    db = get_db()
    with open(os.path.join(BASE_DIR, 'database', 'schema.sql'), 'r', encoding='utf-8') as f:
        db.executescript(f.read())
    db.commit()
    db.close()
