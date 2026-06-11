from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EXPORT_DIR = BASE_DIR / "exports"
DB_PATH = DATA_DIR / "netmonitor.db"

DATA_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

APP_NAME = "NetUsage Monitor"
REFRESH_INTERVAL = 1
FLUSH_INTERVAL = 60
MINUTE_LOG_RETENTION_DAYS = 7
MAX_EXPORT_FILES = 10
