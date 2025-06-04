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
    return "Ghosttrade API is live."

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Service is running."}), 200

@app.route("/order", methods=["POST"])
def order():
    try:
        data = request.get_json(force=True)
        token = data.get("token")
        if token != CONTROL_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401

        action = data.get("action", "").lower()
        coin = data.get("coin", "").upper()
        amount = data.get("amount", 0)

        if not action or not coin or not isinstance(amount, (int, float)):
            return jsonify({"error": "Invalid parameters"}), 400

        print(f"[API] Order erhalten: {action.upper()} {amount}€ {coin}")
        return jsonify({
            "status": "received",
            "action": action,
            "coin": coin,
            "amount": amount
        })

    except Exception as e:
        print(f"[ERROR] API /order Exception: {e}")
        return jsonify({"error": "Server error"}), 500

def simulate_trading():
    while trading_enabled:
        print("Ghosttrade heartbeat – API-Modus aktiv.")
        time.sleep(60)

if __name__ == "__main__":
    thread = threading.Thread(target=simulate_trading)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))