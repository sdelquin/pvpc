import datetime
import os
from pathlib import Path
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


def build_datetime(date: datetime.date, hour: int):
    time = datetime.time(hour=hour, minute=0, second=0)
    return datetime.datetime.combine(date, time)


def create_file_if_not_exist(filepath: Path):
    if not filepath.exists():
        filepath.parent.mkdir(parents=True)
        filepath.touch()
