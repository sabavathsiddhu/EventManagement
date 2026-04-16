import pymysql

configs = [
    {'password': None, 'desc': 'None'},
    {'password': '', 'desc': 'Empty string'},
    {'password': 'root', 'desc': 'root'},
]

for cfg in configs:
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=cfg['password'],
            database='event_management_system',
            charset='utf8mb4'
        )
        print(f"✓ Connected with password={cfg['desc']}")
        conn.close()
        break
    except Exception as e:
        error_msg = str(e)[:100]
        print(f"✗ Failed with password={cfg['desc']}: {error_msg}")
