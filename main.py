import datetime

import logzero
import typer

from pvpc.core import PVPC
from pvpc.utils import init_logger, parse_dates_from_range

logger = init_logger()
app = typer.Typer(add_completion=False)


@app.command()
def run(
    verbose: bool = typer.Option(
        False, '--verbose', '-v', show_default=False, help='Loglevel increased to debug.'
    ),
    dates: str = typer.Option(
        datetime.date.today().isoformat(),
        '--dates',
        '-d',
        help='Date(s) to be scraped. If a range is wanted, use YYYY-MM-DD:YYYY-MM:DD',
    ),
):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)

    scraper = PVPC()

    if ':' in dates:
        dates = parse_dates_from_range(dates)
        scraper.get_kwh_prices_from_range(*dates)
    else:
        date = datetime.date.fromisoformat(dates)
        scraper.get_kwh_prices_at(date)

    scraper.dump_data()


if __name__ == "__main__":
    app()
