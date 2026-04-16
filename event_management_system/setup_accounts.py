"""
Setup Admin and Event Organiser accounts with proper bcrypt password hashes
"""
import bcrypt
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def create_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

conn = psycopg2.connect(
    host=os.getenv('POSTGRES_HOST'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    database=os.getenv('POSTGRES_DB'),
    port=int(os.getenv('POSTGRES_PORT', 5432))
)
cur = conn.cursor()

# ========== ADMIN ACCOUNT ==========
admin_email = 'admin@campus.edu'
admin_password = 'Admin@1234'
admin_hash = create_hash(admin_password)

# Delete existing and re-insert to ensure clean state
cur.execute("DELETE FROM admin WHERE email = %s", (admin_email,))
cur.execute("""
    INSERT INTO admin (name, email, password_hash, role, is_active)
    VALUES (%s, %s, %s, %s, TRUE)
""", ('Super Admin', admin_email, admin_hash, 'super_admin'))

print(f"[+] Admin account created")
print(f"    Email: {admin_email}")
print(f"    Password: {admin_password}")

# ========== EVENT ORGANISER ACCOUNT ==========
organiser_email = 'organiser@campus.edu'
organiser_password = 'Organiser@1234'
organiser_hash = create_hash(organiser_password)

# Delete existing and re-insert
cur.execute("DELETE FROM event_organisers WHERE email = %s", (organiser_email,))
cur.execute("""
    INSERT INTO event_organisers (name, email, password_hash, department, contact_number, is_active)
    VALUES (%s, %s, %s, %s, %s, TRUE)
""", ('Event Organiser', organiser_email, organiser_hash, 'Computer Science', '9876543210'))

print(f"\n[+] Event Organiser account created")
print(f"    Email: {organiser_email}")
print(f"    Password: {organiser_password}")

conn.commit()
cur.close()
conn.close()

print("\n[✓] All accounts set up successfully!")
