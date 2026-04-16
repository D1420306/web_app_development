import os
from dotenv import load_dotenv

# 讀取 .env 中的變數到 os.environ
load_dotenv()

class Config:
    # 預設一組開發用的 Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret')
    
    # SQLite 資料庫位置預設在此
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')
