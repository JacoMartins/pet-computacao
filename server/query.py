import sqlite3

conn = sqlite3.connect('database.db')

with conn:
    cur = conn.cursor()
    cur.execute("""SELECT * FROM sentido WHERE id >= 0 LIMIT 10;""")
    rows = cur.fetchall()
    for row in rows:
        print(row)