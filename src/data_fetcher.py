# data_fetcher.py
# Загрузка финансовых данных с Yahoo Finance

import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class DataFetcher:
    """Класс для работы с данными о ценах акций"""
    
    def __init__(self):
        self.data = None
    
    def load_from_csv(self, filepath='stocks_prices.csv'):
        """Загрузка данных из CSV файла"""
        try:
            self.data = pd.read_csv(filepath, index_col=0, parse_dates=True)
            logger.info(f"Данные загружены: {self.data.shape[1]} акций, {self.data.shape[0]} дней")
            return self.data
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
            return None
    
    def prepare_data(self, min_data_points=50):
        """Подготовка данных для анализа"""
        if self.data is None:
            logger.error("Данные не загружены")
            return None
        
        # Удаляем акции с недостаточным количеством данных
        clean_data = self.data.dropna(axis=1, thresh=min_data_points)
        
        # Заполняем оставшиеся пропуски
        clean_data = clean_data.ffill().bfill()
        
        logger.info(f"После очистки: {clean_data.shape[1]} акций")
        return clean_data
    
    def get_tickers(self):
        """Получить список тикеров"""
        if self.data is not None:
            return self.data.columns.tolist()
        return []