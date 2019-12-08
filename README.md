# stockticker
### stock movement summary push notifications

[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](#)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

- Notifications use [notify.run](https://github.com/notify-run/notify.run)
- Stock data from yahoo finance using [yfinance](https://github.com/ranaroussi/yfinance). Check [yahoo.finance.com](yahoo.finance.com) for ticker symbols
- Message formatting uses Mustache ([pystache](https://github.com/defunkt/pystache))

## Setup:

#### gsheets2pandas setup
1. `git clone https://github.com/lucashadfield/stockticker.git`
2. `cd stockticker`
3. `pip install .`
4. `python stockticker/run.py` or `python stockticker/run.py path_to_config_yaml`


## Notes
- `run.py` looks for yaml config file in `~/.stockticker/config.yaml`. See `config_example.yaml` for format. Any element in the config file can be referenced in the `message` using Mustache syntax, `{{likethis}}` in addition to `{{gain}}` which is the calculated gain in the `period`


## To Do
- Support gains per stock rather than just a total
- Support for multi currency (with currency gain)
- Support for gain since purchase (add purchase date to config). This will also mean that one ticker symbol might exist multiple times with different purchase dates. Also dividend reinvestment flag would be useful.
- Correctly handle dividends
- Alternate delivery methods, eg. email
- Tests