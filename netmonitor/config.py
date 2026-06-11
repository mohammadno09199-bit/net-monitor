from pathlib import Path

# این فایل در netmonitor/ قرار دارد
# پس BASE_DIR می‌شود یک پوشه بالاتر (روت پروژه)
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
EXPORT_DIR = BASE_DIR / "exports"
DB_PATH = DATA_DIR / "netmonitor.db"

# ساخت پوشه‌ها
DATA_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)
