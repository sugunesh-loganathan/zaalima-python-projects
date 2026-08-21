"""
Reusable Rich Panel Factory

Provides helper functions for creating
consistent Rich panels throughout the reporting module.
"""

from rich.panel import Panel


def create_panel(content, title="", border_style="cyan"):
    """
    Create a reusable Rich panel.

    Args:
        content: Rich renderable or string.
        title: Panel title (optional).
        border_style: Panel border color.

    Returns:
        Panel
    """
    return Panel(
        content,
        title=title,
        border_style=border_style,
    )