import datetime

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings

from . import utils


class PVPC:
    def __init__(self):
        self.driver = utils.init_webdriver(settings.SELENIUM_HEADLESS)

    def get_kwh_prices_at(self, date: datetime.date):
        url = utils.build_url(settings.PVPC_BASE_URL, dict(date=date.strftime('%d-%m-%Y')))
        print(url)
        self.driver.get(url)

        widget = WebDriverWait(self.driver, timeout=3).until(
            EC.element_to_be_clickable((By.ID, 'pvpcDesgloseWidgetView'))
        )
        widget.click()
        for offset, hour in zip(range(-490, 550, 45), range(0, 24)):
            ActionChains(self.driver).drag_and_drop_by_offset(widget, offset, 0).perform()
            price = widget.find_element(By.XPATH, settings.KWH_PRICE_XPATH)
            print(f'{hour}h: {price.text}€/kWh')
