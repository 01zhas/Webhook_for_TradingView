from binance.client import Client

class BinanceAPI:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret, testnet=True)

    def __get_usdt_balance(self):
        try:
            # Получаем баланс всех активов
            account_info = self.client.futures_account()
            balances = account_info['assets']
            
            # Находим баланс USDT
            for balance in balances:
                if balance['asset'] == 'USDT':
                    return float(balance['walletBalance'])
            
            return 0.0  # Если USDT не найден, возвращаем 0.0
        except Exception as e:
            print(f"Ошибка при получении баланса USDT: {e}")
            return 0.0
    
    def __calculate_quantity_usdt(self, symbol, amount_usdt):
        try:
            # Получаем текущий курс обмена BTC/USDT
            ticker_price = self.client.futures_mark_price(symbol=symbol)['markPrice']
            
            # Рассчитываем количество BTC на основе баланса USDT и желаемого объема в USDT
            quantity = amount_usdt / float(ticker_price)
            return quantity
        except Exception as e:
            print(f"Ошибка при расчете количества: {e}")
            return None
    
    def open_position(self, symbol, action):
        amount_usdt = self.__get_usdt_balance() * 0.01
        try:
            # Устанавливаем маржинальное плечо на 20x (если необходимо)
            try:
                # Попробуем установить маржинальное плечо на 20x
                self.client.futures_change_leverage(symbol=symbol, leverage=20)
                amount_usdt = amount_usdt * 20
            except Exception as e:
                print(f"Не удалось установить маржинальное плечо на 20x: {e}")
                try:
                    # Если 20x недоступно, получаем список доступных уровней маржинального плеча
                    leverage_info = self.client.futures_leverage_bracket(symbol=symbol)
                    if len(leverage_info) > 0:
                        max_leverage = leverage_info[0]['leverage']
                        self.client.futures_change_leverage(symbol=symbol, leverage=max_leverage)
                        amount_usdt = amount_usdt * max_leverage
                    else:
                        print("Не удалось установить маржинальное плечо.")
                except Exception as e:
                    print(f"Ошибка при установке маржинального плеча: {e}")
            
            # Закрываем старую позицию
            msg = self.__close_position(symbol)
            
            # Определяем начальное округление
            rounding = 3
            
            while rounding >= 0:
                try:
                    quantity = round(self.__calculate_quantity_usdt(symbol, amount_usdt), rounding)
                    
                    if action == 'buy':
                        order = self.client.futures_create_order(
                            symbol=symbol,
                            side=Client.SIDE_BUY,
                            type=Client.ORDER_TYPE_MARKET,
                            quantity=quantity
                        )
                    elif action == 'sell':
                        order = self.client.futures_create_order(
                            symbol=symbol,
                            side=Client.SIDE_SELL,
                            type=Client.ORDER_TYPE_MARKET,
                            quantity=quantity
                        )
                    else:
                        raise ValueError("Недопустимое действие. Используйте 'buy' или 'sell'.")
                    
                    return msg
                except Exception as e:
                    rounding -= 1
                    if rounding < 0:
                        return f"Ошибка при размещении ордера: {e}"
        except Exception as e:
            print(f"Ошибка при размещении ордера: {e}")
            return f"Ошибка при размещении ордера: {e}"

    def __close_position(self, symbol):
        try:
            positions = self.client.futures_position_information()
            for position in positions:
                if position['symbol'] == symbol:
                    positionAmt = float(position['positionAmt'])
                    if positionAmt != 0:
                        if positionAmt > 0:
                            side = Client.SIDE_SELL
                        else:
                            side = Client.SIDE_BUY

                        # Создаем ордер для закрытия позиции
                        order = self.client.futures_create_order(
                            symbol=symbol,
                            side=side,
                            type=Client.ORDER_TYPE_MARKET,
                            quantity=abs(positionAmt),
                            recvWindow=5000
                        )

                        # Получаем информацию о сделках пользователя на фьючерсах
                        trades = self.client.futures_account_trades(symbol=symbol)

                        # Вычисляем PNL и ROI на основе сделок
                        pnl = 0.0
                        for trade in trades:
                            if trade['orderId'] == order['orderId']:
                                pnl += float(trade['realizedPnl'])

                        return f"{symbol}: {round(pnl)}$"
            return f"Открыта позиция по: {symbol}"
        except Exception as e:
            print(f"Ошибка при закрытии позиции: {e}")
            return f"Ошибка при закрытии позиции: {e}"


if __name__ == "__main__":
    # Пример использования
    api_key = 'Ваш_API_ключ_Binance'
    api_secret = 'Ваш_API_секрет_Binance'
    binance_api = BinanceAPI(api_key, api_secret)


    # Пример открытия позиции с указанным балансом в USDT
    symbol = 'BTCUSDT'
    order = binance_api.open_position(symbol, 'buy')
