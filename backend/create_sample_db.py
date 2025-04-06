import sqlite3
from datetime import datetime, timedelta

def create_sample_database():
    # 连接到数据库（如果不存在则创建）
    conn = sqlite3.connect('healthsync_sample.db')
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 创建药物表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        dosage TEXT NOT NULL,
        schedule TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_logged TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # 创建预约表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        record_type TEXT NOT NULL,
        value TEXT NOT NULL,
        unit TEXT,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notes TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # 插入示例用户
    cursor.execute('''
    INSERT INTO users (username, password, email, created_at)
    VALUES (?, ?, ?, ?)
    ''', ('demo_user', 'demo123', 'demo@example.com', datetime.now()))

    # 获取用户ID
    user_id = cursor.lastrowid

    # 插入示例药物
    medications = [
        ('Metformin', '500mg', 'Daily 8:00 AM & 8:00 PM'),
        ('Insulin', '10 units', 'Before meals'),
        ('Aspirin', '81mg', 'Once daily')
    ]
    
    for med in medications:
        cursor.execute('''
        INSERT INTO medications (user_id, name, dosage, schedule, created_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, med[0], med[1], med[2], datetime.now()))

    # 插入示例预约
    appointments = [
        ('Dr. Smith', '2024-04-15', '10:00 AM', 'Regular Checkup', 'Annual physical examination'),
        ('Dr. Johnson', '2024-04-20', '2:30 PM', 'Specialist Consultation', 'Follow-up for diabetes management')
    ]
    
    for apt in appointments:
        cursor.execute('''
        INSERT INTO appointments (user_id, doctor_name, date, time, type, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, apt[0], apt[1], apt[2], apt[3], apt[4], datetime.now()))

    # 插入示例健康记录
    health_records = [
        ('Blood Sugar', '95', 'mg/dL', 'Fasting blood sugar reading'),
        ('Blood Pressure', '120/80', 'mmHg', 'Morning reading'),
        ('Weight', '70', 'kg', 'Weekly measurement')
    ]
    
    for record in health_records:
        cursor.execute('''
        INSERT INTO health_records (user_id, record_type, value, unit, notes, recorded_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, record[0], record[1], record[2], record[3], datetime.now()))

    # 提交更改并关闭连接
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_sample_database()
    print("Sample database created successfully!") 