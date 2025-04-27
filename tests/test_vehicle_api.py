import json
from datetime import datetime

def test_add_vehicle(client):
    """測試新增車輛"""
    data = {
        'license_plate': 'XYZ-5678',
        'owner_name': '測試用戶2',
        'id_number': 'B123456789',
        'pregnancy_date': '2024-03-20',
        'has_maternity_pass': 'true',
        'maternity_pass_type': '一般',
        'maternity_pass_expiry': '2024-12-31'
    }
    
    response = client.post('/add_vehicle', data=data)
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['license_plate'] == 'XYZ-5678'

def test_check_plate(client, test_vehicle):
    """測試車牌查詢功能"""
    data = {'plate': test_vehicle.license_plate}
    response = client.post('/api/check_plate', json=data)
    
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['status'] == 'allowed'

def test_get_vehicle(client, test_vehicle):
    """測試獲取車輛資訊功能"""
    response = client.get(f'/api/vehicle/{test_vehicle.id}')
    
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['license_plate'] == test_vehicle.license_plate

def test_search_vehicles(client, test_vehicle):
    """測試搜尋車輛功能"""
    response = client.get(f'/api/search_vehicles?query={test_vehicle.license_plate}')
    
    assert response.status_code == 200
    response_data = response.get_json()
    assert len(response_data) > 0
    assert response_data[0]['license_plate'] == test_vehicle.license_plate

def test_update_vehicle(client, test_vehicle):
    """測試更新車輛資訊功能"""
    data = {
        'vehicle_id': test_vehicle.id,
        'owner_name': '更新後的用戶',
        'maternity_pass_type': '特殊',
        'license_plate': test_vehicle.license_plate,
        'id_number': test_vehicle.id_number,
        'pregnancy_date': test_vehicle.pregnancy_date.strftime('%Y-%m-%d'),
        'maternity_pass_expiry': test_vehicle.maternity_pass_expiry.strftime('%Y-%m-%d') if test_vehicle.maternity_pass_expiry else None
    }
    
    response = client.post('/update_vehicle', data=data)
    
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['owner_name'] == '更新後的用戶'
    assert response_data['maternity_pass_type'] == '特殊'

def test_invalid_plate_query(client):
    """測試無效車牌查詢"""
    data = {'plate': 'INVALID-PLATE'}
    response = client.post('/api/check_plate', json=data)
    
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['status'] == 'forbidden' 