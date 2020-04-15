import yourkey as key
import pybitflyer

OPEN     = 1
HIGH     = 2
LOW      = 3
CLOSE    = 4
VALUE    = 5
bitflyer = key.bitflyerkey

class bFOrderClass():
    def __init__(self, lot, minute, product_code):
        self.LOT = lot
        self.MINUTE = minute
        self.product_code = product_code

    def limit_order(self, side, price):
        bitflyer.sendchildorder(product_code=self.product_code,
                                child_order_type="LIMIT",
                                price=price,
                                minute_to_expire=self.MINUTE,
                                side=side,
                                size=self.LOT)

    def market_order(self, side):
        bitflyer.sendchildorder(product_code=self.product_code,
                                child_order_type="MARKET",
                                price=price,
                                minute_to_expire=self.MINUTE,
                                side=side,
                                size=self.LOT)

    def order_contents_setting(self, side, price=0, condition_type="MARKET", trigger_price=None,offset=0):
        if condition_type == "STOP_LIMIT":
            order_contents = {"product_code":self.product_code,
                            "condition_type":condition_type,
                            "side":side,
                            "price":price,
                            "trigger_price":trigger_price,
                            "size":self.LOT}
        elif condition_type == "STOP":
            order_contents = {"product_code":self.product_code,
                            "condition_type":condition_type,
                            "side":side,
                            "trigger_price":trigger_price,
                            "size":self.LOT}
        elif condition_type == "LIMIT":
            order_contents = {"product_code":self.product_code,
                            "condition_type":condition_type,
                            "side":side,
                            "price":price,
                            "size":self.LOT}
        elif condition_type == "MARKET":
            order_contents = {"product_code":self.product_code,
                            "condition_type":condition_type,
                            "side":side,
                            "size":self.LOT}
        elif condition_type == "TRAIL":
            order_contents = {"product_code":self.product_code,
                            "condition_type":condition_type,
                            "side":side,
                            "size":self.LOT,
                            "offset":offset}
        return order_contents

    def simple_order(self, order, time_in_force_value="GTC"):
        bitflyer.sendparentorder(order_method="SIMPLE",
                                minute_to_expire=self.MINUTE,
                                time_in_force=time_in_force_value,
                                parameters=[order])

    def ifd_oco_order(self, order1, order2, time_in_force_value="GTC", kind="ifd"):
        if kind == "ifd":
            bitflyer.sendparentorder(order_method="OCO",
                                    minute_to_expire=self.MINUTE,
                                    time_in_force=time_in_force_value,
                                    parameters=[order1,order2])
        elif kind == "oco":
            bitflyer.sendparentorder(order_method="OCO",
                                    minute_to_expire=self.MINUTE,
                                    time_in_force=time_in_force_value,
                                    parameters=[order1,order2])

    def ifdoco_order(self, order1, order2, oreder3, time_in_force_value="GTC"):
        bitflyer.sendparentorder(order_method="IFDOCO",
                                minute_to_expire=self.MINUTE,
                                time_in_force=time_in_force_value,
                                parameters=[order1,order2,order3])

class TechIndicatorsClass():
    def __init__(self, ohlcv):
        self.ohlcv = bf_ohlcv

    def SimpleMA(self, len): #開始日，n日間
        sum_sma = 0
        for i in range(1,len+1):
            sum_sma += self.ohlcv[-i][CLOSE]
        sma = int(sum_sma / len)
        return sma

    def ExponentialMA(self, len):
        sum_ema = ohlcv[-1][CLOSE]
        for i in range(1,len+1):
            sum_ema += self.ohlcv[-i][CLOSE]
        ema = int(sum_ema / (len+1))
        return ema

    def WeightedMA(self, len):
        sum_wma = 0
        for i in range(1, len+1):
            sum_wma += self.ohlcv[i][CLOSE] * (len - i + 1)
        wma = int(sum_wma / len)
        return wma

    def intermediate(self, start, len):
        high = 0
        low = 10000000
        for i in range(start, len+start):
            if(self.ohlcv[-i][HIGH] > high):
                high = self.ohlcv[-i][HIGH]
            if(self.ohlcv[-i][LOW] < low):
                low = self.ohlcv[-i][LOW]
        result = (high + low) / 2
        return result

    def ichimoku(self,t=1): #t = 1~27
        kijyun = self.intermediate(t,26) #現在の基準線
        tenkan = self.intermediate(t, 9) #現在の転換線
        span1  = (self.intermediate(bf_ohlcv, t+26, 26) + self.intermediate(bf_ohlcv, t+26, 9)) / 2 #先行スパン1
        span2  = self.intermediate(bf_ohlcv, t+26, 52) #先行スパン2
        return {'kijyun':kijyun, 'tenkan':tenkan, 'span1':span1, 'span2':span2}

    def channel_breakout(self, len=20):#過去20本分の足の最安高値
        high = 0
        low = 10000000
        for i in range(len):
            if(self.ohlcv[-i-2][HIGH] > high):
                high = self.ohlcv[-i-2][HIGH]
            if(self.ohlcv[-i-2][LOW] < low):
                low = self.ohlcv[-i-2][LOW]
        return {'high': high, 'low': low}
