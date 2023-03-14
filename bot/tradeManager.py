import ast

from bot.bingxapi import *
from bot.trade import *

class TradeManager():
  client = None
  FEE = 0.05
  trades = {}

  def __init__(self) -> None:
      self.client = BingxClient()

  def updatePrices(self):
    for i in self.trades.values():
      try:
        price = float(self.client.getPrice(i.symbol))
      except TimeoutError as e:
        logger.warning("Connection lost.. trying again")
        return -1
      except Exception as e:
        logger.error(e)
        return -1
      
      i.setCurrentPrice(price)
      self.calculateActualPNL(i)
      if i.subtrade:
        i.subtrade.setCurrentPrice(price)

    return 0

  def updateDatabase(self):
    with open("data.json", "w+") as f:
      data = {}
      for i, j in self.trades.items():
        data[i] = ast.literal_eval(str(j))
        data[i]['subtrade'] = ast.literal_eval(str(data[i]['subtrade']))
      json.dump(data, f, indent=2)
    
    return 0
  

  def load(self):
    try:
      with open("data.json", "r") as f:
        data = json.load(f)
        if data:
          for j in data.values():

            config = subconfig = ORDER_CONFIG.MARKET
            if j['config'].find('long') >= 0:
              config |= ORDER_CONFIG.LONG
              
              if j['subtrade'] != None:
                subconfig |= ORDER_CONFIG.SHORT
            else:
              config |= ORDER_CONFIG.SHORT
              if j['subtrade'] != None:
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
            trade.accumulatingSubtradePNL = j['accumulatingSubtradePNL']
            
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
            
            self.trades[trade.symbol] = trade
    except FileNotFoundError as e:
      logger.warning("data file not found.. Please fetch trades before loading")
      return -1

    return 0
          

  def fetchTrade(self, symbol, loss, lev, config):
    logger.debug(f"Fetching order: {symbol} / {str(config)}")
    trade = self.getTradeInfo(symbol, loss, lev, config)
    if trade == -1:
      return -1

    self.trades[symbol] = trade
    self.updateDatabase()

    return 0

  def startTrade(self, symbol, entry, amount, loss, lev, config):
    logger.debug(f"Opening order: {symbol} / {str(config)}")
    try:
      self.client.openOrder(symbol, entry, amount, config)
    except TimeoutError as e:
      logger.warning("Connection lost.. trying again")
      return -1
    except Exception as e:
      logger.error(e)
      return -1
    
    trade = self.getTradeInfo(symbol, loss, lev, config)
    if trade == -1:
      return -1

    self.trades[symbol] = trade
    self.updateDatabase()
    return 0

  def startSubTrade(self, trade):
    logger.debug(f"Opening subtrade({trade.reopened+1}): {trade.symbol} / {str(trade.config)}")
    try:
      self.client.openOrderWithVolume(trade.symbol, 
        trade.loss, 
        trade.volume, 
        (ORDER_CONFIG.LONG if trade.config & ORDER_CONFIG.SHORT else ORDER_CONFIG.SHORT) | ORDER_CONFIG.MARKET)
    except TimeoutError as e:
      logger.warning("Connection lost.. trying again")
      return -1
    except Exception as e:
      logger.error(e)
      return -1

    t = self.getTradeInfo(trade.symbol, trade.loss, trade.leverage, trade.config)
    if t == -1:
      return -1
    
    trade.setSubtrade(t.subtrade)
    trade.reopened += 1
    self.calculateActualPNL(trade)

    self.updateDatabase()
    return 0

  def endTrade(self, symbol):
    logger.debug(f"Ending trade: {symbol}")

    try:
      if self.trades[symbol].subtrade:
        self.client.close(symbol, self.trades[symbol].subtrade.id)
      self.client.close(symbol, self.trades[symbol].id)
      self.trades.pop(symbol)
    except TimeoutError as e:
      logger.warning("Connection lost... trying again")
      return -1
    except Exception as e:
      logger.error(e)
      return -1

    self.updateDatabase()
    return 0

  def endSubtrade(self, symbol):
    logger.debug(f"Ending subtrade: {symbol}")

    try:
      self.client.close(symbol, self.trades[symbol].subtrade.id)
      
      self.trades[symbol].accumulatingSubtradePNL += self.trades[symbol].subtrade.getPNL()
      self.trades[symbol].setSubtrade(None)

    except TimeoutError as e:
      logger.warning("Connection lost... trying again")
      return -1
    except Exception as e:
      logger.error(e)
      return -1

    self.updateDatabase()
    return 0


  def getTradeInfo(self, symbol, loss, lev, config):
    details = trade = subtrade = None

    try:
      details = self.client.getPositionDetails(symbol)    
    except TimeoutError as e:
      logger.warning("Connection lost.. trying again")
      return -1
    except Exception as e:
      logger.error(e)
      return -1

    side = "Long" if config & ORDER_CONFIG.LONG else "Short"
    subSide = ORDER_CONFIG.MARKET
    subSide |= ORDER_CONFIG.LONG if side == "Short" else ORDER_CONFIG.SHORT

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

    return trade
  
  def adjustParam(self, param, symbol, value):
    if param == 'loss':
      logger.debug("Updating loss")
      self.trades[symbol].setLoss(value)
      self.updateDatabase()
    elif param == 'threshold':
      logger.debug("Updating threshold")
      self.trades[symbol].setSubtradeThreshold(value)
      self.updateDatabase()
    elif param == 'triggerPNL':
      logger.debug("Updating triggerPNL")
      self.trades[symbol].setSubtradeTriggerPNL(value)
      self.updateDatabase()

  def calculateActualPNL(self, trade):
    feeLosses = 2*trade.reopened*self.FEE*trade.leverage
    trade.actualPNL = trade.getPNL() + trade.accumulatingSubtradePNL - feeLosses

if __name__=='__main__':
  manager = TradeManager()
  manager.startTrade("BONK-USDT", 0.000000510, 3, 0.0000004, 50, ORDER_CONFIG.MARKET|ORDER_CONFIG.SHORT)