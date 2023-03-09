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
        BOT.tick()
        LOCK.release()
        time.sleep(0.3)
        
    