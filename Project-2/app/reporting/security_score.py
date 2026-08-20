from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.console import Group
from rich.text import Text


def create_security_score(score):

    progress = ProgressBar(
        total=100,
        completed=score,
        width=40,
    )

    color = "green"

    if score < 80:
        color = "yellow"

    if score < 60:
        color = "red"

    group = Group(
        Text(f"Overall Security Score : {score}/100", style=f"bold {color}"),
        Text(""),
        progress,
    )

    return Panel(
        group,
        title="Security Score",
        border_style=color,
    )