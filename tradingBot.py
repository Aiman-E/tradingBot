from bingxapi import *
from trade import *
import ast

class TradingBot():
  client = None
  trades = {}

  def __init__(self) -> None:
    self.client = BingxClient()

  def updateDatabase(self):
    with open("data.json", "w+") as f:
      data = {}
      for i, j in self.trades.items():
        data[i] = ast.literal_eval(str(j))
        data[i]['subtrade'] = ast.literal_eval(str(data[i]['subtrade']))
      json.dump(data, f, indent=2)
    

  def load(self):
    with open("data.json", "r") as f:
      data = json.load(f)
      if data:
        for j in data.values():

          config = subconfig = ORDER_CONFIG.MARKET
          if j['config'].find('long') >= 0:
            config |= ORDER_CONFIG.LONG
            
            if j['subtrade'] != None:
              print('ass')
              subconfig |= ORDER_CONFIG.SHORT
          else:
            config |= ORDER_CONFIG.SHORT
            if j['subtrade'] != None:
              print("as")
              subconfig |= ORDER_CONFIG.LONG

          trade = Trade(
            j['id'],
            j['symbol'],
            j['entry'],
            j['margin'],
            j['volume'],
            j['loss'],
            j['leverage'],
            config
            )
          trade.setSubtradeThreshold(j['subtradeThreshold'])
          trade.setSubtradeTriggerPNL(j['subtradeTriggerPNL'])
          trade.reopened = j['reopened']

          if j['subtrade'] != None:
            subtrade = Trade(
              j['subtrade']['id'],
              j['subtrade']['symbol'],
              j['subtrade']['entry'],
              j['subtrade']['margin'],
              j['subtrade']['volume'],
              j['subtrade']['loss'],
              j['subtrade']['leverage'],
              subconfig
              )
            
            trade.setSubtrade(subtrade)
          
          print(trade)
          self.trades[trade.symbol] = trade
          

  def fetchTrade(self, symbol, loss, lev, config):
    #TODO: on imguiTradeDetails, the trades are referenced from the [0]
    trade = subtrade = None
    details = self.client.getPositionDetails(symbol)   
    side = "Long" if config & ORDER_CONFIG.LONG else "Short"
    subSide = ORDER_CONFIG.MARKET
    subSide |= ORDER_CONFIG.LONG if side == "Short" else ORDER_CONFIG.SHORT
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
        subSide)

    trade.setSubtrade(subtrade)
    self.trades[symbol] = trade
    self.updateDatabase()

  def startTrade(self, symbol, entry, amount, loss, lev, config):
    print(self.client.openOrder(symbol, entry, amount, config))

    details = self.client.getPositionDetails(symbol)
    print(details)

    cng = ORDER_CONFIG.MARKET
    if ORDER_CONFIG.LONG & config:
      cng |= ORDER_CONFIG.LONG
    else:
      cng |= ORDER_CONFIG.SHORT

    trade = None
    for i in details['positions']:
      trade = Trade(i['positionId'],
       symbol,
       i['avgPrice'],
       i['margin'], 
       i['volume'], 
       loss, 
       lev, 
       config)
    self.trades[symbol] = trade
    print(self.trades)
    self.updateDatabase()

  def startSubTrade(self, trade):
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
    
    self.updateDatabase()

  def endTrade(self, symbol):
    if self.trades[symbol].subtrade:
      self.client.close(symbol, self.trades[symbol].subtrade.id)
    self.client.close(symbol, self.trades[symbol].id)
    self.trades.pop(symbol)

    self.updateDatabase()

  def getStoplossRate(self, trade):
    #(final/initial-1)*100
    print((trade.loss/trade.entry-1)*100*trade.leverage)

  def update(self):      
    # try:
      for trade in self.trades.values():
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
            print(f"Price: {s*trade.subtrade.currentPrice} - threshold: {s*trade.getSubtradeThreshold()}")
            if ((s*trade.subtrade.currentPrice >= s*trade.getSubtradeThreshold() and
                not trade.reopened) or
                trade.getPNL()>0.0):
              self.client.close(trade.subtrade.symbol, trade.subtrade.id) #TODO: MOVE TO EXTERNAL FUNCTION 
              trade.subtrade = None
              trade.reopened = False
              print("Closing subtrade")

            elif trade.subtrade.getPNL() > trade.subtradeTriggerPNL:
              self.client.close(trade.subtrade.symbol, trade.subtrade.id) #TODO: MOVE TO EXTERNAL FUNCTION 
              trade.subtrade = None
              trade.reopened = True
              print("reopening subtrade")

    # except KeyboardInterrupt:
      # return
    # except:
      # print("Connection lost, trying again...")

  def adjustParam(self, param, symbol, value):
    if param == 'loss':
      self.trades[symbol].setLoss(value)
      self.updateDatabase()
    elif param == 'threshold':
      self.trades[symbol].setSubtradeThreshold(value)
      self.updateDatabase()
    elif param == 'triggerPNL':
      self.trades[symbol].setSubtradeTriggerPNL(value)
      self.updateDatabase()
    

if __name__ == '__main__':
  bot = TradingBot()
  symbol = "BTC-USDT"
  # symbol2 = "SHIB-USDT"
  price = float(bot.client.getPrice(symbol))
  # price2 = float(bot.client.getPrice(symbol2))
  # bot.fetchTrade(symbol, 22387.0, 150, ORDER_CONFIG.SHORT  | ORDER_CONFIG.MARKET)
  # bot.startTrade(symbol2, price2, 2, price2 - price2*0.001, 50, ORDER_CONFIG.LONG  | ORDER_CONFIG.MARKET)
  bot.load()
  
  while 1:
    bot.update()
