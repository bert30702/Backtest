import hmac
import urllib.request
import time
import requests
import json
import datetime
from datetime import datetime
from bs4 import BeautifulSoup
from requests import Request
import os, sys

import strategy

try :
	os.mkdir('./data')
except FileExistsError :
	print('OK')

a = strategy.Strategy()
start_time = int(input('Start Time (Unix time, enter -1 to default 2019/11/28 00:00:00): '))
end_time   = int(input('End Time (Unix time, enter -1 to default 2020/11/28 00:00:00): '))
market     = input('Market (-1 to BTC-PERP) : ')

if(start_time == -1) : start_time = 1574899200
if(end_time   == -1) : end_time   = 1606521600
if(market     == '-1') : market = 'BTC-PERP'

sell, buy = [], []

for i in range(start_time, end_time, a.period) :
	try :
		file = 'data/' + market + str(a.period) + str(i) + '.data'
		f = open(file)
		data = f.read()

	except FileNotFoundError :
		file = 'data/' + market + str(a.period) + str(i) + '.data'
		url = 'https://ftx.com/api/markets/' + market + '/candles?resolution=' + str(a.period) + '&limit=5000&start_time=' + str(i) + '&end_time=' + str(i + a.period)
		list_req = requests.get(url).content
		soup = BeautifulSoup(list_req, "html.parser")

		f = open(file, "w+")
		f.write(soup.text)
		data = soup.text

	# print(data)
	getjson = json.loads(data)


	getresult = a.trade(getjson['result'][0])
	# getresult = json.loads(result)

	close = float(getjson['result'][0]['close'])

	if(len(getresult) > 0 and float(getresult[0]['amount']) < 0) :
		print('Sell @' + str(close) + ' ' + datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S'))
		sell.append(close)

	if(len(getresult) > 0 and float(getresult[0]['amount']) > 0) :
		print('Buy  @' + str(close) + ' ' + datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S'))
		buy.append(close)

profit = 0.0
sum = 0.0
max_DD = 0.0
win, lose = 0, 0

size = min(len(buy), len(sell))
for i in range(size) :
	if(sell[i] - buy[i] > 0) : win += 1
	else                     : lose += 1
	profit += sell[i] - buy[i]
	sum += sell[i] - buy[i]
	if(sum > 0) : sum = 0
	max_DD = min(max_DD, sum)

print('Num Trades : ' + str(size))
print('Profit : ' + str(profit))
print('Max DD : ' + str(max_DD))
print('Win rate : ' + str(win / (win + lose)))
	# print('\n'.join(map(str, getjson['result'])))
# # f.write('\n'.join(map(str, getjson['rSesult'])))
# # print(i)
# # time.sleep(0.03)

# # f.close()

# #  print(getjson['result'])
