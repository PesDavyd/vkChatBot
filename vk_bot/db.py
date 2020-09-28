import sqlite3

db = sqlite3.connect('users.db')
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id VARCHAR(50) PRIMARY KEY,
        status INTEGER,
        have INTEGER
    );
''')

db.commit()

array = cursor.execute("""
    SELECT * FROM users
""").fetchall()

for i in array:
    for j in i:
        print(j)
