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
    for i in bot.trades: 
      for j in bot.trades[i]:
        if imgui.selectable(j.symbol, self._selectedTrade == i)[1]:
          self._selectedTrade = i
      
      

  def tradeDetails(self, bot:TradingBot):
    if self._selectedTrade == '': return

    imgui.text("DETAILS")
    imgui.separator()
    
    imgui.text(bot.trades[self._selectedTrade][0].symbol.capitalize())
    imgui.separator()
    imgui.text(f"ID: {str(bot.trades[self._selectedTrade][0].id)}")
    imgui.text(f"Current Price: {bot.trades[self._selectedTrade][0].currentPrice}")
    imgui.text(f"Entry: {bot.trades[self._selectedTrade][0].entry}")
    imgui.text(f"Margin: {bot.trades[self._selectedTrade][0].margin}")
    imgui.text(f"Volume: {bot.trades[self._selectedTrade][0].volume}")
    imgui.text(f"Loss: {bot.trades[self._selectedTrade][0].loss}")
    imgui.text(f"Leverage: {bot.trades[self._selectedTrade][0].leverage}")
    imgui.text(f"config: {bot.trades[self._selectedTrade][0].config}")
    imgui.text(f"Subtrade: {bot.trades[self._selectedTrade][0].subtrade}")
    imgui.text(f"Subtrade Threshhold: {bot.trades[self._selectedTrade][0].subtradeThreshold}")


  def tradeSettings(self, bot:TradingBot):
    if self._selectedTrade == '': return

    loss = imgui.input_text(' : Loss', str(bot.trades[self._selectedTrade][0].loss), 256, flags = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
    if loss[0]: 
      bot.adjustParam("loss", self._selectedTrade, float(loss[1]))

    threshold = imgui.input_text(' : Threshold', str(bot.trades[self._selectedTrade][0].subtradeThreshold), 256, flags = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
    if threshold[0]:
      bot.adjustParam("threshold", self._selectedTrade, float(threshold[1]))


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
      bot.startTrade(self._trade.symbol, float(self._trade.entry), float(self._trade.margin), float(self._trade.loss),
                    int(self._trade.leverage), self._trade.config)
      lock.release()

    imgui.same_line(spacing=20)

    if imgui.button("Fetch position"):
      lock.acquire()
      bot.fetchTrade(self._trade.symbol, float(self._trade.loss), int(self._trade.leverage), self._trade.config)
      lock.release()

  def closeOrder(self, bot:TradingBot, lock):
    if self._selectedTrade == '': return
    if imgui.button("Close trade"):
        lock.acquire()
        temp = self._selectedTrade
        self._selectedTrade = ""
        bot.endTrade(temp)
        lock.release()