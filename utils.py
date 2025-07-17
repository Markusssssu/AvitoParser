def check_avito_url(avito_url):
    from urllib.parse import urlparse
    url_parts = urlparse(avito_url)
    return url_parts.netloc == 'm.avito.ru' and len(url_parts.path) > 1


def get_img_file_by_url(url):
    from fake_useragent import UserAgent
    import requests
    ua = UserAgent()

    if url[:2] == '//':
        url = url.replace('//', 'https://')

    try:
        file = requests.get(url=url, headers={
            'User-Agent': ua.random
        }).content
        return file
    except:
        return None


def normalize_avito_url(avito_url):
    """
    Приводит ссылку Avito к мобильному формату, не меняя путь и параметры фильтров.
    Удаляет только явные трекеры (utm_*, ref, clid и т.п.).
    """
    from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
    import re

    avito_url = avito_url.strip()
    if not avito_url.startswith('http') and not avito_url.startswith('HTTP'):
        avito_url = 'https://' + avito_url

    parsed = urlparse(avito_url)
    netloc = parsed.netloc
    path = parsed.path
    query = parsed.query

    # Исправляем netloc на мобильную версию, если нужно (без изменения регистра)
    if netloc.startswith('www.'):
        netloc = netloc[4:]
    if netloc == 'avito.ru':
        netloc = 'm.avito.ru'
    elif netloc == 'm.avito.ru':
        pass
    else:
        # Если вообще не avito, не трогаем
        return avito_url

    # Оставляем все параметры, кроме явных трекеров
    qs = parse_qsl(query, keep_blank_values=True)
    filtered_qs = []
    for k, v in qs:
        if k.startswith('utm_') or k in ['ref', 'clid', 'src', 'context', 'from', 'user']:
            continue
        filtered_qs.append((k, v))

    # Удаляем лишние слэши в конце
    path = re.sub(r'/+$', '', path)

    new_url = urlunparse((
        parsed.scheme,
        netloc,
        path,
        '',
        urlencode(filtered_qs, doseq=True),
        ''
    ))
    return new_url
