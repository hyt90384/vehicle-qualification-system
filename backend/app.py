# --- backend/app.py ---
from flask import Flask, request, jsonify, render_template, redirect, url_for
from backend.database import db_session, init_db
from backend.models import Vehicle, QueryRecord
from datetime import datetime
import logging
import re
import os

# 設置日誌
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 獲取當前文件所在目錄的絕對路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
# 設置模板目錄的絕對路徑
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

# 車牌格式驗證
def is_valid_plate(plate):
    # 移除所有空格和連字符
    plate = plate.replace(' ', '').replace('-', '')
    # 台灣車牌格式：2-3個英文字母 + 4個數字
    pattern = r'^[A-Z]{2,3}\d{4}$'
    return bool(re.match(pattern, plate))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dmv')
def dmv():
    try:
        # 檢查資料庫是否已初始化
        try:
            # 獲取最近的查詢記錄
            recent_records = QueryRecord.query.order_by(QueryRecord.timestamp.desc()).limit(10).all()
        except Exception as e:
            logger.warning(f"QueryRecord table not initialized: {str(e)}")
            recent_records = []
            
        return render_template('dmv.html', recent_records=recent_records)
    except Exception as e:
        logger.error(f"Error in dmv route: {str(e)}")
        return "發生錯誤，請稍後再試", 500

@app.route('/dmv/add')
def dmv_add():
    return render_template('dmv_add.html')

@app.route('/dmv/manage')
def dmv_manage():
    try:
        vehicles = Vehicle.query.filter_by(has_maternity_pass=True).all()
        return render_template('dmv_manage.html', vehicles=vehicles)
    except Exception as e:
        logger.error(f"Error in dmv_manage route: {str(e)}")
        return "發生錯誤，請稍後再試", 500

@app.route('/dmv/check', methods=['POST'])
def dmv_check():
    try:
        license_plate = request.form.get('license_plate')
        if not license_plate:
            return "請輸入車牌號碼", 400
            
        vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
        
        # 記錄查詢
        record = QueryRecord(
            license_plate=license_plate,
            timestamp=datetime.now(),
            status='allowed' if vehicle and vehicle.has_maternity_pass and (not vehicle.maternity_pass_expiry or datetime.now().date() <= vehicle.maternity_pass_expiry) else 'forbidden'
        )
        db_session.add(record)
        db_session.commit()
        
        if vehicle and vehicle.has_maternity_pass and (not vehicle.maternity_pass_expiry or datetime.now().date() <= vehicle.maternity_pass_expiry):
            return render_template('dmv_check_result.html', 
                                vehicle=vehicle, 
                                status='allowed')
        else:
            return render_template('dmv_check_result.html', 
                                license_plate=license_plate, 
                                status='forbidden')
    except Exception as e:
        logger.error(f"Error in dmv_check route: {str(e)}")
        return "發生錯誤，請稍後再試", 500

@app.route('/police')
def police():
    return render_template('police.html')

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    try:
        license_plate = request.form.get('license_plate')
        owner_name = request.form.get('owner_name')
        id_number = request.form.get('id_number')
        pregnancy_date = datetime.strptime(request.form.get('pregnancy_date'), '%Y-%m-%d').date()
        has_pass = True if request.form.get('has_maternity_pass') == 'on' else False
        pass_type = request.form.get('maternity_pass_type')
        expiry = request.form.get('maternity_pass_expiry')

        if expiry:
            expiry_date = datetime.strptime(expiry, '%Y-%m-%d').date()
        else:
            expiry_date = None

        # 檢查車牌是否已存在
        exist = Vehicle.query.filter_by(license_plate=license_plate).first()
        if exist:
            return jsonify({'error': '車牌已被使用'}), 400

        new_vehicle = Vehicle(
            license_plate=license_plate,
            owner_name=owner_name,
            id_number=id_number,
            pregnancy_date=pregnancy_date,
            has_maternity_pass=has_pass,
            maternity_pass_type=pass_type,
            maternity_pass_expiry=expiry_date
        )
        db_session.add(new_vehicle)
        db_session.commit()
        
        return jsonify({
            'id': new_vehicle.id,
            'license_plate': new_vehicle.license_plate,
            'owner_name': new_vehicle.owner_name,
            'id_number': new_vehicle.id_number,
            'pregnancy_date': new_vehicle.pregnancy_date.strftime('%Y-%m-%d'),
            'maternity_pass_type': new_vehicle.maternity_pass_type,
            'maternity_pass_expiry': new_vehicle.maternity_pass_expiry.strftime('%Y-%m-%d') if new_vehicle.maternity_pass_expiry else None
        })
    except Exception as e:
        logger.error(f"Error in add_vehicle route: {str(e)}")
        db_session.rollback()
        return jsonify({'error': '發生錯誤，請稍後再試'}), 500

@app.route('/api/check_plate', methods=['POST'])
def check_plate():
    try:
        plate = request.json.get('plate')
        vehicle = Vehicle.query.filter_by(license_plate=plate).first()
        if vehicle and vehicle.has_maternity_pass and (not vehicle.maternity_pass_expiry or datetime.now().date() <= vehicle.maternity_pass_expiry):
            return jsonify({
                'status': 'allowed',
                'owner_name': vehicle.owner_name,
                'id_number': vehicle.id_number,
                'pregnancy_date': vehicle.pregnancy_date.strftime('%Y-%m-%d')
            })
        else:
            return jsonify({'status': 'forbidden'})
    except Exception as e:
        logger.error(f"Error in check_plate route: {str(e)}")
        return jsonify({'status': 'error', 'message': '發生錯誤，請稍後再試'}), 500

