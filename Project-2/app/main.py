import typer

app = typer.Typer()

@app.command()
def hello():
    print("Cloud Infrastructure Auditor CLI Initialized")

if __name__ == "__main__":
    app()