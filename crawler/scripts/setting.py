# Code of tocks to be crawled; Set None to crawl all stocks
STOCK_LIST = [2330,
              3008,
              2454,
              6669,
              2327,
              5274,
              3406,
              3034,]

# Number of saved news
MAX_NEWS_NUMBER = 1000

# Oldest date of saved HistoryPrice per Stock
# Supported format: \d+\w, where \w has following options:
# m : month, w : week, d: day, h : hour
OLDEST_HIS_PRICE = '3m'

# Oldest date of saved HistoryPriceSummary per Stock
# Supported format: \d+\w, where \w has following options:
# m : month, w : week, d: day, h : hour
OLDEST_HIS_PRICE_SUM = '12m'


