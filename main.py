import datetime

import logzero
import typer

from pvpc.core import PVPC
from pvpc.utils import init_logger

logger = init_logger()
app = typer.Typer(add_completion=False)


@app.command()
def run(
    verbose: bool = typer.Option(
        False, '--verbose', '-v', show_default=False, help='Loglevel increased to debug.'
    ),
):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)

    scraper = PVPC()
    scraper.get_kwh_prices_at(datetime.date.today())
    scraper.dump_data()


if __name__ == "__main__":
    app()
