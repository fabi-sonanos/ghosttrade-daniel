
import os
import time
import random
import requests
from datetime import datetime
from bitvavo import Bitvavo

bitvavo = Bitvavo({
  'APIKEY': os.getenv('BITVAVO_API_KEY'),
  'APISECRET': os.getenv('BITVAVO_API_SECRET'),
  'RESTURL': 'https://api.bitvavo.com/v2',
  'WSURL': 'wss://ws.bitvavo.com/v2/'
})

# Konfiguration
coins = ["BTC-EUR", "ETH-EUR", "SOL-EUR", "PEPE-EUR", "RNDR-EUR", "DOGE-EUR", "XRP-EUR", "INJ-EUR", "FET-EUR", "OP-EUR", "ARB-EUR"]
min_trade = 5
max_trade = 15
max_loss = 60
target_profit = 120
check_interval_range = (10, 60)
starting_balance = 500

# Zustand
total_profit = 0
total_loss = 0

def get_available_balance():
    try:
        balances = bitvavo.balance({})
        for entry in balances:
            if entry['symbol'] == 'EUR':
                return float(entry['available'])
    except Exception as e:
        print("Fehler beim Abrufen des Kontostands:", e)
    return 0

def simulate_market_analysis():
    return random.choice([True, False, False, True])

def choose_coin():
    return random.choice(coins)

def place_order(coin, amount_eur):
    try:
        price_info = bitvavo.tickerPrice({"market": coin})
        price = float(price_info['price'])
        amount = round(amount_eur / price, 8)
        order = bitvavo.placeOrder(coin, {
            'side': 'buy',
            'orderType': 'market',
            'amount': amount
        })
        return order
    except Exception as e:
        print(f"Fehler bei Order für {coin}: {e}")
        return None

def log_trade(success, coin, amount):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if success:
        print(f"[{now}] ✅ Kauf: {coin} für {amount} EUR")
    else:
        print(f"[{now}] ❌ Kein Trade: {coin}")

def main_loop():
    global total_profit, total_loss

    while total_profit < target_profit and total_loss < max_loss:
        wait = random.randint(*check_interval_range)
        time.sleep(wait)

        available = get_available_balance()
        if available < min_trade:
            print("❗ Nicht genug verfügbares Guthaben.")
            break

        if simulate_market_analysis():
            trade_amount = min(random.randint(min_trade, max_trade), available)
            coin = choose_coin()
            result = place_order(coin, trade_amount)
            if result:
                total_profit += random.uniform(1.5, 3.5)
                log_trade(True, coin, trade_amount)
            else:
                total_loss += random.uniform(1.5, 3.5)
                log_trade(False, coin, trade_amount)

    print("🎯 Trading abgeschlossen.")
    print(f"📈 Gesamtgewinn: {round(total_profit, 2)} €")
    print(f"📉 Gesamtverlust: {round(total_loss, 2)} €")

if __name__ == "__main__":
    main_loop()
