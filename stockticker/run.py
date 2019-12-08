import sys
from stockticker.ticker import StockMovements

if len(sys.argv) < 2:
    path = '~/.stockticker/config.yaml'
else:
    path = sys.argv[1]

StockMovements(path).notify_gain()
