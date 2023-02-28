from bingxapi import *
from trade import *

class TradingBot():
  client = None
  trades = {}

  def __init__(self) -> None:
    self.client = BingxClient()

  def fetchTrade(self, symbol, loss, lev, config):
    #TODO: on imguiTradeDetails, the trades are referenced from the [0]
    trade = subtrade = None
    details = self.client.getPositionDetails(symbol)   
    side = "Long" if config & ORDER_CONFIG.LONG else "Short"
    print(f"The side is: {side}")
    for i in details['positions']:
      if i['positionSide'] == side:
        trade = Trade(i['positionId'],
        symbol,
        i['avgPrice'],
        i['margin'], 
        i['volume'], 
        loss, 
        lev, 
        config)
      else:
        subtrade = Trade(i['positionId'],
        symbol,
        i['avgPrice'],
        i['margin'], 
        i['volume'], 
        loss, 
        lev, 
        config)

    trades = []
    trade.setSubtrade(subtrade)
    trades.append(trade)
    self.trades[symbol] = trades

  def startTrade(self, symbol, entry, amount, loss, lev, config):
    print(self.client.openOrder(symbol, entry, amount, config))

    trades = []
    details = self.client.getPositionDetails(symbol)
    print(details)

    for i in details['positions']:
      trades.append(Trade(i['positionId'],
       symbol,
       i['avgPrice'],
       i['margin'], 
       i['volume'], 
       loss, 
       lev, 
       config))
    self.trades[symbol] = trades
    print(self.trades)

  def startSubTrade(self, trade):
    print(trade)
    print(self.client.openOrderWithVolume(trade.symbol, 
      trade.loss, 
      trade.volume, 
      (ORDER_CONFIG.LONG if trade.config & ORDER_CONFIG.SHORT else ORDER_CONFIG.SHORT) | ORDER_CONFIG.MARKET))

    details = self.client.getPositionDetails(trade.symbol)
    for i in details['positions']:
      if i['positionId'] != trade.id:
        trade.setSubtrade(Trade(i['positionId'], 
                trade.symbol, 
                i['avgPrice'], 
                i['margin'],
                i['volume'],
                trade.loss, 
                trade.leverage,
                (ORDER_CONFIG.LONG if trade.config & ORDER_CONFIG.SHORT else ORDER_CONFIG.SHORT) | ORDER_CONFIG.MARKET))
        print(f"created subtrade {trade.subtrade}") 

  def endTrade(self, symbol):
    if self.trades[symbol][0].subtrade:
      self.client.close(symbol, self.trades[symbol][0].subtrade.id)
    self.client.close(symbol, self.trades[symbol][0].id)
    self.trades.pop(symbol)

  def getStoplossRate(self, trade):
    #(final/initial-1)*100
    print((trade.loss/trade.entry-1)*100*trade.leverage)

  def update(self):      
    try:
      for t in self.trades.values():
        for trade in t:
          # Adds subtrade if not exist
          if not trade.subtrade:
            trade.setCurrentPrice(float(self.client.getPrice(trade.symbol)))
            s = trade.getTradeSign()
            print(f"Price: {trade.currentPrice} - Loss: {trade.loss}")
            if s*trade.currentPrice <= s*trade.loss:
              self.startSubTrade(trade)
              print("subtrade Done")

          # check subtrade
          else:
            price = float(self.client.getPrice(trade.symbol))
            trade.setCurrentPrice(price)
            trade.subtrade.setCurrentPrice(price)
            s = trade.getTradeSign() #equality flips when multiplied with minus
            print(f"Pprice: {s*trade.subtrade.currentPrice} - Loss: {s*trade.getSubtradeThreshold()}")
            if s*trade.subtrade.currentPrice >= s*trade.getSubtradeThreshold():
              self.endTrade(trade.subtrade)
              trade.subtrade = None
              print("Closing subtrade")
    except KeyboardInterrupt:
      return
    except:
      print("Connection lost, trying again...")

  def adjustParam(self, param, symbol, value):
    if param == 'loss':
      self.trades[symbol][0].setLoss(value)
    elif param == 'threshold':
      self.trades[symbol][0].setSubtradeThreshold(value)
    

if __name__ == '__main__':
  bot = TradingBot()
  symbol = "USTC-USDT"
  # symbol2 = "SHIB-USDT"
  price = float(bot.client.getPrice(symbol))
  # price2 = float(bot.client.getPrice(symbol2))
  # bot.startTrade(symbol, 0.02744, 2.2, 0.0274, 1, ORDER_CONFIG.LONG  | ORDER_CONFIG.MARKET)
  # bot.startTrade(symbol2, price2, 2, price2 - price2*0.001, 50, ORDER_CONFIG.LONG  | ORDER_CONFIG.MARKET)
  
  while 1:
    bot.update()