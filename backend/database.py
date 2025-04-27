from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import logging

# 設置日誌
logger = logging.getLogger(__name__)

# 確保資料庫目錄存在
db_dir = os.path.join(os.path.dirname(__file__), '..', 'database')
os.makedirs(db_dir, exist_ok=True)

# 資料庫檔案路徑
db_path = os.path.join(db_dir, "vehicle.db")

# 創建 SQLite 資料庫 Engine
engine = create_engine(f'sqlite:///{db_path}', connect_args={"check_same_thread": False})

# 創建 session，用於操作資料庫
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# 初始化資料庫（創建表）
def init_db():
    try:
        from . import models
        # 創建所有表
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

# 提供查詢介面
def get_query_property():
    return db_session.query_property()
