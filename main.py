from backend.app import app
from backend.database import init_db

if __name__ == '__main__':
    # 初始化資料庫
    init_db()
    app.run(debug=True) 