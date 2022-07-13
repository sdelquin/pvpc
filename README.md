# PVPC

![REE](ree.svg)

Regular rate _PVPC (Precio Voluntario para el Pequeño Consumidor)_ (in spanish) is a way of fixing the electricity price. It was designed and is regulated by Spanish Government. It only concerns to clients within _regulated electricity market_.

This price es calculated **daily** by _Red Eléctrica de España (REE)_ (in spanish) in terms of hourly prices of market energy. Electricity price **can change hourly** according to the evolution of electric market.

Prices are daily published at [Red Eléctrica Española](https://www.esios.ree.es/es/pvpc) website.

## Aim

The idea behing this project is to make a daily scraping on REE website and get the PVPC of next day, adding these new data to an existing file containing historical data.

## Data

PVPC data is available on file [pvpc.csv](data/pvpc.csv). There is information since 1st April 2014 with records during 24 hours per day and data concerning the Spanish Mainland, Balearic and Canary Islands (peaje 2.0 TD).

Each record has got these two fields:

- **Timestamp** with isoformat `YYYYMMDDTHHMMSS`
- **PVPC price** as a floating number (max 5 decimals) whose measurement unit is €/kWh

**This file is updated daily in an automatic manner.**

Datasets are also available at [Kaggle](https://www.kaggle.com/sdelquin/pvpc).

## Setup

Create a Python virtualenv and install requirements:

```console
$ python3.10 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Optionally, you can create a `.env` file in the working directory to overwrite settings from [settings.py](settings.py).

### Other requirements

There are few external requirements for the project to work properly:

- [geckodriver](https://github.com/mozilla/geckodriver/releases)
- [Firefox Browser](https://www.mozilla.org/firefox/download/)

## Usage

```console
$ python main.py --help
Usage: main.py [OPTIONS]

Options:
  -v, --verbose      Increase loglevel to debug.
  -t, --tomorrow     Get kWh prices for tomorrow.
  -x, --recreate     Recreate output data file.
  -d, --dates TEXT   Date(s) to be scraped. If a range is wanted, use YYYY-MM-
                     DD:YYYY-MM:DD (both included).  [default: 2022-07-13]
  -o, --output PATH  Output file to store results.  [default:
                     /apps/pvpc/data/pvpc.csv]
  --help             Show this message and exit.
```

A common usage would be just `python main.py -v`. It will try to get electricity prices for today. After each execution, new data is appended to [pvpc.csv](data/pvpc.csv).
