# 車輛資格系統

這是一個用於管理和查詢車輛孕婦通行證資格的系統。

## 功能特點

- 車輛資格查詢
- 孕婦通行證管理
- 查詢記錄追蹤
- 警察執法查詢介面

## 系統需求

- Python 3.8 或更高版本
- SQLite3

## 安裝步驟

1. 克隆專案：
```bash
git clone [repository-url]
cd vehicle-qualification-system
```

2. 創建虛擬環境：
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 初始化資料庫：
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. 設定環境變數：
創建 `.env` 檔案並設定以下變數：
```
FLASK_APP=main.py
FLASK_ENV=development
DATABASE_URL=sqlite:///database/vehicle.db
SECRET_KEY=your-secret-key-here
```

## 運行系統

開發環境：
```bash
python main.py
```

生產環境：
```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## API 文檔

### 車輛查詢
- GET `/api/vehicle/<id>` - 獲取特定車輛資訊
- POST `/api/check_plate` - 檢查車牌資格
- GET `/api/search_vehicles` - 搜尋車輛

### 管理介面
- POST `/add_vehicle` - 新增車輛
- POST `/update_vehicle` - 更新車輛資訊
- DELETE `/api/delete_vehicle/<id>` - 刪除車輛

## 安全性考慮

- 所有 API 請求都需要進行身份驗證
- 敏感資料（如身分證號碼）已加密存儲
- 系統記錄所有查詢操作以供審計

## 維護和支援

如有任何問題或建議，請聯繫系統管理員。 