from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def format_bytes(n):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if n < 1024: return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} TB"

def render_dashboard(up_speed, down_speed, total_up, total_down):
    table = Table(title="Live Monitor", expand=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Upload Speed", f"{format_bytes(up_speed)}/s")
    table.add_row("Download Speed", f"{format_bytes(down_speed)}/s")
    table.add_row("Session Upload", format_bytes(total_up))
    table.add_row("Session Download", format_bytes(total_down))
    
    return Panel(table, title="Net Monitor Stats")
