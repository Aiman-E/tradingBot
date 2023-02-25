from bingxapi import *
from trade import *
class TradingBot():
  client = None
  trades = {}

  def __init__(self) -> None:
    self.client = BingxClient()

  def startTrade(self, symbol, entry, amount, loss, lev, config):
    self.client.openOrder(symbol, entry, amount, config)


    trades = []
    details = self.client.getPositionDetails(symbol)
    
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

  def startSubTrade(self, trade):
    print(trade)
    print(self.client.openOrderWithVolume(trade.symbol, 
      trade.loss, 
      trade.volume, 
      (ORDER_CONFIG.LONG if trade.config & ORDER_CONFIG.SHORT else ORDER_CONFIG.SHORT) | ORDER_CONFIG.MARKET))

    details = self.client.getPositionDetails(symbol)
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

  def endTrade(self, trade):
    self.client.close(trade.symbol, trade.id)

  def getStoplossRate(self, trade):
    #(final/initial-1)*100
    print((trade.loss/trade.entry-1)*100*trade.leverage)

  def run(self):
    x = 0
    
    while 1:
      x+=1
      try:
        for t in self.trades.values():
          for trade in t:
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
                self.endTrade(trade.subtrade)
                trade.subtrade = None
                print("Closing subtrade")
      except KeyboardInterrupt:
        return
      except:
        print("Connection lost, trying again...")


if __name__ == '__main__':
  bot = TradingBot()
  symbol = "BONK-USDT"
  # symbol2 = "SHIB-USDT"
  price = float(bot.client.getPrice(symbol))
  # price2 = float(bot.client.getPrice(symbol2))
  bot.startTrade(symbol, price, 2.2, price + price*(.3/100), 1, ORDER_CONFIG.SHORT  | ORDER_CONFIG.MARKET)
  # bot.startTrade(symbol2, price2, 2, price2 - price2*0.001, 50, ORDER_CONFIG.LONG  | ORDER_CONFIG.MARKET)
  
  bot.run()