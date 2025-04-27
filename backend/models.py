from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from backend.database import get_query_property

Base = declarative_base()

class Vehicle(Base):
    __tablename__ = 'vehicles'
    
    id = Column(Integer, primary_key=True)
    license_plate = Column(String(20), unique=True, nullable=False)
    owner_name = Column(String(100), nullable=False)
    id_number = Column(String(10), nullable=False)  # 身分證字號
    pregnancy_date = Column(Date, nullable=False)   # 懷孕時間
    has_maternity_pass = Column(Boolean, default=False)
    maternity_pass_type = Column(String(50))
    maternity_pass_expiry = Column(Date)

    # 添加查詢介面
    query = get_query_property()

class QueryRecord(Base):
    __tablename__ = 'query_records'
    
    id = Column(Integer, primary_key=True)
    license_plate = Column(String(10), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)  # 'allowed' or 'forbidden'
