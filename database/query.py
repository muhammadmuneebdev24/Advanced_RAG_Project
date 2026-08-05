from database.Connection import get_connection

def hash_exist(hashing):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
            SELECT 1
            FROM pdf_files
            WHERE file_hash = %s
            """

    cursor.execute(query , (hashing,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is not None:
        return True
    else:
        return False

def insert_pdf(file_name, file_hash):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
            INSERT INTO pdf_files
            (file_name,
             file_hash,
             status)
            VALUES (%s,%s,%s)"""
    cursor.execute(query,
                   (file_name,file_hash,"PROCESSING"))

    conn.commit()
    cursor.close()
    conn.close()

def update_status(file_hash, status):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE pdf_files
    SET
        status = %s,
        updated_at = CURRENT_TIMESTAMP
    WHERE file_hash = %s
    """

    cursor.execute(
        query,
        (status, file_hash)
    )

    conn.commit()
    cursor.close()
    conn.close()