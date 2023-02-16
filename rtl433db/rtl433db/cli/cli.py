import click
from .help import ClickHelp as cli


@click.group(help=cli.help)
def main() -> None:
    return


@main.command(help=cli.rtl433db)
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
    from rtl433db.rtl433 import main
    main()


@main.command(help=cli.saveconf)
def saveconf():
    click.echo("\n\033[1;96m {}\033[00m\n" .format(cli.saveconf))
    from rtl433db.saveconf import saveconfig
    saveconfig()
