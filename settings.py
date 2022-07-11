from prettyconf import config

SELENIUM_HEADLESS = config('SELENIUM_HEADLESS', default=True, cast=lambda v: bool(int(v)))

PVPC_BASE_URL = config('PVPC_BASE_URL', default='https://www.esios.ree.es/es/pvpc')

KWH_PRICE_XPATH = config(
    'KWH_PRICE_XPATH',
    default='/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div/div[4]/'
    'div[2]/div/div/ul/div[1]/li/div[2]/span[1]',
)
