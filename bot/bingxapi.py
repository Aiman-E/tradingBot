from enum import Flag, auto
import json

from loguru import logger
from timeout_decorator import timeout, TimeoutError
from bingX.perpetual.v1 import Perpetual
from bingX.perpetual.v1 import market


class ORDER_CONFIG(Flag):
  LONG = auto()
  SHORT = auto()
  MARKET = auto()
  LIMIT = auto()
  
  def __str__(self) -> str:
    if self.value == 5:
      return "market|long"
    elif self.value == 6:
      return "market|short"

class BingxClient():
  APIKEY = ""
  SECRETKEY = ""
  CLIENT = None

  def __init__(self) -> None:
    f = open('credentials.txt')
    credentials = json.load(f)['credentials']['bingx']
    self.APIKEY = credentials['APIKEY']
    self.SECRETKEY = credentials['SECRETKEY']
    logger.debug(f"\n\tapikey: {self.APIKEY}\n\tsecretkey:{self.SECRETKEY}")
    self.CLIENT = Perpetual(self.APIKEY, self.SECRETKEY)
  
  # @timeout(3)
  def getPrice(self, symbol) -> str:
    return market.latest_price(self.CLIENT, symbol)["tradePrice"]

  # @timeout(3)
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

  # @timeout(3)
  def openOrderWithVolume(self, symbol, entry, amount, config):
    if config == ORDER_CONFIG.LONG | ORDER_CONFIG.MARKET:
      return self.CLIENT.place_order(symbol, "Bid", entry, amount, "Market", "Open")

    elif config == ORDER_CONFIG.LONG | ORDER_CONFIG.LIMIT:
      return self.CLIENT.place_order(symbol, "Bid", entry, amount, "Limit", "Open")

    elif config == ORDER_CONFIG.SHORT | ORDER_CONFIG.MARKET:
      return self.CLIENT.place_order(symbol, "Ask", entry, amount, "Market", "Open")
    
    elif config == ORDER_CONFIG.SHORT | ORDER_CONFIG.LIMIT:
      return self.CLIENT.place_order(symbol, "Ask", entry, amount, "Limit", "Open")

  # @timeout(3)
  def trim(self, symbol, entry, amount, side):
    if side == ORDER_CONFIG.LONG:
      return self.CLIENT.place_order(symbol, "Ask", entry, amount/entry, "Market", "Close")
    elif side == ORDER_CONFIG.SHORT:
      return self.CLIENT.place_order(symbol, "Bid", entry, amount/entry, "Market", "Close")  

  # @timeout(3)
  def close(self, symbol, id):
    return self.CLIENT.close_position(symbol, id)

  # @timeout(3)
  def getPositionDetails(self, symbol):
    return self.CLIENT.positions(symbol)

  


if __name__=='__main__':
  client = BingxClient()
