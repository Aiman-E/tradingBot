import asyncio

from bingX.perpetual.v2 import Perpetual
from bingX.perpetual.v2 import market


APIKEY = "2Ohbn3NBvAiBSAbjtwzAKMOXvpcSqCtdXxqK9XFHF56ouSjcai56CHydcFpI0g5IStjh3GbGd9YftZAIew"
SECRETKEY = "RgVYyNap7rCIa5mkD5DehhcIPnoIdeJvIJ89kBOL4sMs94sKxMqfQydrGhJofRGSSVY5Go6vmXZvIKrvhMLXg"
CLIENT = Perpetual(APIKEY, SECRETKEY)


ASSET = "USTC-USDT"
PRICE = 0.0
LOSS = 40
PROFIT = 500
MARGIN = 1
LEV = 50

async def getPrice():
    price = await market.latest_price(CLIENT, "USTC-USDT")["price"]
    return  price