import sqlite3

def check_database():
    # 连接到数据库
    conn = sqlite3.connect('healthsync.db')
    cursor = conn.cursor()
    
    # 获取所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n=== 数据库表结构 ===")
    for table in tables:
        table_name = table[0]
        print(f"\n表名: {table_name}")
        # 获取表结构
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print("列信息:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # 获取表中的数据
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        print(f"\n数据行数: {len(rows)}")
        if rows:
            print("数据示例:")
            for row in rows[:3]:  # 只显示前3行
                print(f"  {row}")
    
    conn.close()

if __name__ == "__main__":
    check_database() 