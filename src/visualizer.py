# visualizer.py
# Визуализация цен и спреда для пар акций
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class Visualizer:
    
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        self.fig_size = (12, 8)
    
    def plot_price_comparison(self, price_data: pd.DataFrame, pair: Dict):
        """График сравнения цен двух акций"""
        ticker_x = pair['ticker_x']
        ticker_y = pair['ticker_y']
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.fig_size)
        
        # Нормализованные цены
        norm_x = price_data[ticker_x] / price_data[ticker_x].iloc[0]
        norm_y = price_data[ticker_y] / price_data[ticker_y].iloc[0]
        
        ax1.plot(norm_x.index, norm_x, label=ticker_x, linewidth=2)
        ax1.plot(norm_y.index, norm_y, label=ticker_y, linewidth=2)
        ax1.set_title(f'Нормализованные цены: {ticker_x} vs {ticker_y}')
        ax1.set_ylabel('Нормализованная цена')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Исходные цены
        ax2.plot(price_data.index, price_data[ticker_x], label=ticker_x, alpha=0.7)
        ax2.plot(price_data.index, price_data[ticker_y], label=ticker_y, alpha=0.7)
        ax2.set_title(f'Исходные цены: {ticker_x} vs {ticker_y}')
        ax2.set_ylabel('Цена')
        ax2.set_xlabel('Дата')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_spread(self, pair: Dict):
        """График спреда коинтегрированной пары"""
        spread = pair['residuals']
        ticker_x = pair['ticker_x']
        ticker_y = pair['ticker_y']
        
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        ax.plot(spread.index, spread.values, label='Спред', linewidth=2, color='blue')
        ax.axhline(y=0, color='red', linestyle='--', alpha=0.7, label='Среднее')
        
        # Полосы стандартных отклонений
        std = spread.std()
        ax.axhline(y=std, color='orange', linestyle=':', alpha=0.6, label='+1 std')
        ax.axhline(y=-std, color='orange', linestyle=':', alpha=0.6, label='-1 std')
        ax.axhline(y=2*std, color='red', linestyle=':', alpha=0.4, label='+2 std')
        ax.axhline(y=-2*std, color='red', linestyle=':', alpha=0.4, label='-2 std')
        
        ax.set_title(f'Спред для пары {ticker_x}-{ticker_y}\n'
                    f'p-value: {pair["p_value"]:.4f}, R²: {pair["r_squared"]:.3f}')
        ax.set_ylabel('Значение спреда')
        ax.set_xlabel('Дата')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_top_pairs(self, cointegrated_pairs: List[Dict], top_n: int = 10):
        """Визуализация топ-N коинтегрированных пар"""
        if not cointegrated_pairs:
            logger.warning("Нет коинтегрированных пар для отображения")
            return
        
        top_pairs = cointegrated_pairs[:top_n]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # P-values
        pairs_names = [f"{p['ticker_x']}-{p['ticker_y']}" for p in top_pairs]
        p_values = [p['p_value'] for p in top_pairs]
        
        bars = ax1.bar(pairs_names, p_values, color='lightblue', alpha=0.7)
        ax1.axhline(y=0.05, color='red', linestyle='--', label='Уровень значимости 0.05')
        ax1.set_title('P-value коинтегрированных пар')
        ax1.set_ylabel('P-value')
        ax1.tick_params(axis='x', rotation=45)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Подсвечиваем значимые пары
        for bar, p_val in zip(bars, p_values):
            if p_val <= 0.05:
                bar.set_color('lightcoral')
        
        # R-squared
        r_squared = [p['r_squared'] for p in top_pairs]
        
        ax2.bar(pairs_names, r_squared, color='lightgreen', alpha=0.7)
        ax2.set_title('R² коинтегрированных пар')
        ax2.set_ylabel('R-squared')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()