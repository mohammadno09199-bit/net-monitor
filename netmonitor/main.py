import time
from datetime import date
from rich.live import Live
from .database import DatabaseManager
from .monitor import NetMonitor
from .ui import render_dashboard

def main():
    db = DatabaseManager()
    monitor = NetMonitor()
    
    session_up = 0
    session_down = 0
    interval = 1

    with Live(refresh_per_second=4, screen=False) as live:
        try:
            while True:
                up_delta, down_delta, up_speed, down_speed = monitor.get_speed(interval)
                
                session_up += up_delta
                session_down += down_delta
                
                # بروزرسانی دیتابیس هر دقیقه (ساده‌سازی برای شروع)
                # در پروژه بزرگتر این رو هم به متد جدا می‌بریم
                db.upsert_daily(date.today().isoformat(), up_delta, down_delta)
                
                dashboard = render_dashboard(up_speed, down_speed, session_up, session_down)
                live.update(dashboard)
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Stopped.")

if __name__ == "__main__":
    main()
