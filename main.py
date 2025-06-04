import os
import time
import threading
from flask import Flask, request, jsonify

try:
    from bitvavo import Bitvavo
    BITVAVO_AVAILABLE = True
except Exception as e:
    print("[INIT ERROR] Bitvavo import failed:", e)
    BITVAVO_AVAILABLE = False

app = Flask(__name__)

API_KEY = os.getenv("BITVAVO_API_KEY", "")
API_SECRET = os.getenv("BITVAVO_API_SECRET", "")
CONTROL_TOKEN = os.getenv("CONTROL_TOKEN", "gh0st-trade-safe42")

if BITVAVO_AVAILABLE and API_KEY and API_SECRET:
    try:
        bitvavo = Bitvavo({
            'APIKEY': API_KEY,
            'APISECRET': API_SECRET,
            'RESTURL': 'https://api.bitvavo.com/v2',
            'WSURL': 'wss://ws.bitvavo.com/v2/',
            'ACCESSWINDOW': 10000,
            'DEBUGGING': False
        })
        bitvavo_ready = True
    except Exception as e:
        print("[BITVAVO INIT ERROR]", e)
        bitvavo_ready = False
else:
    bitvavo_ready = False

@app.route("/")
def index():
    if bitvavo_ready:
        return "✅ Ghosttrade LIVE – Bitvavo angebunden."
    else:
        return "⚠️ Ghosttrade aktiv, aber Bitvavo nicht verbunden."

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "bitvavo_connected": bitvavo_ready}), 200

@app.route("/order", methods=["POST"])
def order():
    if not bitvavo_ready:
        return jsonify({"error": "Bitvavo not ready"}), 503

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

        print(f"[TRADE] {action.upper()} {amount} EUR {coin}")

        result = bitvavo.placeOrder(coin + "-EUR", {
            'side': action,
            'orderType': 'market',
            'amount': str(amount)
        })

        return jsonify({"status": "executed", "exchange": result})

    except Exception as e:
        print("[ERROR] /order failed:", e)
        return jsonify({"error": "Execution failed", "details": str(e)}), 500

def heartbeat():
    while True:
        print("💡 Ghosttrade läuft – Heartbeat aktiv.")
        time.sleep(60)

if __name__ == "__main__":
    print("🚀 Starte Ghosttrade...")
    if not bitvavo_ready:
        print("❗ Achtung: Bitvavo-Verbindung NICHT aktiv.")
    thread = threading.Thread(target=heartbeat)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))