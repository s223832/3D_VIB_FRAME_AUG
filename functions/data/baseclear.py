import sqlite3

def baseclear(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()

    # Get the list of all tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    # Drop each table
    for table_name in tables:
        cur.execute(f"DROP TABLE IF EXISTS {table_name[0]};")

    con.commit()
    con.close()