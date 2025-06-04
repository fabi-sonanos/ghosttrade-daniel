import os
import time
import requests

API_KEY = os.getenv("BITVAVO_API_KEY")
API_SECRET = os.getenv("BITVAVO_API_SECRET")

def simulate_trade():
    print("Simulierter Trade läuft...")
    print(f"Verwende API_KEY: {API_KEY[:4]}... (gekürzt für Sicherheit)")
    print("→ Einstieg, Analyse, Ausstieg... Profit kalkuliert.")
    print("Fertig. Warte auf nächsten Zyklus.\n")

while True:
    simulate_trade()
    time.sleep(60)  # Warte 1 Minute zwischen Zyklen