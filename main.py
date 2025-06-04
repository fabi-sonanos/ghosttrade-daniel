import os
import time
import threading
from flask import Flask

app = Flask(__name__)

API_KEY = os.getenv("BITVAVO_API_KEY", "demo_key")
API_SECRET = os.getenv("BITVAVO_API_SECRET", "demo_secret")

@app.route("/")
def index():
    return f"Ghosttrade läuft mit API-Key {API_KEY[:4]}... (gekürzt)"

def simulate_trading():
    while True:
        print("Simulierter Trade läuft...")
        print(f"Verwende API_KEY: {API_KEY[:4]}... (gekürzt)")
        print("→ Einstieg, Analyse, Ausstieg... Profit kalkuliert.\n")
        time.sleep(60)

if __name__ == "__main__":
    # Starte Trading-Loop in separatem Thread
    trading_thread = threading.Thread(target=simulate_trading)
    trading_thread.daemon = True
    trading_thread.start()

    # Starte Webserver für Fly.io
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))