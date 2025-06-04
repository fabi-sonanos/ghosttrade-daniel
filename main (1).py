import os
import time
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = os.getenv("BITVAVO_API_KEY", "demo_key")
API_SECRET = os.getenv("BITVAVO_API_SECRET", "demo_secret")
CONTROL_TOKEN = os.getenv("CONTROL_TOKEN", "supersecuretoken")

trading_enabled = True

@app.route("/")
def index():
    return "Ghosttrade API is running."

@app.route("/order", methods=["POST"])
def order():
    data = request.get_json()
    token = data.get("token")
    if token != CONTROL_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    action = data.get("action")
    coin = data.get("coin")
    amount = data.get("amount")

    # Simulierter Trade-Ausgabe
    print(f"[API] Empfangen: {action.upper()} {amount}€ {coin}")
    return jsonify({
        "status": "received",
        "action": action,
        "coin": coin,
        "amount": amount
    })

def simulate_trading():
    while trading_enabled:
        print("Ghosttrade heartbeat – verbunden mit API.")
        time.sleep(60)

if __name__ == "__main__":
    thread = threading.Thread(target=simulate_trading)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))