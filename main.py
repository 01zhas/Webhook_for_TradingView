import time
from config import API_KEY_BINANCE, API_SECRET_BINANCE, TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID, SEC_KEY
from binance_api import BinanceAPI
from telegram_notifier import TelegramNotifier

from flask import Flask, request

#TODO: Отправлять профит от ордера в телеграмм. Отправлять ошибку в телеграмм. 

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        if request.method == "POST":
            data = request.get_json()
            key = data["sec_key"]
            print(f"{key}:{SEC_KEY}")
            if key == SEC_KEY:
                order = binance_api.open_position(data["ticker"], data["action"])
                telegram_notifier.send_message(order)
                return "Sent alert", 200

            else:
                print("Alert Received & Refused! (Wrong Key)")
                return "Refused alert", 400

    except Exception as e:
        print("Error:\n>", e)
        return "Error", 400

if __name__ == "__main__":
    binance_api = BinanceAPI(API_KEY_BINANCE, API_SECRET_BINANCE)
    telegram_notifier = TelegramNotifier(TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID)
    app.run(host='0.0.0.0', port=5000)  # Запускаем сервер Flask
