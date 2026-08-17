import typer

from aws.auth import AWSAuth
from aws.client_factory import AWSClientFactory
from aws.cleanup import CleanupService
from aws.cloudwatch import CloudWatchService
from aws.ec2 import EC2Service
from aws.ebs import EBSService
from aws.eip import ElasticIPService

app = typer.Typer(
    name="cloud-auditor",
    help="AWS Cloud Infrastructure Auditor & Cost Optimizer"
)


def create_client_factory():
    """
    Create AWS authentication and client factory.
    """
    auth = AWSAuth()
    return AWSClientFactory(auth)


@app.command()
def scan():
    """
    Scan AWS resources.
    """

    factory = create_client_factory()

    ec2_service = EC2Service(factory)
    ebs_service = EBSService(factory)
    eip_service = EIPService(factory)

    print("\n" + "=" * 60)
    print("AWS RESOURCE SCAN")
    print("=" * 60)

    instances = ec2_service.list_instances()
    volumes = ebs_service.list_volumes()
    addresses = eip_service.list_addresses()

    print(f"\nEC2 Instances : {len(instances)}")
    print(f"EBS Volumes   : {len(volumes)}")
    print(f"Elastic IPs   : {len(addresses)}")

    print("\nScan completed.")


@app.command()
def report():
    """
    Generate AWS cleanup and optimization report.
    """

    factory = create_client_factory()

    cleanup_service = CleanupService(factory)

    summary = cleanup_service.generate_summary(
        dry_run=True
    )

    cleanup_service.display_summary(summary)


@app.command()
def cleanup(
    execute: bool = typer.Option(
        False,
        "--execute",
        help="Actually delete/release eligible resources."
    )
):
    """
    Preview or execute AWS cleanup.

    Default behavior is DRY RUN.
    """

    factory = create_client_factory()

    cleanup_service = CleanupService(factory)

    if execute:
        typer.echo("\nWARNING: Cleanup execution mode enabled.")

        confirmation = typer.confirm(
            "Do you really want to modify AWS resources?"
        )

        if not confirmation:
            typer.echo("Cleanup cancelled.")
            raise typer.Exit()

    result = cleanup_service.run_cleanup_workflow(
        dry_run=not execute
    )

    typer.echo(
        f"\nCleanup status: {result['status']}"
    )


if __name__ == "__main__":
    app()