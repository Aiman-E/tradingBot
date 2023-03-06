from multiprocessing import Process, Lock
from multiprocessing.managers import BaseManager, NamespaceProxy
import types
import time
import imgui

from tradingBot import *
from context import Context
from editor import *

class BotManager(BaseManager): pass

def Proxy(target):
    def __getattr__(self, key):
        result = self._callmethod('__getattribute__', (key,))
        if isinstance(result, types.MethodType):
            def wrapper(*args, **kwargs):
                self._callmethod(key, args)
            return wrapper
        return result

    dic = {'types': types, '__getattr__': __getattr__}
    proxy_name = target.__name__ + "Proxy"
    ProxyType = type(proxy_name, (NamespaceProxy,), dic) 
    ProxyType._exposed_ = tuple(dir(target))

    return ProxyType

BotProxy = Proxy(TradingBot)

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


def main(b, lock, editor):  
    CONTEXT = Context()
    
    while not CONTEXT.shouldClose():
        CONTEXT.render(imguiCommands, bot=b, lock=lock, editor = editor)
        

if __name__=='__main__':
    BotManager.register("BOT", TradingBot, BotProxy)
    manager = BotManager()
    manager.start()

    BOT = manager.BOT()
    LOCK = Lock()
    editor = Editor()

    mainProccess = Process(target=main, args=(BOT, LOCK, editor))
    mainProccess.start()


    while 1:
        LOCK.acquire()
        BOT.update()
        LOCK.release()
        time.sleep(0.3)
    