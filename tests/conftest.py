import os
import tempfile
import pytest
from backend.app import app
from backend.database import init_db, db_session
from backend.models import Vehicle, QueryRecord, Base
from datetime import datetime, timedelta
import uuid
import random
import string

@pytest.fixture
def client():
    """建立測試用的 Flask 客戶端"""
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            # 確保資料庫表格被正確創建
            Base.metadata.drop_all(bind=db_session.get_bind())
            Base.metadata.create_all(bind=db_session.get_bind())
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)
    db_session.remove()

@pytest.fixture
def test_vehicle(client):
    """建立測試用的車輛資料"""
    # 生成符合格式的車牌號碼：2-3個英文字母 + 4個數字
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=4))
    license_plate = f'{letters}{numbers}'
    
    vehicle = Vehicle(
        license_plate=license_plate,
        owner_name='測試用戶',
        id_number='A123456789',
        pregnancy_date=datetime.now().date(),
        has_maternity_pass=True,
        maternity_pass_type='一般',
        maternity_pass_expiry=datetime.now().date() + timedelta(days=30)
    )
    db_session.add(vehicle)
    db_session.commit()
    return vehicle

@pytest.fixture
def test_query_record(client, test_vehicle):
    """建立測試用的查詢記錄"""
    record = QueryRecord(
        license_plate=test_vehicle.license_plate,
        timestamp=datetime.now(),
        status='allowed'
    )
    db_session.add(record)
    db_session.commit()
    return record 