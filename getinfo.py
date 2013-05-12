# If you find this sample useful, please feel free to donate :)
# LTC: LePiC6JKohb7w6PdFL2KDV1VoZJPFwqXgY
# BTC: 1BzHpzqEVKjDQNCqV67Ju4dYL68aR8jTEe

import httplib
import urllib
import json
import hashlib
import hmac
import time

from btcapi import *

def get_nonce():
    t = time.time()
    upper = int(time.time()) % 10000000 * 100
    lower = int(time.time() * 100) % 100
    return upper + lower

# Replace these with your own API key data
# BTC_api_key = ""      Pulled from btcapi
# BTC_api_secret = ""   Pulled from btcapi
# Come up with your own method for choosing an incrementing nonce
# nonce = 13

# method name and nonce go into the POST parameters
params = {"method":"TradeHistory",
          "nonce": get_nonce()}
params = urllib.urlencode(params)

# Hash the params string to produce the Sign header value
H = hmac.new(BTC_api_secret, digestmod=hashlib.sha512)
H.update(params)
sign = H.hexdigest()

headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Key":BTC_api_key,
                   "Sign":sign}
conn = httplib.HTTPSConnection("btc-e.com")
conn.request("POST", "/tapi", params, headers)
response = conn.getresponse()

print response.status, response.reason
print json.load(response)

conn.close()


"""getInfo
200 OK
{u'return':
    {u'funds':
        {u'ppc': 0, u'usd': 0, u'trc': 0, u'ltc': 10, u'cnc': 0, u'ftc': 0, u'nvc': 0, u'nmc': 0, u'btc': 0, u'rur': 0, u'eur': 0},
     u'open_orders': 0, 
     u'server_time': 1368253349, 
     u'transaction_count': 1, 
     u'rights': {u'info': 1, 
     u'withdraw': 0, 
     u'trade': 0}},
 u'success': 1}
"""

"""TransHistory
200 OK
{u'return':
    {u'32654213': 
        {u'status': 2, 
         u'timestamp': 1368252486, 
         u'currency': u'LTC', 
         u'amount': 10.0, 
         u'type': 1, 
         u'desc': u'LTC payment'}}, 
 u'success': 1}
"""

"""TradeHistory
200 OK
{u'success': 0, 
 u'error': u'no trades'}
"""

