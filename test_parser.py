#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый скрипт для проверки работы обновленного парсера Avito
"""

from parserr.parserr import get_ads_list, debug_page_structure
import requests


def test_parser():
    """Тестируем парсер на разных URL"""
    
    # Тестовые URL для проверки
    test_urls = [
        "https://m.avito.ru/moskva/avtomobili",
        "https://m.avito.ru/sankt-peterburg/avtomobili",
        "https://m.avito.ru/kazan/avtomobili",
        "https://m.avito.ru/novosibirsk/avtomobili"
    ]
    
    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"Тестируем URL: {url}")
        print(f"{'='*60}")
        
        try:
            # Получаем объявления с отладкой
            ads = get_ads_list(url, debug=True)
            
            print(f"\nНайдено объявлений: {len(ads)}")
            
            if ads:
                print("\nПервые 3 объявления:")
                for i, ad in enumerate(ads[:3], 1):
                    print(f"\n{i}. ID: {ad['id']}")
                    print(f"   Заголовок: {ad['title']}")
                    print(f"   Цена: {ad['price']}")
                    print(f"   URL: {ad['url']}")
                    print(f"   Изображение: {ad['img']}")
            else:
                print("Объявления не найдены!")
                
        except Exception as e:
            print(f"Ошибка при парсинге {url}: {e}")
        
        print(f"\n{'-'*60}")


def test_specific_url(url):
    """Тестируем конкретный URL"""
    print(f"Тестируем конкретный URL: {url}")
    
    try:
        ads = get_ads_list(url, debug=True)
        print(f"Найдено объявлений: {len(ads)}")
        
        if ads:
            print("\nВсе найденные объявления:")
            for i, ad in enumerate(ads, 1):
                print(f"\n{i}. ID: {ad['id']}")
                print(f"   Заголовок: {ad['title']}")
                print(f"   Цена: {ad['price']}")
                print(f"   URL: {ad['url']}")
                print(f"   Изображение: {ad['img']}")
        else:
            print("Объявления не найдены!")
            
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    print("Тестирование обновленного парсера Avito")
    print("=" * 60)
    
    # Тестируем общие URL
    test_parser()
    
    # Можно также протестировать конкретный URL
    # test_specific_url("https://m.avito.ru/moskva/avtomobili/toyota") 