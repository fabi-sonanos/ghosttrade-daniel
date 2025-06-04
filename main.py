import os
import time
import threading
from flask import Flask, request, jsonify
from bitvavo import Bitvavo

app = Flask(__name__)

API_KEY = os.getenv("BITVAVO_API_KEY")
API_SECRET = os.getenv("BITVAVO_API_SECRET")
CONTROL_TOKEN = os.getenv("CONTROL_TOKEN", "gh0st-trade-safe42")

bitvavo = Bitvavo({
    'APIKEY': API_KEY,
    'APISECRET': API_SECRET,
    'RESTURL': 'https://api.bitvavo.com/v2',
    'WSURL': 'wss://ws.bitvavo.com/v2/',
    'ACCESSWINDOW': 10000,
    'DEBUGGING': False
})

auto_enabled = True

@app.route("/")
def index():
    return "✅ Ghosttrade Autotrading läuft."

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "autotrade": auto_enabled}), 200

@app.route("/order", methods=["POST"])
def order():
    try:
        data = request.get_json(force=True)
        token = data.get("token")
        if token != CONTROL_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401

        action = data.get("action", "").lower()
        coin = data.get("coin", "").upper()
        amount = float(data.get("amount", 0))

        if action not in ["buy", "sell"] or amount <= 0 or not coin:
            return jsonify({"error": "Invalid parameters"}), 400

        print(f"[MANUAL TRADE] {action.upper()} {amount} EUR {coin}")
        result = bitvavo.placeOrder(coin + "-EUR", {
            'side': action,
            'orderType': 'market',
            'amount': str(amount)
        })

        return jsonify({"status": "executed", "exchange": result})

    except Exception as e:
        print("[ERROR] /order failed:", e)
        return jsonify({"error": "Execution failed", "details": str(e)}), 500

def autotrader():
    while auto_enabled:
        try:
            # Beispiel: 5€ ETH kaufen alle 12 Minuten (Test-Simulation)
            print("🤖 Autotrade wird ausgeführt: Kaufe 5€ ETH")
            result = bitvavo.placeOrder("ETH-EUR", {
                'side': 'buy',
                'orderType': 'market',
                'amount': "5"
            })
            print("✅ Trade erfolgreich:", result)
        except Exception as e:
            print("⚠️ Autotrade-Fehler:", e)
        time.sleep(720)  # 12 Minuten Pause (5€ x 5 Trades = 60–90€/12h Ziel)

if __name__ == "__main__":
    print("🚀 Ghosttrade Autotrading startet...")
    thread = threading.Thread(target=autotrader)
    thread.daemon = True
    thread.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))