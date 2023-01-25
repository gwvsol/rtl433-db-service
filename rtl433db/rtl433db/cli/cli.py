import click
from .help import ClickHelp as cli

from rtl433db.rtl433 import main


@click.command(help=cli.rtl433db)
@click.option("-s", "--saveconf",
              show_default=False,
              default=False,
              help=cli.saveconf)
def start(saveconf: bool):
    if saveconf:
        from rtl433db.saveconf import saveconfig
        click.echo("\n\033[1;96m {}\033[00m\n" .format(cli.saveconf))
        saveconfig()
    click.echo("\n\033[1;96m {}\033[00m\n" .format(cli.rtl433db))
    main()
