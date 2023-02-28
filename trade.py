from bingxapi import ORDER_CONFIG

class Trade():
  id = ""
  symbol = ""
  currentPrice = 0.0
  entry = 0.0
  margin = 0.0
  volume = 0.0
  loss = 0.0
  leverage = 0.0
  config = None
  subtrade = None
  subtradeThreshold = .2

  def __init__(self, id, symbol, entry, margin, volume, loss, lev, config) -> None:
    self.id = id
    self.symbol = symbol
    self.entry = entry
    self.currentPrice = entry
    self.margin = margin
    self.volume = volume
    self.loss = loss
    self.leverage = lev
    self.config = config

  def setSymbol(self, x):
    self.symbol = x

  def setEntry(self, x):
    self.entry = x

  def setCurrentPrice(self, x):
    self.currentPrice = x

  def setMargin(self, x):
    self.margin = x

  def setVolume(self, x):
    self.volume = x

  def setLoss(self, x):
    self.loss = x

  def setLev(self, x):
    self.leverage = x  

  def setConfig(self, x):
    self.config = x
  
  def setSubtrade(self, subtrade):
    self.subtrade = subtrade

  def setSubtradeThreshold(self, x):
    self.subtradeThreshold = x

  def getTradeSign(self):
    return 1 if self.config & ORDER_CONFIG.LONG else -1

  def getSubtradeThreshold(self):
    if self.config & ORDER_CONFIG.LONG:
      return self.subtrade.entry*(1+self.subtradeThreshold/100)
    return self.subtrade.entry*(1-self.subtradeThreshold/100)
    
  def __str__(self) -> str:
    return f"<TRADE ID:{self.id}> symbol:{self.symbol} - entry:{self.entry} - margin:{self.margin} - volume:{self.volume} - loss:{self.loss} - leverage:{self.leverage} - config:{self.config}"