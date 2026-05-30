import sqlite3

conn = sqlite3.connect("data/personal_assistant.db")

cursor = conn.cursor()

print("\n=== TASKS ===")
cursor.execute("SELECT * FROM tasks")
for row in cursor.fetchall():
    print(row)

print("\n=== NOTES ===")
cursor.execute("SELECT * FROM notes")
for row in cursor.fetchall():
    print(row)

conn.close()