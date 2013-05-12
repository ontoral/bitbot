import urllib2
import json

tickers = {'btc_usd': 'https://btc-e.com/api/2/btc_usd/ticker',
           'ltc_btc': 'https://btc-e.com/api/2/ltc_btc/ticker',
           'ltc_usd': 'https://btc-e.com/api/2/ltc_usd/ticker'}

for k, v in tickers.iteritems():
    print k

    tickers_feed = urllib2.urlopen(v)
    j = json.loads(tickers_feed.read())
    tickers_feed.close()
    print k, j

