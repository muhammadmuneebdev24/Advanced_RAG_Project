from database.Connection import get_connection


def insert_pdf(file_name, file_hash):

    conn = get_connection()

    cursor = conn.cursor()


    query = """
    INSERT INTO pdf_files
    (file_name, file_hash, status)
    VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (file_name, file_hash, "PROCESSING")
    )

    conn.commit()

    cursor.close()

    conn.close()