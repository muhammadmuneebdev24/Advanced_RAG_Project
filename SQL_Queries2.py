from database.Connection import get_connection

def update (hash ,status):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
           """