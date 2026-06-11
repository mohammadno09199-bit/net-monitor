from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()


def format_bytes(num: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024
    return f"{num:.2f} PB"


def render_dashboard(
    up_speed: float,
    down_speed: float,
    session_up: int,
    session_down: int,
    today_up: int,
    today_down: int,
    buffer_up: int,
    buffer_down: int,
):
    table = Table(title="NetUsage Monitor", expand=True)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    table.add_row("Upload Speed", f"{format_bytes(up_speed)}/s")
    table.add_row("Download Speed", f"{format_bytes(down_speed)}/s")
    table.add_row("Session Upload", format_bytes(session_up))
    table.add_row("Session Download", format_bytes(session_down))
    table.add_row("Today Upload", format_bytes(today_up))
    table.add_row("Today Download", format_bytes(today_down))
    table.add_row("Buffer Upload", format_bytes(buffer_up))
    table.add_row("Buffer Download", format_bytes(buffer_down))

    footer = Text()
    footer.append(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="bold yellow")
    footer.append(" | Press Ctrl+C to stop", style="bold red")

    return Panel(table, title="Live Stats", subtitle=footer)
