import click
import gspread

from logarius.sheets import get_spreadsheet, list_categories, record_new_entry


@click.group(name="logarius")
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.obj = get_spreadsheet()


@cli.command(name="new")
@click.argument("category", nargs=1)
@click.pass_obj
def new_cmd(spreadsheet: gspread.Spreadsheet, category: str) -> None:
    record_new_entry(spreadsheet=spreadsheet, category=category)


@cli.command(name="list")
@click.pass_obj
def list_cmd(spreadsheet: gspread.Spreadsheet) -> None:
    categories = list_categories(spreadsheet)
    for category in categories:
        click.echo(category)


if __name__ == "__main__":
    cli()
