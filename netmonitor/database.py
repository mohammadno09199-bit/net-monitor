import sqlite3
from datetime import datetime, timedelta
from netmonitor.config import DB_PATH, MINUTE_LOG_RETENTION_DAYS


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

    def insert_minute_log(self, timestamp: str, upload_bytes: int, download_bytes: int):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO minute_logs (timestamp, upload_bytes, download_bytes)
                VALUES (?, ?, ?)
            """, (timestamp, upload_bytes, download_bytes))
            conn.commit()

    def upsert_daily(self, date_str: str, upload_bytes: int, download_bytes: int):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO daily_summary (date, total_upload_bytes, total_download_bytes)
                VALUES (?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                    total_upload_bytes = total_upload_bytes + excluded.total_upload_bytes,
                    total_download_bytes = total_download_bytes + excluded.total_download_bytes
            """, (date_str, upload_bytes, download_bytes))
            conn.commit()

    def get_today_stats(self, date_str: str):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT total_upload_bytes, total_download_bytes
                FROM daily_summary
                WHERE date = ?
            """, (date_str,))
            row = cursor.fetchone()
            return row if row else (0, 0)

    def get_recent_minute_logs(self, days: int = 7):
        cutoff = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT timestamp, upload_bytes, download_bytes
                FROM minute_logs
                WHERE timestamp >= ?
                ORDER BY timestamp ASC
            """, (cutoff,))
            return cursor.fetchall()

    def cleanup_old_minute_logs(self):
        cutoff = (datetime.now() - timedelta(days=MINUTE_LOG_RETENTION_DAYS)).isoformat(timespec="seconds")
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM minute_logs
                WHERE timestamp < ?
            """, (cutoff,))
            conn.commit()
