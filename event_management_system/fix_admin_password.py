"""Fix default admin password hash"""
import bcrypt
import psycopg2

pw = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode()
conn = psycopg2.connect(
    host='db.pmmiddrxjkfqkmldmbwf.supabase.co',
    user='postgres',
    password='Shannu@2430',
    database='postgres',
    port=5432
)
cur = conn.cursor()
cur.execute(
    "UPDATE admin SET password_hash = %s WHERE email = %s",
    (pw, 'admin@campus.edu')
)
conn.commit()
print(f"Updated admin password hash. Rows affected: {cur.rowcount}")
cur.close()
conn.close()
