import sqlite3

def run_query(sql_query, db_path="ecommerce.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)

        columns = [description[0] for description in cursor.description]

        rows = cursor.fetchall()

        result = [dict(zip(columns, row)) for row in rows]

        conn.close()
        return result

    except Exception as e:
        return {"error": str(e)}

def show_columns(table_name, db_path="ecommerce.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    conn.close()
    return columns
