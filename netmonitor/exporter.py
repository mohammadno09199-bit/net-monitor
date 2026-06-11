import csv
from datetime import datetime
from netmonitor.config import EXPORT_DIR, MAX_EXPORT_FILES


def export_logs_to_csv(logs):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = EXPORT_DIR / f"netusage_export_{timestamp}.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "upload_bytes", "download_bytes"])
        writer.writerows(logs)

    cleanup_old_exports()
    return file_path


def cleanup_old_exports():
    files = sorted(
        EXPORT_DIR.glob("netusage_export_*.csv"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    for old_file in files[MAX_EXPORT_FILES:]:
        old_file.unlink(missing_ok=True)
