#!/usr/bin/env python3
"""
Главный файл для запуска анализа коинтеграции
Полная версия с анализом коинтеграции
"""

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
    #Основная функция запуска анализа
    logger.info("Запуск анализа коинтеграции")
    
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
        
<<<<<<< HEAD
        logger.info("Базовый анализ завершён")
        logger.info("Для полного анализа коинтеграции дополните функционал")
=======
        # 3. Анализ коинтеграции
        logger.info("3. Поиск коинтегрированных пар...")
        from src.cointegration_tester import CointegrationTester
        tester = CointegrationTester(significance_level=0.05)
        cointegrated_pairs = tester.find_cointegrated_pairs(clean_data)
        
        if not cointegrated_pairs:
            logger.warning("Коинтегрированные пары не найдены")
            return
        
        # 4. Визуализация результатов
        logger.info("4. Визуализация результатов...")
        from src.visualizer import Visualizer
        viz = Visualizer()
        
        # Топ пар
        viz.plot_top_pairs(cointegrated_pairs, top_n=min(10, len(cointegrated_pairs)))
        
        # Детальный анализ лучших пар
        top_pairs_to_show = min(3, len(cointegrated_pairs))
        logger.info(f"\nТоп-{top_pairs_to_show} коинтегрированных пар:")
        for i in range(top_pairs_to_show):
            pair = cointegrated_pairs[i]
            logger.info(f"  {i+1}. {pair['ticker_x']}-{pair['ticker_y']}: "
                       f"p-value: {pair['p_value']:.4f}, R²: {pair['r_squared']:.3f}")
            
            viz.plot_price_comparison(clean_data, pair)
            viz.plot_spread(pair)
        
        # 5. Сохраняем результаты
        logger.info("5. Сохранение результатов...")
        save_results(cointegrated_pairs, clean_data)
        
        logger.info("=== АНАЛИЗ ЗАВЕРШЕН УСПЕШНО ===")
>>>>>>> feature/cointegration-analysis
        
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

def save_results(cointegrated_pairs, price_data):
    """Сохранение результатов анализа"""
    try:
        # Создаем папку для результатов
        os.makedirs('results', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Сохраняем список коинтегрированных пар
        pairs_df = pd.DataFrame([
            {
                'Ticker_X': p['ticker_x'],
                'Ticker_Y': p['ticker_y'],
                'P_Value': p['p_value'],
                'Alpha': p['alpha'],
                'Beta': p['beta'],
                'R_Squared': p['r_squared'],
                'Hedge_Ratio': p['beta']
            }
            for p in cointegrated_pairs
        ])
        
        results_file = f'results/cointegrated_pairs_{timestamp}.csv'
        pairs_df.to_csv(results_file, index=False)
        logger.info(f"Результаты сохранены в: {results_file}")
        
        # Сохраняем информацию о лучшей паре
        if cointegrated_pairs:
            best_pair = cointegrated_pairs[0]
            best_pair_file = f'results/best_pair_{timestamp}.txt'
            with open(best_pair_file, 'w', encoding='utf-8') as f:
                f.write(f"Лучшая коинтегрированная пара:\n")
                f.write(f"Пара: {best_pair['ticker_x']} - {best_pair['ticker_y']}\n")
                f.write(f"P-value: {best_pair['p_value']:.6f}\n")
                f.write(f"R²: {best_pair['r_squared']:.4f}\n")
                f.write(f"Alpha: {best_pair['alpha']:.4f}\n")
                f.write(f"Beta: {best_pair['beta']:.4f}\n")
                f.write(f"Hedge Ratio: {best_pair['beta']:.4f}\n")
            
            logger.info(f"Информация о лучшей паре сохранена в: {best_pair_file}")
            
    except Exception as e:
        logger.error(f"Ошибка при сохранении результатов: {e}")

if __name__ == "__main__":
    main()