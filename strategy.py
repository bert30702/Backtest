#Author : Bert

# Class name must be Strategy
class Strategy():
    def __setitem__(self, key, value):
        self.options[key] = value

    def __getitem__(self, key):
        return self.options.get(key, '')

    def __init__(self):
        self.subscribedBooks = {
            'Bitfinex': {
                'pairs': ['ETH-USDT'],
            },
        }
        self.period = 60 * 60 * 4
        self.RSI_period = 14
        self.options = {}

        self.last_price = 0.0
        self.ETH_balance = 0.0
        self.USDT_balance = 0.0
        self.lst = []
        self.cnt = 0
        self.price = 0
        self.max_price = 0
        self.min_price = 1000000

    def RSI(self) :
        lng, shrt = 0.0, 0.0
        for i in range(self.RSI_period) :
            if(self.lst[-i - 1] - self.lst[-i - 2] > 0) :
                lng += (self.lst[-i - 1] - self.lst[-i - 2]) 
            else :
                shrt -= (self.lst[-i - 1] - self.lst[-i - 2])

        if(lng < self.price / 50 * self.RSI_period and shrt < self.price / 50 * self.RSI_period): 
            return -1000

        return 100 * lng / max(1, shrt + lng)
    
    def sell(self) :
        # Log('Sell ' + str(self.price))
        return [
            {
                'amount': -0.10,
                'price': -1,
                'type': 'MARKET',
            }
        ]

    def buy(self) :
        # Log('Buy ' + str(self.price))
        return [
            {
                'amount': 0.10,
                'price': -1,
                'type': 'MARKET',
            }
        ] 

    def Long(self, rsi, price) :
        if(price < self.max_price * 0.98 or rsi <= 50) :
            self.cnt = 0
            self.max_price = 0
            self.min_price = 1000000
            return self.sell()
        return []

    def Short(self, rsi, price) :
        if(price > self.min_price * 1.02 or rsi == -1000 or rsi >= 50) :
            self.cnt = 0
            self.max_price = 0
            self.min_price = 1000000
            return self.buy()
        return []

    def trade(self, information):
        # exchange = list(information['candles'])[0]
        # pair = list(information['candles'][exchange])[0]
        close_price = float(information['close'] or 0)
        high_price = float(information['high'] or 0)
        low_price = float(information['low'] or 0)

        # print('close_price : ' + str(close_price))
        # return []

        if(self.cnt != 0) :
            self.max_price = max(self.max_price, high_price)
            self.min_price = min(self.min_price, low_price)

        self.lst.append(close_price)

        if(len(self.lst) <= self.RSI_period) :
            return []

        rsi = self.RSI()

        if(self.cnt != 0) :
            self.max_price = max(self.max_price, close_price)
            self.min_price = min(self.min_price, close_price)

            if(self.cnt > 0) :
                return self.Long(rsi, close_price)
            else :
                return self.Short(rsi, close_price)

        # if(self.clk % 4 != 0) :
        #     return []

        if(rsi == -1000) :
            # Log('SKIP')
            return []

        if(rsi > 60 and rsi < 70) :
            # Log('Yeeeee')
            self.cnt = 10
            self.max_price = close_price
            self.min_price = close_price
            return self.buy()

        if(rsi < 40 and rsi > 30) :
            # Log('Yeeeee')
            self.cnt = -10
            self.max_price = close_price
            self.min_price = close_price
            return self.sell()

        return []