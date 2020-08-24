"""Command-line interface."""
import textwrap

import click

from . import __version__, wikipedia


@click.command()
@click.option(
    "--language", "-l", default="ru", help="Language edition of Wikipedia", metavar="LANG", show_default=True,
)
@click.version_option(version=__version__)
def main(language: str) -> None:
    """Is an entrypoint."""
    page = wikipedia.random_page(lang=language)

    click.secho(page.title, fg="green")
    click.echo(textwrap.fill(page.extract))
