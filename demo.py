#!/usr/bin/env python3
"""
Скрипт для демонстрации функционала научному руководителю
"""

import os
import pandas as pd
from datetime import datetime

def show_demo():
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ АНАЛИЗА КОИНТЕГРАЦИИ")
    print("=" * 60)
    
    # Показываем структуру проекта
    print("\n1. СТРУКТУРА ПРОЕКТА:")
    print("   📁 pair-trading/")
    print("   ├── 📁 src/           # Модули анализа")
    print("   ├── 📁 data/          # Исторические данные") 
    print("   ├── 📁 results/       # Результаты анализа")
    print("   ├── 📁 scripts/       # Вспомогательные скрипты")
    print("   └── 📁 tests/         # Тесты")
    
    # Показываем информацию о данных
    print("\n2. ДАННЫЕ ДЛЯ АНАЛИЗА:")
    if os.path.exists('data/stocks_prices.csv'):
        data = pd.read_csv('data/stocks_prices.csv', index_col=0, parse_dates=True)
        print(f"   • Акций: {data.shape[1]}")
        print(f"   • Торговых дней: {data.shape[0]}")
        print(f"   • Период: {data.index[0].strftime('%Y-%m-%d')} - {data.index[-1].strftime('%Y-%m-%d')}")
        print(f"   • Примеры акций: {', '.join(data.columns.tolist()[:3])}...")
    else:
        print("   • Данные не найдены. Запустите scripts/download_data.py")
    
    # Показываем последние результаты
    print("\n3. РЕЗУЛЬТАТЫ АНАЛИЗА:")
    results_files = [f for f in os.listdir('results') if f.endswith('.txt')]
    if results_files:
        latest_result = max(results_files)
        with open(f'results/{latest_result}', 'r', encoding='utf-8') as f:
            content = f.read()
            print("   📊 Последний анализ:")
            for line in content.split('\n'):
                if line.strip():
                    print(f"      {line}")
    else:
        print("   • Результаты не найдены. Запустите python main.py")
    
    print("\n4. ЗАПУСК АНАЛИЗА:")
    print("   • python main.py          # Полный анализ")
    print("   • python demo.py          # Эта демонстрация")
    print("   • python scripts/download_data.py # Загрузка данных")
    
    print("\n" + "=" * 60)
    print("Для подробного анализа запустите: python main.py")
    print("=" * 60)

if __name__ == "__main__":
    show_demo()