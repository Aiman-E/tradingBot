
from bingX.perpetual.v2 import Perpetual


APIKEY = "2Ohbn3NBvAiBSAbjtwzAKMOXvpcSqCtdXxqK9XFHF56ouSjcai56CHydcFpI0g5IStjh3GbGd9YftZAIew"
SECRETKEY = "RgVYyNap7rCIa5mkD5DehhcIPnoIdeJvIJ89kBOL4sMs94sKxMqfQydrGhJofRGSSVY5Go6vmXZvIKrvhMLXg"
CLIENT = Perpetual(APIKEY, SECRETKEY)


# Define the symbol and trade sizes
symbol = 'USTC-USDT'
long_trade_size = 0.01
short_trade_size = 0.02

# Initialize the long and short positions
long_position = None
short_position = None

# Enter into a long position
response = CLIENT.order(symbol=symbol, side='buy', quantity=long_trade_size)
if response['status'] == 'filled':
    long_position = response['result']

CLIENT.get_open_positions()
while True:
    # Check the unrealized profit/loss of the long position
    long_unrealized_pnl = connector.get_position_unrealized_pnl(long_position['position_id'])
    long_loss = long_unrealized_pnl / long_position['initial_margin'] * 100
    if long_loss <= -10:
        # Enter into a short position next to the long position
        response = connector.market_order(symbol=symbol, side='sell', quantity=short_trade_size)
        if response['status'] == 'filled':
            short_position = response['result']
        break

# Check the unrealized profit/loss of the short position
while True:
    short_unrealized_pnl = connector.get_position_unrealized_pnl(short_position['position_id'])
    if short_unrealized_pnl <= 0:
        # Close the short position
        response = connector.market_order(symbol=symbol, side='buy', quantity=short_trade_size)
        break