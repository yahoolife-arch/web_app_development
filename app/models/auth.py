import sqlite3
from typing import Optional, Dict

DATABASE_PATH = "instance/database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class User:
    @staticmethod
    def create(username: str, password_hash: str) -> Optional[int]:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id: int) -> Optional[Dict]:
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_username(username: str) -> Optional[Dict]:
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        return dict(user) if user else None