@app.route('/api/vehicle/<int:vehicle_id>')
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        return jsonify({
            'id': vehicle.id,
            'license_plate': vehicle.license_plate,
            'owner_name': vehicle.owner_name,
            'id_number': vehicle.id_number,
            'pregnancy_date': vehicle.pregnancy_date.strftime('%Y-%m-%d'),
            'maternity_pass_type': vehicle.maternity_pass_type,
            'maternity_pass_expiry': vehicle.maternity_pass_expiry.strftime('%Y-%m-%d') if vehicle.maternity_pass_expiry else None
        })
    return jsonify({'error': 'Vehicle not found'}), 404

@app.route('/update_vehicle', methods=['POST'])
def update_vehicle():
    try:
        vehicle_id = request.form.get('vehicle_id')
        vehicle = Vehicle.query.get(vehicle_id)
        
        if not vehicle:
            return "找不到車輛", 404
            
        vehicle.license_plate = request.form.get('license_plate')
        vehicle.owner_name = request.form.get('owner_name')
        vehicle.id_number = request.form.get('id_number')
        vehicle.pregnancy_date = datetime.strptime(request.form.get('pregnancy_date'), '%Y-%m-%d').date()
        vehicle.maternity_pass_type = request.form.get('maternity_pass_type')
        
        expiry = request.form.get('maternity_pass_expiry')
        if expiry:
            vehicle.maternity_pass_expiry = datetime.strptime(expiry, '%Y-%m-%d').date()
        else:
            vehicle.maternity_pass_expiry = None
            
        db_session.commit()
        
        # 返回更新後的車輛資料
        return jsonify({
            'id': vehicle.id,
            'license_plate': vehicle.license_plate,
            'owner_name': vehicle.owner_name,
            'id_number': vehicle.id_number,
            'pregnancy_date': vehicle.pregnancy_date.strftime('%Y-%m-%d'),
            'maternity_pass_type': vehicle.maternity_pass_type,
            'maternity_pass_expiry': vehicle.maternity_pass_expiry.strftime('%Y-%m-%d') if vehicle.maternity_pass_expiry else None
        })
    except Exception as e:
        logger.error(f"Error in update_vehicle route: {str(e)}")
        db_session.rollback()
        return jsonify({'error': '發生錯誤，請稍後再試'}), 500

@app.route('/api/search_vehicles')
def search_vehicles():
    try:
        license_plate = request.args.get('license_plate', '')
        id_number = request.args.get('id_number', '')
        owner_name = request.args.get('owner_name', '')
        
        logger.debug(f"Search parameters - license_plate: {license_plate}, id_number: {id_number}, owner_name: {owner_name}")
        
        # 先獲取所有車輛
        all_vehicles = Vehicle.query.filter_by(has_maternity_pass=True).all()
        logger.debug(f"Total vehicles in database: {len(all_vehicles)}")
        
        # 處理搜尋條件
        if license_plate:
            # 移除所有空格和連字符，並轉換為大寫
            license_plate = license_plate.replace(' ', '').replace('-', '').upper()
            logger.debug(f"Processed search license_plate: {license_plate}")
            
            # 過濾車輛
            filtered_vehicles = []
            for vehicle in all_vehicles:
                # 處理資料庫中的車牌號碼
                db_license_plate = vehicle.license_plate.replace(' ', '').replace('-', '').upper()
                logger.debug(f"Comparing - Search: {license_plate}, DB: {db_license_plate}")
                
                if license_plate == db_license_plate:
                    filtered_vehicles.append(vehicle)
            
            vehicles = filtered_vehicles
        else:
            vehicles = all_vehicles
            
        if id_number:
            # 移除所有空格並轉換為大寫
            id_number = id_number.replace(' ', '').upper()
            vehicles = [v for v in vehicles if v.id_number.replace(' ', '').upper() == id_number]
            
        if owner_name:
            vehicles = [v for v in vehicles if owner_name.lower() in v.owner_name.lower()]
            
        logger.debug(f"Found {len(vehicles)} vehicles")
        
        # 記錄找到的車輛資料
        for vehicle in vehicles:
            logger.debug(f"Vehicle found - ID: {vehicle.id}, License: {vehicle.license_plate}, Owner: {vehicle.owner_name}")
        
        return jsonify([{
            'id': vehicle.id,
            'license_plate': vehicle.license_plate,
            'owner_name': vehicle.owner_name,
            'id_number': vehicle.id_number,
            'pregnancy_date': vehicle.pregnancy_date.strftime('%Y-%m-%d'),
            'maternity_pass_type': vehicle.maternity_pass_type,
            'maternity_pass_expiry': vehicle.maternity_pass_expiry.strftime('%Y-%m-%d') if vehicle.maternity_pass_expiry else None
        } for vehicle in vehicles])
    except Exception as e:
        logger.error(f"Error in search_vehicles: {str(e)}")
        return jsonify([])

@app.route('/api/delete_vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle_api(vehicle_id):
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({'error': '找不到車輛'}), 404
            
        db_session.delete(vehicle)
        db_session.commit()
        return jsonify({'message': '刪除成功'})
    except Exception as e:
        logger.error(f"Error in delete_vehicle_api: {str(e)}")
        db_session.rollback()
        return jsonify({'error': '發生錯誤，請稍後再試'}), 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    try:
        init_db()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        raise