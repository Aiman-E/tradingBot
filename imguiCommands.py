import imgui
from trade import *
from tradingBot import *
import numpy as np

_selectedTrade = ""
_sideLong = False
_sideShort = False
_trade = Trade(0, 0, 0, 0, 0, 0, 0, 0)

def imguiTrade(bot:TradingBot):
  windowSize = imgui.get_window_size()
  imgui.begin_child("Trades", windowSize[0] * 0.2, windowSize[1] * 0.4, True)
  imgui.text("Trades") 
  imgui.separator()
  imguiTradeList(bot)
  imgui.end_child()

  imgui.same_line(spacing=20)

  imgui.begin_child("Details", 0.0, imgui.get_window_size()[1] * 0.4, True)
  imgui.text("DETAILS")
  imgui.separator()
  imguiTradeDetails(bot)
  imgui.end_child()

def imguiTradeList(bot:TradingBot):
  global _selectedTrade
  
  for i in bot.trades: 
    for j in bot.trades[i]:
      if imgui.selectable(j.symbol, _selectedTrade == i)[1]:
        _selectedTrade = i
    
    

def imguiTradeDetails(bot:TradingBot):
  if _selectedTrade == '': return
  windowSize = imgui.get_window_size()
  imgui.begin_child(bot.trades[_selectedTrade][0].symbol, windowSize[0] *0.4, 0.0, True)
  imgui.text(bot.trades[_selectedTrade][0].symbol.capitalize())
  imgui.separator()
  imgui.text(f"ID: {str(bot.trades[_selectedTrade][0].id)}")
  imgui.text(f"Current Price: {bot.trades[_selectedTrade][0].currentPrice}")
  imgui.text(f"Entry: {bot.trades[_selectedTrade][0].entry}")
  imgui.text(f"Margin: {bot.trades[_selectedTrade][0].margin}")
  imgui.text(f"Volume: {bot.trades[_selectedTrade][0].volume}")
  imgui.text(f"Loss: {bot.trades[_selectedTrade][0].loss}")
  imgui.text(f"Leverage: {bot.trades[_selectedTrade][0].leverage}")
  imgui.text(f"config: {bot.trades[_selectedTrade][0].config}")
  imgui.text(f"Subtrade: {bot.trades[_selectedTrade][0].subtrade}")
  imgui.text(f"Subtrade Threshhold: {bot.trades[_selectedTrade][0].subtradeThreshold}")
  imgui.end_child()

  imgui.same_line(spacing=20)

  imgui.begin_child("Adjust", 0.0, windowSize[1]* 0.35), True
  loss = imgui.input_text(' : Loss', str(bot.trades[_selectedTrade][0].loss), 256, flags = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
  if loss[0]: 
    bot.adjustParam("loss", _selectedTrade, float(loss[1]))

  threshold = imgui.input_text(' : Threshold', str(bot.trades[_selectedTrade][0].subtradeThreshold), 256, flags = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
  if threshold[0]:
    bot.adjustParam("threshold", _selectedTrade, float(threshold[1]))
  
  imgui.end_child()

def imguiOpenOrder(bot:TradingBot):
  global _sideLong, _sideShort, _trade
  imgui.push_text_wrap_pos(0.0)
  imgui.text(str(_trade))
  imgui.pop_text_wrap_pos()
  x = imgui.input_text(' : Symbol', str(_trade.symbol), 256)
  if x[0]:
    _trade.setSymbol(x[1])

  x = imgui.input_text(' : entry', str(_trade.entry), 256)
  if x[0]:
    _trade.setEntry(x[1])

  x = imgui.input_text(' : margin', str(_trade.margin), 256)
  if x[0]:
    _trade.setMargin(x[1])

  x = imgui.input_text(' : loss', str(_trade.loss), 256)
  if x[0]:
    _trade.setLoss(x[1])

  x = imgui.input_text(' : lev', str(_trade.leverage), 256)
  if x[0]:
    _trade.setLev(x[1])

  if imgui.radio_button("Long", _sideLong):
    _sideLong = True
    _sideShort = False
    _trade.setConfig(ORDER_CONFIG.LONG | ORDER_CONFIG.MARKET)
  imgui.same_line()
  if imgui.radio_button("Short", _sideShort):
    _sideShort = True
    _sideLong = False
    _trade.setConfig(ORDER_CONFIG.SHORT | ORDER_CONFIG.MARKET)

  if imgui.button("Open position"):
    bot.startTrade(_trade.symbol, float(_trade.entry), float(_trade.margin), float(_trade.loss),
                   int(_trade.leverage), _trade.config)

  imgui.same_line(spacing=20)

  if imgui.button("Fetch position"):
    bot.fetchTrade(_trade.symbol, float(_trade.loss), int(_trade.leverage), _trade.config)