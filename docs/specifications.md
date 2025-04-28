# 孕婦停車優惠系統規格文件

## 1. 系統架構

### 1.1 整體架構
- 前端：React.js網頁應用程式
- 後端：ASP.NET Core Web API
- 資料庫：Microsoft SQL Server
- 快取：Redis
- 訊息佇列：RabbitMQ

### 1.2 系統元件
- 醫院資料整合模組
- 監理站API整合模組
- 車輛綁定管理模組
- 停車場驗證模組
- 使用者認證授權模組

## 2. API規格

### 2.1 醫院端API
```
POST /api/hospital/pregnant-woman
Content-Type: application/json

{
    "id": "string",
    "name": "string",
    "idNumber": "string",
    "handbookNumber": "string",
    "hospitalId": "string",
    "checkDate": "datetime"
}
```

### 2.2 孕婦端API
```
GET /api/vehicle/owner/{idNumber}
GET /api/binding/status/{handbookNumber}
POST /api/binding/create
PUT /api/binding/update
```

### 2.3 停車場端API
```
GET /api/validation/vehicle/{plateNumber}
```

## 3. 資料庫設計

### 3.1 主要資料表
- PregnantWoman
- Vehicle
- Binding
- Hospital
- ParkingLot

### 3.2 資料表關聯
- PregnantWoman 1:1 Binding
- Vehicle 1:1 Binding
- Hospital 1:N PregnantWoman
- ParkingLot N:N Vehicle

## 4. 安全性設計

### 4.1 認證機制
- JWT Token認證
- OAuth 2.0整合
- API Key驗證

### 4.2 資料加密
- 個人資料加密存儲
- 傳輸層加密
- 敏感資料遮罩

## 5. 監控與日誌

### 5.1 系統監控
- 效能監控
- 錯誤追蹤
- 使用量統計

### 5.2 日誌記錄
- 操作日誌
- 錯誤日誌
- 安全日誌 