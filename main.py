from PySide6.QtCore import QObject, QThread, QMutex

from bot.tradingBot import TradingBot
from editor.editor import Editor
        
class BotWorker(QObject):
    def __init__(self, bot, lock):
        super(BotWorker, self).__init__()
        self.bot = bot
        self.lock = lock
    
    def run(self):
        while 1:
            self.lock.lock()
            self.bot.tick()
            self.lock.unlock()
            QThread.sleep(0.3)
            
            
if __name__=='__main__':
    LOCK = QMutex()
    BOT = TradingBot()
    botThread = QThread()
    botWorder = BotWorker(BOT, LOCK)

    botWorder.moveToThread(botThread)
    botThread.started.connect(botWorder.run)
    botThread.start()
    
    
    editor = Editor(LOCK)
    editor.setOpenAndFetchCallback(BOT.openOrder, BOT.fetchOrder)
    editor.setLoadCallback(BOT.loadTrades)
    editor.setDetailsCallback(BOT.tradeDetails)
    editor.setDetailsEditCallback(BOT.tradeEdit)
    editor.setTradeCloseCallback(BOT.tradeClose)


    while 1:
        editor.tick()
        editor.processEvents()