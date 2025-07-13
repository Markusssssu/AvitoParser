import json
import requests
import time
from bs4 import BeautifulSoup
from requests import RequestException


def get_proxy():
    proxy = requests.get(
        'https://gimmeproxy.com/api/getProxy?country=RU&get=true&supportsHttps=true&protocol=http')
    proxy_json = json.loads(proxy.content)
    if proxy.status_code != 200 and 'ip' not in proxy_json:
        raise RequestException
    else:
        return 'http://' + proxy_json['ip'] + ':' + proxy_json['port']


def get_html(url):
    import random
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Android 14; Mobile; rv:109.0) Gecko/121.0 Firefox/121.0'
    ]
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    proxy = {
        # 'https': get_proxy()
    }
    response = requests.get(url, headers=headers)
    return response.content


def debug_page_structure(html_content, url):
    """
    Функция для отладки структуры страницы
    """
    soup = BeautifulSoup(html_content, 'lxml')
    
    print(f"=== Отладка структуры страницы: {url} ===")
    
    # Проверяем основные селекторы
    selectors_to_test = [
        'article[data-marker="item"]',
        'div[data-marker="item"]',
        'article[class*="item"]',
        'div[class*="item"]',
        'article[class*="listing"]',
        'div[class*="listing"]',
        'article[class*="b-item"]',
        'div[class*="b-item"]'
    ]
    
    for selector in selectors_to_test:
        elements = soup.select(selector)
        print(f"Селектор '{selector}': найдено {len(elements)} элементов")
        
        if elements:
            # Показываем структуру первого элемента
            first_elem = elements[0]
            print(f"  Первый элемент: {first_elem.name} с классами: {first_elem.get('class', [])}")
            
            # Ищем заголовок
            title_elem = first_elem.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if title_elem:
                print(f"  Заголовок: {title_elem.get_text(strip=True)[:50]}...")
            
            # Ищем ссылку
            link_elem = first_elem.find('a', href=True)
            if link_elem:
                print(f"  Ссылка: {link_elem['href'][:50]}...")
    
    print("=== Конец отладки ===\n")


def get_ads_list(avito_search_url, debug=False):
    """
    :param avito_search_url: url like https://m.avito.ru/kazan/avtomobili/inomarki?pmax=200000&pmin=50000
    :param debug: включить отладку структуры страницы
    :return: ads list
    """
    html = get_html(avito_search_url)
    
    if debug:
        debug_page_structure(html, avito_search_url)
    
    soup = BeautifulSoup(html, 'lxml')
    
    # Пробуем разные селекторы для современной верстки Avito
    ads = []
    
    # Новые селекторы для современной верстки Avito
    selectors = [
        'article[data-marker="item"]',  # Основной селектор для объявлений
        'div[data-marker="item"]',      # Альтернативный селектор
        'article[class*="item"]',       # По частичному совпадению класса
        'div[class*="item"]',           # Альтернативный вариант
        'article[class*="listing"]',    # Еще один возможный вариант
        'div[class*="listing"]',        # Альтернативный вариант
    ]
    
    for selector in selectors:
        ads = soup.select(selector)
        if ads:
            break
    
    # Если ничего не найдено, пробуем старые селекторы
    if not ads:
        ads = soup.find_all('article', {'class': 'b-item'})
    
    ads_list = []
    for ad in ads:
        try:
            # Получаем ID объявления
            ad_id = ad.get('data-item-id') or ad.get('id') or ad.get('data-marker-id')
            if not ad_id:
                continue
                
            # Ищем ссылку на объявление
            ad_link = ad.find('a', href=True)
            if not ad_link:
                continue
                
            ad_url = ad_link['href']
            if not ad_url.startswith('http'):
                ad_url = 'https://m.avito.ru' + ad_url
            
            # Ищем заголовок объявления
            title_selectors = [
                'h3[data-marker="item-title"]',
                'h3[class*="title"]',
                'span[data-marker="item-title"]',
                'div[data-marker="item-title"]',
                'h3',
                'span[class*="title"]',
                'div[class*="title"]'
            ]
            
            ad_header = None
            for title_selector in title_selectors:
                title_elem = ad.select_one(title_selector)
                if title_elem:
                    ad_header = title_elem.get_text(strip=True)
                    break
            
            if not ad_header:
                continue
            
            # Ищем цену
            price_selectors = [
                'span[data-marker="item-price"]',
                'div[data-marker="item-price"]',
                'span[class*="price"]',
                'div[class*="price"]',
                'span[class*="cost"]',
                'div[class*="cost"]'
            ]
            
            ad_price = None
            for price_selector in price_selectors:
                price_elem = ad.select_one(price_selector)
                if price_elem:
                    ad_price = price_elem.get_text(strip=True)
                    break
            
            if not ad_price:
                ad_price = "Цена не указана"
            
            # Ищем изображение
            img_selectors = [
                'img[data-marker="item-photo"]',
                'img[class*="photo"]',
                'img[class*="image"]',
                'img',
                'div[class*="photo"] img',
                'div[class*="image"] img'
            ]
            
            ad_img = None
            for img_selector in img_selectors:
                img_elem = ad.select_one(img_selector)
                if img_elem and img_elem.get('src'):
                    ad_img = img_elem['src']
                    if ad_img.startswith('//'):
                        ad_img = 'https:' + ad_img
                    elif not ad_img.startswith('http'):
                        ad_img = 'https://' + ad_img
                    break
            
            # Проверяем, не является ли объявление премиум или выделенным
            is_premium = any([
                'premium' in str(ad.get('class', [])).lower(),
                'vip' in str(ad.get('class', [])).lower(),
                'highlight' in str(ad.get('class', [])).lower(),
                'promoted' in str(ad.get('class', [])).lower()
            ])
            
            # Добавляем объявление в список (исключаем премиум)
            if not is_premium:
                ads_list.append({
                    'id': ad_id,
                    'title': ad_header.replace(u'\xa0', u' '),
                    'price': ad_price.replace(u'\xa0', u' '),
                    'url': ad_url,
                    'img': ad_img
                })
                
        except Exception as e:
            # Пропускаем объявления с ошибками парсинга
            if debug:
                print(f"Ошибка при парсинге объявления: {e}")
            continue
    
    return ads_list


def get_new_ads(new, old):
    _ = []
    for ad in new:
        if ad not in old:
            _.append(ad)
    return _
