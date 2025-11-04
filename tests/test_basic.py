#Базовые тесты для проверки функционала


import unittest
import pandas as pd
import numpy as np
import os

class TestBasicFunctionality(unittest.TestCase):
    
    def test_data_file_exists(self):
        #Проверка существования файла с данными
        self.assertTrue(os.path.exists('data/stocks_prices.csv'), 
                       "Файл data/stocks_prices.csv должен существовать")
    
    def test_data_loading(self):
        #Проверка загрузки данных
        try:
            from src.data_fetcher import DataFetcher
            fetcher = DataFetcher()
            data = fetcher.load_from_csv('data/stocks_prices.csv')
            self.assertIsNotNone(data, "Данные должны загружаться")
            if data is not None:
                self.assertGreater(len(data), 0, "Данные не должны быть пустыми")
        except Exception as e:
            self.fail(f"Ошибка загрузки данных: {e}")

if __name__ == '__main__':
    unittest.main()