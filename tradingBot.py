from tradeManager import *

class TradingBot():
  def __init__(self) -> None:
    self.manager = TradeManager()
    logger.add("./log.txt")

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
              trade.reopened = False

            # Reopen subtrade
            elif trade.subtrade.getPNL() > trade.subtradeTriggerPNL:
              if self.manager.endSubtrade(trade.symbol) == -1:
                logger.warning(f"Reopening subtrade({trade.symbol}) failure")
                return -1
              
              logger.success(f"Subtrade({trade.symbol}) closed")
              trade.reopened = True
              trade.setLoss(trade.currentPrice)

              if self.manager.startSubTrade(trade) == -1:
                logger.warning(f"Subtrade({trade.symbol}) not reopened")
                return -1
              logger.success(f"Subtrade({trade.symbol}) reopened")

#2023-03-09 20:28:25.657
    except KeyboardInterrupt as e:
      logger.error(e)
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
  
  