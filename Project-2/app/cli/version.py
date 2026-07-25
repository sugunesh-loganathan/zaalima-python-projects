import typer

from app.config import settings

app = typer.Typer()


@app.command()
def show():
    """
    Display application version and project information.
    """

    typer.echo(f"\n{settings.PROJECT_NAME}")
    typer.echo(f"Version : {settings.VERSION}")
    typer.echo(f"Author  : {settings.AUTHOR}")
    typer.echo(f"License : {settings.LICENSE}")