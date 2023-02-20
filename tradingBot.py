from bingxapi import *
from trade import *
class TradingBot():
  client = None
  trades = []

  def __init__(self) -> None:
    self.client = BingxClient()

  def startTrade(self, symbol, entry, amount, loss, lev, config):
    self.client.openOrder(symbol, entry, amount, config)

    details = self.client.getPositionDetails(symbol)
    
    for i in details['positions']:
      self.trades.append(Trade(i['positionId'], symbol, i['avgPrice'], i['margin'], loss, lev, config))
    print(self.trades[0])

    

  def startSubTrade(self, trade):
    print(self.client.openOrder(trade.symbol, 
      trade.loss, 
      trade.amount, 
      (ORDER_CONFIG.LONG if trade.config & ORDER_CONFIG.SHORT else ORDER_CONFIG.SHORT) | ORDER_CONFIG.MARKET))

    details = self.client.getPositionDetails(symbol)
    for i in details['positions']:
      if i['positionId'] != trade.id:
        trade.setSubtrade(Trade(i['positionId'], 
                trade.symbol, 
                i['avgPrice'], 
                i['margin'], 
                trade.loss, 
                trade.leverage,
                (ORDER_CONFIG.LONG if trade.config & ORDER_CONFIG.SHORT else ORDER_CONFIG.SHORT) | ORDER_CONFIG.MARKET))
        print(f"created subtrade {trade.subtrade}") 

  def endTrade(self, trade):
    self.client.close(trade.symbol, trade.id)

  def getStoplossRate(self, trade):
    #(final/initial-1)*100
    print((trade.loss/trade.entry-1)*100*trade.leverage)

  def run(self):
    x = 0

    while 1:
      x+=1
      for trade in self.trades:
        # Adds subtrade if not exist
        if not trade.subtrade:
          price = float(self.client.getPrice(trade.symbol))
          s = trade.getTradeSign()
          print(f"{x}Price: {price} - Loss: {trade.loss}")
          if s*price <= s*trade.loss:
            self.startSubTrade(trade)
            print("subtrade Done")

        # check subtrade
        else:
          price = float(self.client.getPrice(trade.symbol))
          s = trade.getTradeSign() #equality flips when multiplied with minus
          print(f"{x}Pprice: {s*price} - Loss: {s*trade.getSubtradeThreshold()}")
          if s*price >= s*trade.getSubtradeThreshold():
            print(self.client.close(trade.subtrade.symbol, trade.subtrade.id))
            trade.subtrade = None
            print("Cloding subtrade")


if __name__ == '__main__':
  bot = TradingBot()
  symbol = "USTC-USDT"
  price = float(bot.client.getPrice(symbol))
  bot.startTrade(symbol, price, 1.9, price - 0.000005, 50, ORDER_CONFIG.LONG  | ORDER_CONFIG.MARKET)
  bot.run()