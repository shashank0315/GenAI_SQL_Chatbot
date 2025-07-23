import sqlite3

# Connect to your database
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Show columns in ad_sales
print("📋 Columns in ad_sales:")
cursor.execute("PRAGMA table_info(ad_sales)")
for row in cursor.fetchall():
    print("-", row[1])

# Show columns in total_sales
print("\n📋 Columns in total_sales:")
cursor.execute("PRAGMA table_info(total_sales)")
for row in cursor.fetchall():
    print("-", row[1])

conn.close()
