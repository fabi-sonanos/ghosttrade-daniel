
import time
import random
import threading
from bitvavo import Bitvavo
import os

# Konfiguration über Umgebungsvariablen (für Sicherheit)
API_KEY = os.environ.get("BITVAVO_API_KEY")
API_SECRET = os.environ.get("BITVAVO_API_SECRET")

if not API_KEY or not API_SECRET:
    raise EnvironmentError("Bitvavo API_KEY oder API_SECRET fehlt!")

bitvavo = Bitvavo({
    'APIKEY': API_KEY,
    'APISECRET': API_SECRET,
    'RESTURL': 'https://api.bitvavo.com/v2',
    'WSURL': 'wss://ws.bitvavo.com/v2/',
    'ACCESSWINDOW': 10000,
    'DEBUGGING': False
})

# Konfigurationen
TRADING_PAIRS = ['BTC-EUR', 'ETH-EUR', 'SOL-EUR', 'PEPE-EUR', 'RNDR-EUR', 'DOGE-EUR', 'XRP-EUR']
MAX_INVEST = 15  # in EUR
MIN_INVEST = 5
STOP_LOSS = -60
PROFIT_TARGET = 120
TRADE_INTERVAL_MIN = 10  # Sekunden
TRADE_INTERVAL_MAX = 60 * 60  # Sekunden

total_profit = 0


def choose_strategy(pair):
    strategies = ['scalping', 'news', 'breakout', 'mean']
    return random.choice(strategies)


def simulate_news_impact(pair):
    return random.uniform(-2.0, 3.5)


def place_trade():
    global total_profit

    while True:
        pair = random.choice(TRADING_PAIRS)
        strategy = choose_strategy(pair)
        invest_amount = random.uniform(MIN_INVEST, MAX_INVEST)

        # Simulierter Gewinn/Verlust auf Basis Strategie
        if strategy == 'news':
            pnl = simulate_news_impact(pair)
        elif strategy == 'scalping':
            pnl = random.uniform(-0.5, 1.2)
        elif strategy == 'breakout':
            pnl = random.uniform(-1.5, 2.5)
        else:  # mean reversion
            pnl = random.uniform(-1.0, 1.5)

        # Gewinn in Euro berechnen
        profit = invest_amount * (pnl / 100.0)
        total_profit += profit

        print(f"Pair: {pair}, Strategy: {strategy}, Invested: €{invest_amount:.2f}, Profit: €{profit:.2f}, Total: €{total_profit:.2f}")

        if total_profit <= STOP_LOSS:
            print("❌ Stop-Loss erreicht. Trading wird gestoppt.")
            break
        if total_profit >= PROFIT_TARGET:
            print("✅ Gewinnziel erreicht. Trading abgeschlossen.")
            break

        time.sleep(random.randint(TRADE_INTERVAL_MIN, TRADE_INTERVAL_MAX))


def start_trading_loop():
    print("🤖 Trading-Bot gestartet...")
    trading_thread = threading.Thread(target=place_trade)
    trading_thread.start()


if __name__ == "__main__":
    start_trading_loop()
