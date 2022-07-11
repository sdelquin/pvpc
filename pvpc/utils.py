import os
from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def init_webdriver(headless=True):
    options = Options()
    options.headless = headless
    service = Service(log_path=os.devnull)
    return webdriver.Firefox(options=options, service=service)


def build_url(path: str, query: dict):
    path = path[:-1] if path.endswith('/') else path
    return f'{path}?{urlencode(query)}'
