from bingxapi import ORDER_CONFIG

class Trade():
  id = ""
  symbol = ""
  entry = 0.0
  amount = 0.0
  loss = 0.0
  leverage = 0.0
  config = None
  subtrade = None
  subtradeThreshold = .06

  def __init__(self, id, symbol, entry, amount, loss, lev, config) -> None:
    self.id = id
    self.symbol = symbol
    self.entry = entry
    self.amount = amount
    self.loss = loss
    self.leverage = lev
    self.config = config

  def setSymbol(self, x):
    self.symbol = x

  def setEntry(self, x):
    self.entry = x

  def setAmount(self, x):
    self.amount = x
    
  def setLoss(self, x):
    self.loss = x

  def setLev(self, x):
    self.leverage = x  
  
  def setSubtrade(self, subtrade):
    self.subtrade = subtrade

  def getTradeSign(self):
    return 1 if self.config & ORDER_CONFIG.LONG else -1

  def getSubtradeThreshold(self):
    if self.config & ORDER_CONFIG.LONG:
      return self.subtrade.entry*(1+self.subtradeThreshold/100)
    return self.subtrade.entry*(1-self.subtradeThreshold/100)
    
  def __str__(self) -> str:
    return f"<TRADE ID:{self.id}> symbol:{self.symbol} - entry:{self.entry} - amount:{self.amount} - loss:{self.loss} - leverage:{self.leverage} - config:{self.config}"
