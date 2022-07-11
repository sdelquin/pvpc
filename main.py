import datetime

from pvpc.core import PVPC

scraper = PVPC()
scraper.get_kwh_prices_at(datetime.date.today())
