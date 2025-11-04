import yfinance as yf
import pandas as pd

print("Начинаем загрузку данных")

#1. Загружем список популярных американских акций
tickers = [
    'AAPL',    # Apple
    'MSFT',    # Microsoft
    'GOOGL',   # Google
    'AMZN',    # Amazon
    'META',    # Meta (Facebook)
    'TSLA',    # Tesla
    'NVDA',    # NVIDIA
    'JPM',     # JPMorgan
    'JNJ',     # Johnson & Johnson
    'V',       # Visa
    'PG',      # Procter & Gamble
    'UNH',     # UnitedHealth
    'HD',      # Home Depot
    'DIS',     # Disney
    'BAC',     # Bank of America
    'MA',      # Mastercard
    'CVX',     # Chevron
    'XOM',     # Exxon Mobil
]

print(f"Загружаем данные для {len(tickers)} акций")

try:
    # Загружаем данные за 1 год
    data = yf.download(tickers, period="1y", progress=True)
    
     # Проверяем какие колонки есть
    if 'Adj Close' in data.columns.levels[0]:
        prices = data['Adj Close']
        print("Используем Adj Close")
    elif 'Close' in data.columns.levels[0]:
        prices = data['Close'] 
        print("Используем Close (Adj Close не доступен)")
    else:
        print("Ни Close, ни Adj Close не найдены")
        print("Доступные колонки:", list(data.columns.levels[0]))
        exit()
    
    print(f"Успешно загружено!")
    print(f"Размер данных: {prices.shape}")
    print(f"Период: {prices.index[0].strftime('%Y-%m-%d')} - {prices.index[-1].strftime('%Y-%m-%d')}")
    print(f"Всего торговых дней: {len(prices)}")
    
    # Показываем первые строки
    print(f"\nПервые 5 строк данных:")
    print(prices.head())
    
    # Сохраняем
    prices.to_csv('data/stocks_prices.csv')
    print(f"\nДанные сохранены в 'stocks_prices.csv'")
    print("Файл перезаписан (старые данные удалены)")
    
    # Быстрая проверка качества
    print(f"\nПроверим качество данных:")
    missing_data = prices.isnull().sum()
    print("Пропуски по акциям:")
    for ticker, missing in missing_data.items():
        if missing > 0:
            print(f"   {ticker}: {missing} пропусков")
        else:
            print(f"   {ticker}: нет пропусков")
            
except Exception as e:
    print(f"Ошибка: {e}")