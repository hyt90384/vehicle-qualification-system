from datetime import datetime, timedelta
from backend.models import QueryRecord
from backend.database import db_session
import time

def test_create_query_record(client, test_vehicle):
    """測試創建查詢記錄"""
    # 確保測試車輛有有效的通行證
    test_vehicle.has_maternity_pass = True
    test_vehicle.maternity_pass_expiry = datetime.now().date() + timedelta(days=30)
    db_session.commit()
    
    data = {'plate': test_vehicle.license_plate}
    response = client.post('/api/check_plate',
                         json=data,
                         content_type='application/json')
    
    assert response.status_code == 200
    
    # 驗證是否創建了查詢記錄
    record = QueryRecord.query.filter_by(license_plate=test_vehicle.license_plate).first()
    assert record is not None
    assert record.status == 'allowed'

def test_query_record_timestamp(client, test_query_record):
    """測試查詢記錄的時間戳"""
    assert isinstance(test_query_record.timestamp, datetime)
    assert (datetime.now() - test_query_record.timestamp) < timedelta(minutes=1)

def test_invalid_plate_query_record(client):
    """測試無效車牌查詢的記錄"""
    # 使用符合格式但無效的車牌
    data = {'plate': 'ABC1234'}
    response = client.post('/api/check_plate',
                         json=data,
                         content_type='application/json')
    
    assert response.status_code == 200
    
    # 驗證查詢記錄
    record = QueryRecord.query.filter_by(license_plate='ABC1234').first()
    assert record is not None
    assert record.status == 'forbidden'

def test_multiple_queries(client, test_vehicle):
    """測試多次查詢記錄"""
    # 確保測試車輛有有效的通行證
    test_vehicle.has_maternity_pass = True
    test_vehicle.maternity_pass_expiry = datetime.now().date() + timedelta(days=30)
    db_session.commit()
    
    # 執行多次查詢，每次查詢之間添加短暫延遲
    for _ in range(3):
        data = {'plate': test_vehicle.license_plate}
        response = client.post('/api/check_plate',
                           json=data,
                           content_type='application/json')
        assert response.status_code == 200
        time.sleep(0.1)  # 添加 0.1 秒延遲
    
    # 驗證查詢記錄數量並按時間戳降序排序
    records = QueryRecord.query.filter_by(license_plate=test_vehicle.license_plate).order_by(QueryRecord.timestamp.desc()).all()
    assert len(records) == 3
    
    # 驗證記錄順序
    timestamps = [record.timestamp for record in records]
    assert timestamps == sorted(timestamps, reverse=True), f"時間戳未正確排序：\n實際：{timestamps}\n期望：{sorted(timestamps, reverse=True)}" 