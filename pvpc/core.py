import datetime

from logzero import logger
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings

from . import utils


class PVPC:
    def __init__(self, output_file=settings.PVPC_DATA_PATH, quit_on_exception=False):
        logger.debug('Initializing webdriver')
        self.driver = utils.init_webdriver(settings.SELENIUM_HEADLESS)
        self.actions = ActionChains(self.driver)
        self.output_file = output_file
        utils.create_file_if_not_exist(self.output_file)
        self.quit_on_exception = quit_on_exception

    def extract_kwh_price_at(self, widget: WebElement, offset: int):
        self.actions.drag_and_drop_by_offset(widget, offset, 0).perform()
        price = widget.find_element(By.XPATH, settings.KWH_PRICE_XPATH)
        return float(price.text.replace(',', '.'))

    def _handle_error(self, error):
        logger.exception(error)
        if self.quit_on_exception:
            raise error

    def get_kwh_prices_at(self, date: datetime.date):
        try:
            url = utils.build_url(
                settings.PVPC_BASE_URL, dict(date=date.strftime('%d-%m-%Y'))
            )
            logger.info(f'Getting data from {url}')
            self.driver.get(url)
            widget = WebDriverWait(self.driver, timeout=3).until(
                EC.element_to_be_clickable((By.ID, 'pvpcDesgloseWidgetView'))
            )
            # Focus the widget
            widget.click()
        except Exception as e:
            self._handle_error(e)

        self.output = open(self.output_file, 'a')
        # Drag the marker through all hours
        for offset, hour in zip(range(-490, 550, 45), range(0, 24)):
            logger.debug(f'Getting kWh price for {date} {hour:02}h')
            moment = utils.build_datetime(date, hour)
            try:
                price = self.extract_kwh_price_at(widget, offset)
            except Exception as e:
                price = -1
                self._handle_error(e)
            self.output.write(f'{moment.isoformat()},{price}\n')
        self.output.close()

    def get_kwh_prices_from_range(self, start_date, end_date):
        for date in utils.daterange(start_date, end_date):
            self.get_kwh_prices_at(date)

    def __del__(self):
        self.driver.quit()
        self.output.close()
