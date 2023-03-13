from bot.tradeManager import *

class TradingBot():
  def __init__(self) -> None:
    self.manager = TradeManager()
    logger.add("log.txt")

  def openOrder(self, *args, **kwargs):
    s= ORDER_CONFIG.MARKET
    a = 's'
    s|= ORDER_CONFIG.LONG if kwargs['side'].lower() == 'long' else ORDER_CONFIG.SHORT
    self.manager.startTrade(kwargs['symbol'],
                            kwargs['entry'],
                            kwargs['margin'],
                            kwargs['loss'],
                            kwargs['leverage'],
                            s)

  def fetchOrder(self, *args, **kwargs):
    s= ORDER_CONFIG.MARKET
    a = 's'
    s|= ORDER_CONFIG.LONG if kwargs['side'].lower() == 'long' else ORDER_CONFIG.SHORT
    self.manager.fetchTrade(kwargs['symbol'],
                            kwargs['loss'],
                            kwargs['leverage'],
                            s)
  
  def loadTrades(self):
    self.manager.load()
    return [str(i) for i in self.manager.trades.keys()]
  
  def tradeDetails(self, x):
    if x:
      return self.manager.trades[x]
  
  def tradeEdit(self, param, symbol, value):
    self.manager.adjustParam(param, symbol, value)

  def tradeClose(self, symbol):
    self.manager.endTrade(symbol)

  def getStats(self, symbol):
    pnl = self.manager.trades[symbol].getPNL()
    profit = self.manager.trades[symbol].getProfit()
    actualPNL = self.manager.trades[symbol].actualPNL
    actualprofit = self.manager.trades[symbol].margin*(actualPNL/100)
    return {"pnl":[pnl, actualPNL], "profit":[profit, actualprofit]}

  def tick(self):      
    if self.manager.updatePrices() == -1: return -1

    try:
      for trade in self.manager.trades.values():
          s = trade.getTradeSign()
          # Adds subtrade if not exist
          if not trade.subtrade:
            logger.debug(f"Price: {trade.currentPrice} - Loss: {trade.loss}")
            if s*trade.currentPrice <= s*trade.loss:
              if self.manager.startSubTrade(trade) == -1:
                logger.warning(f"Subtrade({trade.symbol}) not accomplished")
                return -1
              logger.success(f"Subtrade({trade.symbol}) accomplished")
              continue

          # Check subtrade
          else:
            logger.debug(f"Price: {s*trade.subtrade.currentPrice} - threshold: {s*trade.getSubtradeThreshold()}")

            # Close subtrade
            if (s*trade.subtrade.currentPrice >= s*trade.getSubtradeThreshold()):
              if self.manager.endSubtrade(trade.symbol) == -1:
                logger.warning(f"Closing subtrade({trade.symbol}) failure")
                return -1
              logger.success(f"Subtrade({trade.symbol}) closed")

            # Reopen subtrade
            elif trade.subtrade.getPNL() > trade.subtradeTriggerPNL:
              if self.manager.endSubtrade(trade.symbol) == -1:
                logger.warning(f"Reopening subtrade({trade.symbol}) failure")
                return -1
              
              logger.success(f"Subtrade({trade.symbol}) closed")
              trade.setLoss(trade.currentPrice)

              if self.manager.startSubTrade(trade) == -1:
                logger.warning(f"Subtrade({trade.symbol}) not reopened")
                return -1
              logger.success(f"Subtrade({trade.symbol}) reopened")

    except Exception as e:
      logger.error(e)
    

if __name__ == '__main__':
  bot = TradingBot()
  # bot.manager.startTrade("BTC-USDT", 20307.5, 2, 20305.5, 150, ORDER_CONFIG.MARKET | ORDER_CONFIG.LONG)
  # bot.manager.load()
  # bot.manager.fetchTrade("ADA-USDT", 22387.0, 100, ORDER_CONFIG.SHORT  | ORDER_CONFIG.MARKET)
  # bot.startTrade(symbol2, price2, 2, price2 - price2*0.001, 50, ORDER_CONFIG.LONG  | ORDER_CONFIG.MARKET)
  while 1:
    bot.tick()
  
  