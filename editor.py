import imgui
from trade import *
from tradingBot import *
import numpy as np

class Editor():
  _selectedTrade = ""
  _sideLong = False
  _sideShort = False
  _trade = Trade(0, 0, 0, 0, 0, 0, 0, 0)


  def __init__(self) -> None:
    pass

  def tradeList(self, bot:TradingBot):    
    imgui.text("Trades") 
    imgui.separator()
    for i in bot.manager.trades: 
        if imgui.selectable(bot.manager.trades[i].symbol, self._selectedTrade == i)[1]:
          self._selectedTrade = i
      
      

  def tradeDetails(self, bot:TradingBot):
    if self._selectedTrade == '': return

    imgui.text("DETAILS")
    imgui.separator()
    
    imgui.text(bot.manager.trades[self._selectedTrade].symbol.capitalize())
    imgui.separator()
    imgui.text(f"ID: {str(bot.manager.trades[self._selectedTrade].id)}")
    imgui.text(f"Current Price: {bot.manager.trades[self._selectedTrade].currentPrice}")
    imgui.text(f"Entry: {bot.manager.trades[self._selectedTrade].entry}")
    imgui.text(f"Margin: {bot.manager.trades[self._selectedTrade].margin}")
    imgui.text(f"Volume: {bot.manager.trades[self._selectedTrade].volume}")
    imgui.text(f"Loss: {bot.manager.trades[self._selectedTrade].loss}")
    imgui.text(f"Leverage: {bot.manager.trades[self._selectedTrade].leverage}")
    imgui.text(f"config: {bot.manager.trades[self._selectedTrade].config}")
    imgui.text(f"Subtrade: {bot.manager.trades[self._selectedTrade].subtrade}")
    imgui.text(f"Subtrade reopened: {bot.manager.trades[self._selectedTrade].reopened}")
    imgui.text(f"Subtrade Threshhold: {bot.manager.trades[self._selectedTrade].subtradeThreshold}")
    imgui.text(f"subtrade trigger PNL: {bot.manager.trades[self._selectedTrade].subtradeTriggerPNL}")
    imgui.text(f"PNL: {bot.manager.trades[self._selectedTrade].getPNL()}")
    imgui.text(f"Profit: {bot.manager.trades[self._selectedTrade].getProfit()}")


  def tradeSettings(self, bot:TradingBot):
    if self._selectedTrade == '': return

    loss = imgui.input_text(' : Loss', str(bot.manager.trades[self._selectedTrade].loss), 256, flags = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
    if loss[0]: 
      bot.manager.adjustParam("loss", self._selectedTrade, float(loss[1]))

    threshold = imgui.input_text(' : Threshold', str(bot.manager.trades[self._selectedTrade].subtradeThreshold), 256, flags = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
    if threshold[0]:
      bot.manager.adjustParam("threshold", self._selectedTrade, float(threshold[1]))

    triggerpnl = imgui.input_text(' : triggerPNL', str(bot.manager.trades[self._selectedTrade].subtradeTriggerPNL), 256, flags = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
    if triggerpnl[0]:
      bot.manager.adjustParam("triggerPNL", self._selectedTrade, float(triggerpnl[1]))


  def openOrder(self, bot:TradingBot, lock):
    imgui.text("Open order") 
    imgui.push_text_wrap_pos(0.0)
    imgui.text(str(self._trade))
    imgui.pop_text_wrap_pos()
    x = imgui.input_text(' : Symbol', str(self._trade.symbol), 256)
    if x[0]:
      self._trade.setSymbol(x[1])

    x = imgui.input_text(' : entry', str(self._trade.entry), 256)
    if x[0]:
      self._trade.setEntry(x[1])

    x = imgui.input_text(' : margin', str(self._trade.margin), 256)
    if x[0]:
      self._trade.setMargin(x[1])

    x = imgui.input_text(' : loss', str(self._trade.loss), 256)
    if x[0]:
      self._trade.setLoss(x[1])

    x = imgui.input_text(' : lev', str(self._trade.leverage), 256)
    if x[0]:
      self._trade.setLev(x[1])

    if imgui.radio_button("Long", self._sideLong):
      self._sideLong = True
      self._sideShort = False
      self._trade.setConfig(ORDER_CONFIG.LONG | ORDER_CONFIG.MARKET)
    imgui.same_line()
    if imgui.radio_button("Short", self._sideShort):
      self._sideShort = True
      self._sideLong = False
      self._trade.setConfig(ORDER_CONFIG.SHORT | ORDER_CONFIG.MARKET)

    if imgui.button("Open position"):
      lock.acquire()
      bot.manager.startTrade(self._trade.symbol, float(self._trade.entry), float(self._trade.margin), float(self._trade.loss),
                    int(self._trade.leverage), self._trade.config)
      lock.release()

    imgui.same_line(spacing=20)

    if imgui.button("Fetch position"):
      lock.acquire()
      bot.manager.fetchTrade(self._trade.symbol, float(self._trade.loss), int(self._trade.leverage), self._trade.config)
      lock.release()

    imgui.same_line(spacing=20)
    
    if imgui.button("Load positions"):
      lock.acquire()
      bot.manager.load()
      lock.release()

  def closeOrder(self, bot:TradingBot, lock):
    if self._selectedTrade == '': return
    if imgui.button("Close trade"):
        lock.acquire()
        temp = self._selectedTrade
        self._selectedTrade = ""
        bot.manager.endTrade(temp)
        lock.release()

def imguiCommands(*args, **kwargs):
    bot = args[1]['bot']
    lock = args[1]['lock']
    editor = args[1]['editor']

    imgui.begin("Bot")
    windowSize = imgui.get_window_size()

    # LIST
    imgui.begin_child("Trades", windowSize[0] * 0.2, windowSize[1] * 0.6, True)
    editor.tradeList(bot)
    imgui.end_child()

    imgui.same_line(spacing=20)

    # DETIALS
    imgui.begin_child("Details", 0.0, windowSize[1] * 0.6, True)

    imgui.begin_child(editor._selectedTrade, windowSize[0] * 0.3, 0.0, True)
    editor.tradeDetails(bot)
    editor.closeOrder(bot, lock)
    imgui.end_child() #-------END details subsection

    imgui.same_line(spacing=20)

    # Settings
    imgui.begin_child("Settings", 0.0, 0.0, True)
    editor.tradeSettings(bot)
    imgui.end_child()

    imgui.end_child() #-------END Details super section


    # Order
    imgui.begin_child("OpenOrder", 0.0, 0.0, True)   
    editor.openOrder(bot, lock)
    imgui.end_child()

    imgui.end()

