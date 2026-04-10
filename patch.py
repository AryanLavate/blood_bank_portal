import MySQLdb

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
cursor = conn.cursor()

def add_col(table, col, defn):
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {defn}")
        print(f"Added {col} to {table}")
    except Exception as e:
        print(f"Skipped {col} in {table}: {e}")

add_col('blood_requests', 'status', "VARCHAR(20) DEFAULT 'Open'")
add_col('blood_requests', 'city', "VARCHAR(100)")
add_col('blood_requests', 'urgency', "VARCHAR(20) DEFAULT 'Normal'")
add_col('blood_requests', 'created_at', "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

add_col('organ_requests', 'status', "VARCHAR(20) DEFAULT 'Open'")
add_col('organ_requests', 'city', "VARCHAR(100)")
add_col('organ_requests', 'urgency', "VARCHAR(20) DEFAULT 'Normal'")
add_col('organ_requests', 'notes', "TEXT")
add_col('organ_requests', 'created_at', "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

add_col('users', 'city', "VARCHAR(100)")
add_col('users', 'availability_status', "VARCHAR(20) DEFAULT 'Available'")
add_col('users', 'is_verified', "TINYINT(1) DEFAULT 0")
add_col('users', 'organ_donor', "TINYINT(1) DEFAULT 0")
add_col('users', 'created_at', "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

add_col('donations', 'donation_type', "VARCHAR(20) DEFAULT 'Blood'")
add_col('donations', 'donation_date', "DATE")

add_col('hospitals', 'city', "VARCHAR(100)")
add_col('hospitals', 'is_verified', "TINYINT(1) DEFAULT 0")
add_col('hospitals', 'created_at', "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

conn.commit()
print("Done")
