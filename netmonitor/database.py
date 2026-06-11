import sqlite3
from .config import DB_PATH

class DatabaseManager:
    def __init__(self):
        self.init_db()

    def init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS minute_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    upload_bytes INTEGER NOT NULL,
                    download_bytes INTEGER NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_summary (
                    date TEXT PRIMARY KEY,
                    total_upload_bytes INTEGER NOT NULL,
                    total_download_bytes INTEGER NOT NULL
                )
            """)
            conn.commit()

    def upsert_daily(self, date_str, up, down):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO daily_summary (date, total_upload_bytes, total_download_bytes)
                VALUES (?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                    total_upload_bytes = total_upload_bytes + excluded.total_upload_bytes,
                    total_download_bytes = total_download_bytes + excluded.total_download_bytes
            """, (date_str, up, down))
            conn.commit()

    def get_today_stats(self, date_str):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT total_upload_bytes, total_download_bytes FROM daily_summary WHERE date = ?", (date_str,))
            row = cursor.fetchone()
            return row if row else (0, 0)
