# main.py
# Главный файл для запуска приложения
#!/usr/bin/env python3

import logging
import pandas as pd
import os
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Основная функция запуска анализа"""
    logger.info("=== ЗАПУСК АНАЛИЗА КОИНТЕГРАЦИИ ===")
    
    try:
        # 1. Загрузка данных
        logger.info("1. Загрузка данных...")
        
        # Проверяем существование файла с данными
        if not os.path.exists('data/stocks_prices.csv'):
            logger.error("Файл data/stocks_prices.csv не найден")
            logger.info("Сначала запустите scripts/download_data.py для загрузки данных")
            return
        
        from src.data_fetcher import DataFetcher
        fetcher = DataFetcher()
        price_data = fetcher.load_from_csv('data/stocks_prices.csv')
        
        if price_data is None:
            logger.error("Не удалось загрузить данные")
            return
        
        # Подготовка данных
        clean_data = fetcher.prepare_data(min_data_points=50)
        logger.info(f"Данные готовы: {clean_data.shape[1]} акций")
        
        # 2. Покажем базовую информацию о данных
        logger.info("2. Базовая информация о данных:")
        logger.info(f"   - Период: {clean_data.index[0].strftime('%Y-%m-%d')} до {clean_data.index[-1].strftime('%Y-%m-%d')}")
        logger.info(f"   - Торговых дней: {len(clean_data)}")
        logger.info(f"   - Акции: {', '.join(clean_data.columns.tolist()[:5])}...")
        
        logger.info("=== БАЗОВЫЙ АНАЛИЗ ЗАВЕРШЕН ===")
        logger.info("Для полного анализа коинтеграции дополните функционал")
        
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main()