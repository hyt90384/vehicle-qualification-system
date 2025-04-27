from backend.app import app
from backend.database import init_db
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

if __name__ == '__main__':
    # 初始化資料庫
    init_db()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 