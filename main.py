
from flask import Flask, request, jsonify
import os
from bitvavo import Bitvavo

bitvavo = Bitvavo({
    'APIKEY': os.getenv('BITVAVO_API_KEY'),
    'APISECRET': os.getenv('BITVAVO_API_SECRET')
})

app = Flask(__name__)

@app.route('/buy', methods=['POST'])
def buy_eth():
    try:
        data = request.get_json()
        amount_eur = float(data.get('amount', 5))  # default to 5 EUR if not provided

        # Get ETH-EUR price
        price_data = bitvavo.tickerPrice({'market': 'ETH-EUR'})
        eth_price = float(price_data['price'])

        # Calculate amount of ETH to buy
        eth_amount = round(amount_eur / eth_price, 8)

        # Place order
        response = bitvavo.placeOrder('ETH-EUR', {
            'side': 'buy',
            'orderType': 'market',
            'amount': str(eth_amount)
        })
        return jsonify({'status': 'success', 'order': response}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    return "Ghosttrade bot is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
