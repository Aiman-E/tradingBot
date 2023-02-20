from enum import Flag, auto
import json


from bingX.perpetual.v1 import Perpetual
from bingX.perpetual.v1 import market
import time 

class ORDER_CONFIG(Flag):
  LONG = auto()
  SHORT = auto()
  MARKET = auto()
  LIMIT = auto()

class BingxClient():
  APIKEY = "2Ohbn3NBvAiBSAbjtwzAKMOXvpcSqCtdXxqK9XFHF56ouSjcai56CHydcFpI0g5IStjh3GbGd9YftZAIew"
  SECRETKEY = "RgVYyNap7rCIa5mkD5DehhcIPnoIdeJvIJ89kBOL4sMs94sKxMqfQydrGhJofRGSSVY5Go6vmXZvIKrvhMLXg"
  CLIENT = None

  def __init__(self) -> None:
    self.CLIENT = Perpetual(self.APIKEY, self.SECRETKEY)
  
  def getPrice(self, symbol) -> str:
    return market.latest_price(self.CLIENT, symbol)["tradePrice"]

  def openOrder(self, symbol, entry, amount, config):
    value = amount/entry
    if config == ORDER_CONFIG.LONG | ORDER_CONFIG.MARKET:
      return self.CLIENT.place_order(symbol, "Bid", entry, value, "Market", "Open")

    elif config == ORDER_CONFIG.LONG | ORDER_CONFIG.LIMIT:
      return self.CLIENT.place_order(symbol, "Bid", entry, value, "Limit", "Open")

    elif config == ORDER_CONFIG.SHORT | ORDER_CONFIG.MARKET:
      return self.CLIENT.place_order(symbol, "Ask", entry, value, "Market", "Open")
    
    elif config == ORDER_CONFIG.SHORT | ORDER_CONFIG.LIMIT:
      return self.CLIENT.place_order(symbol, "Ask", entry, value, "Limit", "Open")

  def trim(self, symbol, entry, amount, side):
    if side == ORDER_CONFIG.LONG:
      return self.CLIENT.place_order(symbol, "Ask", entry, amount/entry, "Market", "Close")
    elif side == ORDER_CONFIG.SHORT:
      return self.CLIENT.place_order(symbol, "Bid", entry, amount/entry, "Market", "Close")  

  def close(self, symbol, id):
    return self.CLIENT.close_position(symbol, id)

  def getPositionDetails(self, symbol):
    return self.CLIENT.positions(symbol)

  


if __name__=='__main__':
  symbol = "USTC-USDT"
  client = BingxClient()
  price = float(client.getPrice(symbol))
  old = price

  orderid = client.openOrder(symbol, price, 1.9, ORDER_CONFIG.LONG | ORDER_CONFIG.MARKET)['orderId']
  
  