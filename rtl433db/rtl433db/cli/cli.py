import click
from .help import ClickHelp as cli


@click.group(help=cli.help)
def main() -> None:
    return


@main.command(help=cli.run)
def run():
    click.echo("\n\033[1;96m {}\033[00m\n" .format(cli.run))
    from rtl433db.app import run_app
    run_app()
