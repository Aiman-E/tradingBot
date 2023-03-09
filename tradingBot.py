from tradeManager import *

class TradingBot():
  def __init__(self) -> None:
    self.manager = TradeManager()
    logger.add("./log.txt")

  def tick(self):      
    if self.manager.updatePrices() == -1: return -1

    try:
      for trade in self.manager.trades.values():
          # Adds subtrade if not exist
          if not trade.subtrade:
            s = trade.getTradeSign()
            logger.debug(f"Price: {trade.currentPrice} - Loss: {trade.loss}")
            if s*trade.currentPrice <= s*trade.loss:
              if self.manager.startSubTrade(trade) == -1:
                logger.warning("Subtrade not accomplished")
                return -1
              logger.success("Subtrade accomplished")
              continue

          # check subtrade
          else:
            s = trade.getTradeSign() #equality flips when multiplied with minus
            logger.debug(f"Price: {s*trade.subtrade.currentPrice} - threshold: {s*trade.getSubtradeThreshold()}")

            if ((s*trade.subtrade.currentPrice >= s*trade.getSubtradeThreshold() and
                not trade.reopened) or
                trade.getPNL()>0.0):
              if self.manager.endSubtrade(trade.symbol) == -1:
                logger.warning("Closing subtrade failure")
                return -1
              logger.success("Subtrade closed")
              trade.reopened = False

            elif trade.subtrade.getPNL() > trade.subtradeTriggerPNL:
              if self.manager.endSubtrade(trade.symbol) == -1:
                logger.warning("Closing subtrade failure")
                return -1
              
              logger.success("Subtrade closed")
              trade.reopened = True

    except KeyboardInterrupt as e:
      logger.error(e)
    except Exception as e:
      logger.error(e)
    

if __name__ == '__main__':
  bot = TradingBot()
  # bot.manager.startTrade("BONK-USDT", 0.000000476, 2, 0.0000005, 50, ORDER_CONFIG.MARKET | ORDER_CONFIG.SHORT)
  bot.manager.load()
  # bot.fetchTrade(symbol, 22387.0, 150, ORDER_CONFIG.SHORT  | ORDER_CONFIG.MARKET)
  # bot.startTrade(symbol2, price2, 2, price2 - price2*0.001, 50, ORDER_CONFIG.LONG  | ORDER_CONFIG.MARKET)
  while 1:
    bot.tick()
  
  