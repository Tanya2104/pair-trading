# cointegration_tester.py  
# Тестирование коинтеграции между парами акций
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class CointegrationTester:
    
    def __init__(self, significance_level=0.05):
        self.significance_level = significance_level
    
    def check_stationarity(self, series: pd.Series, name: str = "") -> Dict:
        """Проверка стационарности временного ряда"""
        try:
            result = adfuller(series.dropna())
            return {
                'adf_statistic': result[0],
                'p_value': result[1],
                'is_stationary': result[1] <= self.significance_level,
                'critical_values': result[4]
            }
        except Exception as e:
            logger.error(f"Ошибка ADF теста для {name}: {e}")
            return {}
    
    def engle_granger_test(self, x: pd.Series, y: pd.Series, x_name: str, y_name: str) -> Dict:
        """Тест Энгла-Грэнджера на коинтеграцию"""
        try:
            # Проверяем что ряды I(1)
            x_diff_test = self.check_stationarity(x.diff().dropna(), f"{x_name}_diff")
            y_diff_test = self.check_stationarity(y.diff().dropna(), f"{y_name}_diff")
            
            if not (x_diff_test.get('is_stationary', False) and 
                    y_diff_test.get('is_stationary', False)):
                return {'is_cointegrated': False, 'error': 'Ряды не I(1)'}
            
            # Регрессия y на x
            X = add_constant(x)
            model = OLS(y, X).fit()
            
            # Проверяем остатки на стационарность
            residuals = model.resid
            resid_test = self.check_stationarity(residuals, f"residuals_{x_name}_{y_name}")
            
            is_cointegrated = resid_test.get('is_stationary', False)
            
            return {
                'is_cointegrated': is_cointegrated,
                'p_value': resid_test.get('p_value', 1),
                'alpha': model.params[0],
                'beta': model.params[1],
                'residuals': residuals,
                'r_squared': model.rsquared,
                'residuals_test': resid_test
            }
            
        except Exception as e:
            logger.error(f"Ошибка теста для {x_name}-{y_name}: {e}")
            return {'is_cointegrated': False, 'error': str(e)}
    
    def find_cointegrated_pairs(self, price_data: pd.DataFrame) -> List[Dict]:
        """Поиск всех коинтегрированных пар"""
        tickers = price_data.columns.tolist()
        cointegrated_pairs = []
        
        logger.info(f"Анализируем {len(tickers)} акций...")
        
        total_pairs = len(tickers) * (len(tickers) - 1) // 2
        logger.info(f"Всего возможных пар: {total_pairs}")
        
        analyzed_pairs = 0
        for i, ticker1 in enumerate(tickers):
            for ticker2 in tickers[i+1:]:
                try:
                    analyzed_pairs += 1
                    if analyzed_pairs % 10 == 0:
                        logger.info(f"Проанализировано {analyzed_pairs}/{total_pairs} пар...")
                    
                    # Берем данные без пропусков
                    pair_data = price_data[[ticker1, ticker2]].dropna()
                    
                    if len(pair_data) < 50:
                        continue
                    
                    result = self.engle_granger_test(
                        pair_data[ticker1], 
                        pair_data[ticker2],
                        ticker1, 
                        ticker2
                    )
                    
                    if result.get('is_cointegrated', False):
                        pair_info = {
                            'ticker_x': ticker1,
                            'ticker_y': ticker2,
                            'p_value': result['p_value'],
                            'alpha': result['alpha'],
                            'beta': result['beta'],
                            'r_squared': result['r_squared'],
                            'residuals': result['residuals']
                        }
                        cointegrated_pairs.append(pair_info)
                        logger.info(f"Коинтегрированная пара: {ticker1}-{ticker2} (p-value: {result['p_value']:.4f})")
                        
                except Exception as e:
                    logger.warning(f"Ошибка для пары {ticker1}-{ticker2}: {e}")
                    continue
        
        # Сортируем по p-value (лучшие первые)
        cointegrated_pairs.sort(key=lambda x: x['p_value'])
        logger.info(f"Найдено {len(cointegrated_pairs)} коинтегрированных пар")
        
        return cointegrated_pairs