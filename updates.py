import db
from parserr.parserr import get_ads_list, get_new_ads
from bot_instance import bot
import time
from config import PARSER_CONFIG, NOTIFICATION_CONFIG


def send_updates():
    sce = db.get_search_collection_entries()

    for i in sce:
        tracking_urls = []
        for url in i['tracking_urls']:
            old_ads = url['ads']
            # Используем обновленный парсер с настройками из конфига
            actual_ads = get_ads_list(url['url'], debug=PARSER_CONFIG['debug'])
            new_ads = get_new_ads(actual_ads, old_ads)

            for n_a in new_ads:
                # Современная верстка в стиле Avito
                msg = f"""🏠 <b>Новое объявление</b>

📋 <b>{n_a['title'].rstrip()}</b>
💰 <b>{n_a['price'].rstrip()}</b>

🔗 <a href="{n_a['url']}">Смотреть на Avito</a>"""

                # Отправляем фото, если есть
                if n_a['img']:
                    try:
                        from utils import get_img_file_by_url
                        img_file = get_img_file_by_url(n_a['img'])
                        if img_file:
                            bot.send_photo(i['uid'], img_file, caption=msg, parse_mode='HTML')
                        else:
                            bot.send_message(i['uid'], msg, parse_mode='HTML', disable_web_page_preview=False)
                    except:
                        bot.send_message(i['uid'], msg, parse_mode='HTML', disable_web_page_preview=False)
                else:
                    bot.send_message(i['uid'], msg, parse_mode='HTML', disable_web_page_preview=False)

            url['ads'] = actual_ads
            tracking_urls.append(url)

            import random
            time.sleep(random.randint(1, 15) / 10 + PARSER_CONFIG['delay_between_requests'])

        db.set_actual_ads(i['uid'], tracking_urls)


if __name__ == '__main__':
    import schedule

    send_updates()
    schedule.every(NOTIFICATION_CONFIG['check_interval']).seconds.do(send_updates)

    while True:
        schedule.run_pending()
        time.sleep(1)
