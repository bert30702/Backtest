import hmac
import urllib.request
from requests import Request
import time
import requests
from bs4 import BeautifulSoup
import json
import datetime

import strategy

def eprint(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)

a = strategy.Strategy()
start_time = int(input('Start Time (Unix time, enter -1 to default 2019/11/28 00:00:00): '))
end_time   = int(input('End Time (Unix time, enter -1 to default 2020/11/28 00:00:00): '))
market     = input('Market (-1 to BTC-PERP) : ')

if(start_time == -1) : start_time = 1574899200
if(end_time   == -1) : end_time   = 1606521600
if(market     == '-1') : market = 'BTC-PERP'

sell, buy = [], []

for i in range(start_time, end_time, a.period) :
	url = 'https://ftx.com/api/markets/' + market + '/candles?resolution=' + str(a.period) + '&limit=5000&start_time=' + str(i) + '&end_time=' + str(i + a.period)
	list_req = requests.get(url)

	soup = BeautifulSoup(list_req.content, "html.parser")
	getjson = json.loads(soup.text)

	getresult = a.trade(getjson['result'][0])
	# getresult = json.loads(result)

	close = float(getjson['result'][0]['close'])

	if(len(getresult) > 0 and float(getresult[0]['amount']) < 0) :
		print('Sell @' + str(close))
		sell.append(close)

	if(len(getresult) > 0 and float(getresult[0]['amount']) > 0) :
		print('Buy @' + str(close))
		buy.append(close)

profit = 0.0
sum = 0.0
max_DD = 0.0

size = min(len(buy), len(sell))
for i in range(size) :
	profit += sell[i] - buy[i]
	sum += sell[i] - buy[i]
	if(sum > 0) : sum = 0
	max_DD = min(max_DD, sum)

print('Profit : ' + str(profit))
print('Max DD : ' + str(max_DD))
	# print('\n'.join(map(str, getjson['result'])))
# # f.write('\n'.join(map(str, getjson['rSesult'])))
# # print(i)
# # time.sleep(0.03)

# # f.close()

# #  print(getjson['result'])