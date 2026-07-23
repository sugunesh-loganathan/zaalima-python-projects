from rich.console import Console
from app.reporting.layout import create_layout

console = Console()


def generate_report():
    layout = create_layout()
    console.print(layout)