import sqlite3

DB_NAME = "memory.db"


def create_memory_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history(
        username TEXT,
        role TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_message(username, role, message):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_history
        VALUES (?, ?, ?)
        """,
        (username, role, message)
    )

    conn.commit()
    conn.close()


def load_messages(username):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM chat_history
        WHERE username=?
        """,
        (username,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "role": row[0],
            "content": row[1]
        }
        for row in rows
    ]


def clear_messages(username):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM chat_history
        WHERE username=?
        """,
        (username,)
    )

    conn.commit()
    conn.close()