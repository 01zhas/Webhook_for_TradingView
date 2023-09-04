from telegram import Bot

class TelegramNotifier:
    def __init__(self, api_token, chat_id):
        self.bot = Bot(token=api_token)
        self.chat_id = chat_id

    def send_message(self, message):
        try:
            self.bot.send_message(chat_id=self.chat_id, text=message)
        except Exception as e:
            print(f"Ошибка при отправке сообщения в Telegram: {e}")

if __name__ == "__main__":
    # Пример использования
    api_token = 'Ваш_API_токен_Telegram'
    chat_id = 'Ваш_ID_чата_Telegram'
    telegram_notifier = TelegramNotifier(api_token, chat_id)

    # Пример отправки сообщения
    telegram_notifier.send_message('Привет из вашего торгового бота!')
