import datetime

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings

from . import utils


class PVPC:
    def __init__(self):
        self.driver = utils.init_webdriver(settings.SELENIUM_HEADLESS)
        self.actions = ActionChains(self.driver)
        self.data = {}

    def extract_kwh_price_at(self, widget: WebElement, offset: int):
        self.actions.drag_and_drop_by_offset(widget, offset, 0).perform()
        price = widget.find_element(By.XPATH, settings.KWH_PRICE_XPATH)
        return float(price.text.replace(',', '.'))

    def get_kwh_prices_at(self, date: datetime.date):
        url = utils.build_url(settings.PVPC_BASE_URL, dict(date=date.strftime('%d-%m-%Y')))
        self.driver.get(url)

        widget = WebDriverWait(self.driver, timeout=3).until(
            EC.element_to_be_clickable((By.ID, 'pvpcDesgloseWidgetView'))
        )
        # Focus the widget
        widget.click()
        # Drag the marker through all hours
        for offset, hour in zip(range(-490, 550, 45), range(0, 24)):
            price = self.extract_kwh_price_at(widget, offset)
            moment = utils.build_datetime(date, hour)
            self.data[moment] = price

    def dump_data(self):
        utils.create_file_if_not_exist(settings.PVPC_DATA_PATH)
        with open(settings.PVPC_DATA_PATH, 'a') as f:
            for moment, price in self.data.items():
                f.write(f'{moment.isoformat()},{price}\n')

    def __del__(self):
        self.driver.quit()
