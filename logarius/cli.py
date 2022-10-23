import click

from logarius.sheets import run


@click.command(name="logarius")
@click.argument("name", nargs=1)
def cli(name: str) -> None:
    run(name)


if __name__ == "__main__":
    cli()
