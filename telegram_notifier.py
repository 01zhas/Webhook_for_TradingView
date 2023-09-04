import telepot

class TelegramNotifier:
    def __init__(self, api_token, chat_id):
        self.bot = telepot.Bot(api_token)
        self.chat_id = chat_id

    def send_message(self, message):
        try:
            self.bot.sendMessage(self.chat_id, message)
        except Exception as e:
            print(f"Ошибка при отправке сообщения в Telegram: {e}")

if __name__ == "__main__":
    # Пример использования
    api_token = 'Ваш_токен'
    chat_id = 'Ваш_идентификатор_чата'
    telegram_notifier = TelegramNotifier(api_token, chat_id)

    # Пример отправки сообщения
    telegram_notifier.send_message('Привет из вашего торгового бота!')