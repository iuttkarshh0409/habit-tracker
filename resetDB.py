from db.db_utils import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("DELETE FROM logs;")
cursor.execute("DELETE FROM habits;")
cursor.execute("DELETE FROM reflection_notes;")

# Reset auto-increment counters
cursor.execute("DELETE FROM sqlite_sequence;")

conn.commit()
conn.close()

print("Database reset complete.")
