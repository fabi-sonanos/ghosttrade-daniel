
import os
import asyncio
import aiohttp
import time
from datetime import datetime
from bitvavo import Bitvavo

bitvavo = Bitvavo({
    'APIKEY': os.getenv("BITVAVO_API_KEY"),
    'APISECRET': os.getenv("BITVAVO_API_SECRET"),
    'RESTURL': 'https://api.bitvavo.com/v2',
    'WSURL': 'wss://ws.bitvavo.com/v2/',
    'ACCESSWINDOW': 10000,
    'DEBUGGING': False
})

TRADABLE_COINS = ["BTC-EUR", "ETH-EUR", "SOL-EUR", "PEPE-EUR", "RNDR-EUR", "DOGE-EUR", "XRP-EUR", "INJ-EUR", "FET-EUR", "OP-EUR", "ARB-EUR"]
TRADE_AMOUNT_EUR = 5
MAX_LOSS = -60
TARGET_PROFIT = 120
TRADE_LOG = []
START_BALANCE = 500

async def get_price(session, symbol):
    url = f"https://api.bitvavo.com/v2/market/{symbol}/ticker/price"
    async with session.get(url) as resp:
        data = await resp.json()
        return float(data["price"]) if "price" in data else None

async def trade_loop():
    async with aiohttp.ClientSession() as session:
        while True:
            total_profit = sum(t["profit"] for t in TRADE_LOG)
            if total_profit <= MAX_LOSS:
                print("Maximaler Verlust erreicht. Trading gestoppt.")
                break
            if total_profit >= TARGET_PROFIT:
                print("Zielgewinn erreicht!")
                break

            for coin in TRADABLE_COINS:
                price = await get_price(session, coin)
                if price:
                    print(f"[{datetime.utcnow()}] Preis {coin}: {price}")

                    response = bitvavo.placeOrder(coin, 'buy', 'market', { 'amount': str(TRADE_AMOUNT_EUR / price) })
                    buy_price = price

                    await asyncio.sleep(5)

                    current_price = await get_price(session, coin)
                    if current_price:
                        bitvavo.placeOrder(coin, 'sell', 'market', { 'amount': str(TRADE_AMOUNT_EUR / buy_price) })
                        profit = (current_price - buy_price) * (TRADE_AMOUNT_EUR / buy_price)
                        TRADE_LOG.append({"coin": coin, "buy": buy_price, "sell": current_price, "profit": profit})
                        print(f"Trade abgeschlossen: {coin} | Profit: {profit:.2f} EUR")

                await asyncio.sleep(10)  # Wartezeit bis zum nächsten Coin

async def main():
    await trade_loop()

if __name__ == "__main__":
    asyncio.run(main())
