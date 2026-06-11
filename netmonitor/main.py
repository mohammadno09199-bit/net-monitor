import time
from datetime import datetime, date

from rich.live import Live

from netmonitor.config import REFRESH_INTERVAL, FLUSH_INTERVAL
from netmonitor.database import DatabaseManager
from netmonitor.exporter import export_logs_to_csv
from netmonitor.monitor import NetMonitor
from netmonitor.ui import render_dashboard, console


def main():
    db = DatabaseManager()
    monitor = NetMonitor()

    session_up = 0
    session_down = 0

    buffer_up = 0
    buffer_down = 0

    elapsed_since_flush = 0

    today_str = date.today().isoformat()
    today_up, today_down = db.get_today_stats(today_str)

    with Live(refresh_per_second=4, screen=False, console=console) as live:
        try:
            while True:
                current_today = date.today().isoformat()
                if current_today != today_str:
                    today_str = current_today
                    today_up, today_down = db.get_today_stats(today_str)

                up_delta, down_delta, up_speed, down_speed = monitor.get_speed(REFRESH_INTERVAL)

                session_up += up_delta
                session_down += down_delta

                buffer_up += up_delta
                buffer_down += down_delta

                today_up += up_delta
                today_down += down_delta

                elapsed_since_flush += REFRESH_INTERVAL

                if elapsed_since_flush >= FLUSH_INTERVAL:
                    timestamp = datetime.now().isoformat(timespec="seconds")
                    db.insert_minute_log(timestamp, buffer_up, buffer_down)
                    db.upsert_daily(today_str, buffer_up, buffer_down)
                    db.cleanup_old_minute_logs()

                    buffer_up = 0
                    buffer_down = 0
                    elapsed_since_flush = 0

                dashboard = render_dashboard(
                    up_speed=up_speed,
                    down_speed=down_speed,
                    session_up=session_up,
                    session_down=session_down,
                    today_up=today_up,
                    today_down=today_down,
                    buffer_up=buffer_up,
                    buffer_down=buffer_down,
                )
                live.update(dashboard)

                time.sleep(REFRESH_INTERVAL)

        except KeyboardInterrupt:
            if buffer_up > 0 or buffer_down > 0:
                timestamp = datetime.now().isoformat(timespec="seconds")
                db.insert_minute_log(timestamp, buffer_up, buffer_down)
                db.upsert_daily(today_str, buffer_up, buffer_down)
                db.cleanup_old_minute_logs()

            logs = db.get_recent_minute_logs()
            export_path = export_logs_to_csv(logs)

            console.print("\n[bold red]Monitor stopped.[/bold red]")
            console.print(f"[bold green]Exported CSV:[/bold green] {export_path}")


if __name__ == "__main__":
    main()
