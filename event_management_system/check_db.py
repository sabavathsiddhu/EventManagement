import psycopg2
import socket

host = 'db.pmmiddrxjkfqkmldmbwf.supabase.co'

# Check what addresses DNS resolves to
print("DNS Resolution:")
try:
    results = socket.getaddrinfo(host, 5432)
    for r in results:
        print(f"  Family={r[0]}, Address={r[4]}")
except Exception as e:
    print(f"  DNS error: {e}")

# Try connecting with IPv6 resolved address directly
print("\nTrying direct connection...")
try:
    conn = psycopg2.connect(
        host=host,
        user='postgres',
        password='Shannu@2430',
        database='postgres',
        port=5432,
        connect_timeout=15
    )
    print("Connection SUCCESS!")
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables:", tables)
    cur.close()
    conn.close()
except Exception as e:
    print(f"Connection FAILED: {e}")

# Try with the pooler connection
print("\nTrying pooler connection (port 6543)...")
try:
    conn = psycopg2.connect(
        host='aws-0-ap-south-1.pooler.supabase.com',
        user='postgres.pmmiddrxjkfqkmldmbwf',
        password='Shannu@2430',
        database='postgres',
        port=6543,
        connect_timeout=15
    )
    print("Pooler Connection SUCCESS!")
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables:", tables)
    cur.close()
    conn.close()
except Exception as e:
    print(f"Pooler connection FAILED: {e}")
