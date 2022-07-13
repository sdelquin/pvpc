import datetime
from pathlib import Path

import logzero
import typer

import settings
from pvpc.core import PVPC
from pvpc.utils import init_logger, parse_dates_from_range

logger = init_logger()
app = typer.Typer(add_completion=False)


@app.command()
def run(
    verbose: bool = typer.Option(
        False, '--verbose', '-v', show_default=False, help='Loglevel increased to debug.'
    ),
    tomorrow: bool = typer.Option(
        False, '--tomorrow', '-t', show_default=False, help='Get kWh prices at tomorrow.'
    ),
    recreate: bool = typer.Option(
        False, '--recreate', '-x', show_default=False, help='Recreate output data file.'
    ),
    dates: str = typer.Option(
        datetime.date.today().isoformat(),
        '--dates',
        '-d',
        help='Date(s) to be scraped. If a range is wanted, use YYYY-MM-DD:YYYY-MM:DD',
    ),
    output_file: Path = typer.Option(
        settings.PVPC_DATA_PATH,
        '--output',
        '-o',
        help='Output file to store results',
    ),
):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)

    if recreate:
        if typer.confirm('Are you sure to want to recreate output data file?'):
            output_file.unlink(missing_ok=True)

    scraper = PVPC(output_file)

    if tomorrow:
        date = datetime.date.today() + datetime.timedelta(days=1)
        scraper.get_kwh_prices_at(date)
    elif ':' in dates:
        dates = parse_dates_from_range(dates)
        scraper.get_kwh_prices_from_range(*dates)
    else:
        date = datetime.date.fromisoformat(dates)
        scraper.get_kwh_prices_at(date)


if __name__ == "__main__":
    app()
