import psycopg2

try:
    conn = psycopg2.connect(
        host='2406:da18:243:740f:8162:d5ee:3b:adb8',  # IPv6 address directly
        user='postgres',
        password='Shannu@2430',
        database='postgres',
        port=5432,
        connect_timeout=15
    )
    print("Connection SUCCESS with IPv6!")
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables:", tables)
    conn.close()
except Exception as e:
    print(f"Connection FAILED: {e}")
