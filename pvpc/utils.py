import datetime
import os
import re
from pathlib import Path
from urllib.parse import urlencode

import logzero
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

import settings


def init_logger():
    console_logformat = (
        '%(asctime)s '
        '%(color)s'
        '[%(levelname)-8s] '
        '%(end_color)s '
        '%(message)s '
        '%(color)s'
        '(%(filename)s:%(lineno)d)'
        '%(end_color)s'
    )
    # remove colors on logfile
    file_logformat = re.sub(r'%\((end_)?color\)s', '', console_logformat)

    console_formatter = logzero.LogFormatter(fmt=console_logformat)
    file_formatter = logzero.LogFormatter(fmt=file_logformat)
    logzero.setup_default_logger(formatter=console_formatter)
    logzero.logfile(
        settings.LOGFILE,
        maxBytes=settings.LOGFILE_SIZE,
        backupCount=settings.LOGFILE_BACKUP_COUNT,
        formatter=file_formatter,
    )
    return logzero.logger


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
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.touch()


def daterange(start, end, step=datetime.timedelta(1), closed_interval=False):
    '''https://stackoverflow.com/a/40023824'''
    curr = start
    end = (end + datetime.timedelta(1)) if closed_interval else end
    while curr < end:
        yield curr
        curr += step


def parse_dates_from_range(range: str):
    date1, date2 = range.split(':')
    date1 = datetime.date.fromisoformat(date1)
    date2 = datetime.date.fromisoformat(date2)
    return date1, date2
