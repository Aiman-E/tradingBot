import threading

import imgui

from bingxapi import BingxClient
from context import Context

LOCK = threading.Lock()
context = client = None
price = 0.0

def updatePrice():
    global price, client
    while 1:
        LOCK.acquire()
        price = client.getPrice()
        LOCK.release()

def imguiCommands():
    global price
    imgui.begin("Bot")
    imgui.text(f"Price is: {price}")
    imgui.end()

def main():
    global context, client
    LOCK.acquire()
    context = Context()
    client = BingxClient()
    LOCK.release()
    
    while not context.shouldClose():
        context.render(externalImgui=imguiCommands)


if __name__=='__main__':
    threads = [threading.Thread(target=main), threading.Thread(target=updatePrice)]
    for t in threads:
        t.start()

    for t in threads:
        t.join()