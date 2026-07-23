import typer

from app.config import settings

app = typer.Typer()

@app.command()
def show():
    """Show application version."""
    typer.echo(
        f"{settings.PROJECT_NAME} - Version {settings.VERSION}"
    )