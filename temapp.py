from flask import Flask, request

app = Flask(__name__)

# Constants
RISK_PER_TRADE = 10.0  # $10 risk per trade
ACCOUNT_BALANCE = 1000.0  # Example account balance (adjust to your actual balance)
PIP_VALUE_PER_LOT = 0.01  # Adjust based on your broker's pip value for BTCUSD

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        action = data.get('action')
        entry = float(data.get('entry'))
        sl = float(data.get('sl'))
        tp = float(data.get('tp'))

        risk_in_pips = abs(entry - sl)
        lot_size = RISK_PER_TRADE / (risk_in_pips * PIP_VALUE_PER_LOT)
        lot_size = max(0.01, min(lot_size, ACCOUNT_BALANCE / 1000.0))

        print(f"Received Trade: Symbol={symbol}, Action={action}, Entry={entry}, SL={sl}, TP={tp}")
        print(f"Calculated Lot Size: {lot_size:.2f}")

        return "Webhook received and lot size calculated", 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
