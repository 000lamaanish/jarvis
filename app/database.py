
import sqlite3
from pathlib import Path

# Store the database inside the C:\jarvis project folder
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "jarvis_memory.db"


def initialize_database():
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()
    finally:
        connection.close()



def save_message(role, message):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO conversations (role, message) VALUES (?, ?)",
            (role, message)
        )

        connection.commit()
    finally:
        connection.close()


def get_recent_messages(limit=10):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT role, message
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        # The query returns newest first; reverse to restore conversation order.
        rows.reverse()

        return [
            {"role": role, "content": message}
            for role, message in rows
        ]
    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"JARVIS memory database created at: {DB_PATH}")
