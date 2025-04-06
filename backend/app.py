from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__, static_folder='.')
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type"]}})

# 数据库初始化
def init_db():
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    
    # 创建用户表
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建用药记录表
    c.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            schedule TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_logged TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 创建预约表
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            doctor_name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            type TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # 创建健康记录表
    c.execute('''
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            value TEXT NOT NULL,
            date TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# 用户相关 API
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or not all(k in data for k in ['username', 'password', 'email']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                 (data['username'], data['password'], data['email']))
        conn.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 400
    finally:
        conn.close()

@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.json
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    c.execute('SELECT id, username FROM users WHERE username = ? AND password = ?',
             (data['username'], data['password']))
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({'id': user[0], 'username': user[1]}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# 用药记录相关 API
@app.route('/api/medications', methods=['GET'])
def get_medications():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    c.execute('SELECT * FROM medications WHERE user_id = ?', (user_id,))
    medications = [dict(zip([col[0] for col in c.description], row))
                  for row in c.fetchall()]
    conn.close()
    return jsonify(medications)

@app.route('/api/medications', methods=['POST'])
def add_medication():
    data = request.json
    if not data or not all(k in data for k in ['userId', 'name', 'dosage', 'schedule']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO medications (user_id, name, dosage, schedule)
        VALUES (?, ?, ?, ?)
    ''', (data['userId'], data['name'], data['dosage'], data['schedule']))
    conn.commit()
    medication_id = c.lastrowid
    conn.close()
    
    return jsonify({'id': medication_id, **data}), 201

@app.route('/api/medications/<int:medication_id>/log', methods=['POST'])
def log_dose(medication_id):
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    c.execute('''
        UPDATE medications 
        SET last_logged = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (medication_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Dose logged successfully'})

@app.route('/api/medications/<int:medication_id>', methods=['DELETE'])
def delete_medication(medication_id):
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    c.execute('DELETE FROM medications WHERE id = ?', (medication_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Medication deleted successfully'})

# 预约相关 API
@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    c.execute('SELECT * FROM appointments WHERE user_id = ?', (user_id,))
    appointments = [dict(zip([col[0] for col in c.description], row))
                   for row in c.fetchall()]
    conn.close()
    return jsonify(appointments)

@app.route('/api/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    if not data or not all(k in data for k in ['userId', 'doctorName', 'date', 'time', 'type']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO appointments (user_id, doctor_name, date, time, type, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['userId'], data['doctorName'], data['date'], data['time'], 
          data['type'], data.get('notes', '')))
    conn.commit()
    appointment_id = c.lastrowid
    conn.close()
    
    return jsonify({'id': appointment_id, **data}), 201

# 健康记录相关 API
@app.route('/api/health-records', methods=['GET'])
def get_health_records():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    c.execute('SELECT * FROM health_records WHERE user_id = ?', (user_id,))
    records = [dict(zip([col[0] for col in c.description], row))
              for row in c.fetchall()]
    conn.close()
    return jsonify(records)

@app.route('/api/health-records', methods=['POST'])
def add_health_record():
    data = request.json
    if not data or not all(k in data for k in ['userId', 'type', 'value', 'date']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect('healthsync.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO health_records (user_id, type, value, date, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['userId'], data['type'], data['value'], data['date'], 
          data.get('notes', '')))
    conn.commit()
    record_id = c.lastrowid
    conn.close()
    
    return jsonify({'id': record_id, **data}), 201

# 静态文件路由
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    init_db()  # 初始化数据库
    app.run(debug=True) 