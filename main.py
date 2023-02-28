from multiprocessing import Process
from multiprocessing.managers import BaseManager, NamespaceProxy
import types

import imgui

from tradingBot import *
from context import Context
from imguiCommands import *

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
    imgui.begin("Bot")

    imguiTrade(args[1]['bot'])

    imgui.begin_child("OpenOrder", 0.0, 0.0, True)
    imgui.text("Open order")    
    imguiOpenOrder(args[1]['bot'])
    imgui.end_child()

    imgui.end()


def main(b):  
    CONTEXT = Context()
    
    while not CONTEXT.shouldClose():
        CONTEXT.render(imguiCommands, bot=b)
        

if __name__=='__main__':
    BotManager.register("BOT", TradingBot, BotProxy)
    manager = BotManager()
    manager.start()

    BOT = manager.BOT()

    mainProccess = Process(target=main, args=(BOT,))
    mainProccess.start()


    while 1:
        BOT.update()
    