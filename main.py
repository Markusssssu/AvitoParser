import db
import utils
import os
from bot_instance import bot


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 
                          '🤖 <b>Доброе утро/день/вечер! Я ваш помощник по имени Джанго.</b>\n\n'
                          'Я создан, чтобы служить вам верой и правдой '
                          'по вашим поисковым запросам.\n\n'
                          '📋 <b>Что умею (пух не собираю):</b>\n'
                          '• /add - Добавить новую ссылку\n'
                          '• /list - Показать весь список отслеживаний\n'
                          '• /delete - Удалить отслеживание\n\n'
                          'Нажмите на значок "/" для просмотра доступных команд.',
                          parse_mode='HTML')


# # # Adding search # # #
@bot.message_handler(commands=['add'])
def add_search(message):
    bot.send_message(message.chat.id,
                     '🔍 <b>Добавление нового отслеживания</b>\n\n'
                     'Укажите ссылку на поисковую выдачу Avito с нужными вам фильтрами.\n\n'
                     '⚠️ <b>Важно:</b> Используется мобильная версия Avito.\n'
                     '📝 <b>Пример:</b>\n'
                     '<code>https://m.avito.ru/moskva/avtomobili/s_probegom</code>\n\n'
                     'Если у вас десктопная версия - добавьте <code>m.</code> в начало ссылки.',
                     parse_mode='HTML', disable_web_page_preview=True)
    msg = bot.send_message(message.chat.id, '⏳ Ожидаю ссылку...')

    bot.register_next_step_handler(msg, waiting_url_step)


# Waiting url
def waiting_url_step(message):
    search_url = message.text
    # На случай, если пользователь отравит такое сообщение: "https://avito.ru/kazan/avto/vaz бла бла"
    search_url = search_url.split(' ')[0]
    # УБРАНО: search_url = search_url.lower()

    # Нормализуем ссылку
    normalized_url = utils.normalize_avito_url(search_url)
    if normalized_url != search_url:
        bot.send_message(message.chat.id, f'ℹ️ Ссылка была автоматически исправлена:\n<code>{normalized_url}</code>', parse_mode='HTML')
    search_url = normalized_url

    if not utils.check_avito_url(search_url):
        msg = bot.send_message(message.chat.id, '❌ <b>Некорректная ссылка.</b>\n\nПроверьте правильность ссылки и попробуйте снова.', parse_mode='HTML')
        return

    try:
        if db.is_link_already_tracking_by_user(message.chat.id, search_url):
            bot.send_message(message.chat.id, '⚠️ <b>Вы уже отслеживаете данную ссылку.</b>', parse_mode='HTML')
            return
    except:
        msg = bot.send_message(message.chat.id, '🔴 <b>Ошибка сервера.</b>\n\nПовторите попытку позже.', parse_mode='HTML')
        return

    try:
        search_url = search_url.split(' ')[0]
        db.save_url_to_temp(message.chat.id, search_url)
    except:
        msg = bot.send_message(message.chat.id, '🔴 <b>Ошибка сервера.</b>\n\nПовторите попытку позже.', parse_mode='HTML')
        return

    msg = bot.send_message(message.chat.id, '📝 <b>Укажите название для поиска.</b>\n\nНапример: "Автомобили в Москве" или "Игры PS4"', parse_mode='HTML')
    bot.register_next_step_handler(msg, select_search_name_step)


# Waiting name for tracking results
def select_search_name_step(message):
    search_name = message.text
    # TODO Validate title (search_name)
    try:
        search_url = db.get_temp_url(message.chat.id)
    except:
        bot.send_message(message.chat.id, 'Ошибка сервера. Повторите попытку позже.')
        return

    if db.save_url(message.chat.id, search_url, search_name):
        bot.send_message(message.chat.id, 
                        f'✅ <b>Отслеживание добавлено!</b>\n\n'
                        f'📋 <b>Название:</b> {search_name}\n'
                        f'🔗 <b>Ссылка:</b> {search_url}\n\n'
                        f'Теперь мой хозяин я буду собирать пух... ой то есть объявление с авито для вас.',
                        parse_mode='HTML', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, '🔴 <b>Произошла ошибка при добавлении.</b>\n\nПовторите попытку позже.', parse_mode='HTML')


# # # End adding search # # #

def send_tracking_urls_list(uid):
    user_tracking_urls_list = db.get_users_tracking_urls_list(uid)

    if not user_tracking_urls_list:
        bot.send_message(uid, '📭 <b>У вас нет активных отслеживаний.</b>\n\nИспользуйте /add для добавления нового отслеживания.', parse_mode='HTML')
        return

    msg = '📋 <b>Ваши отслеживания:</b>\n\n'
    i = 1
    for url in user_tracking_urls_list:
        msg += f'{i}. <b>{url["name"]}</b>\n'
        msg += f'🔗 <code>{url["url"]}</code>\n\n'
        i += 1

    bot.send_message(uid, msg, parse_mode='HTML', disable_web_page_preview=True)


# # # Deleting search # # #
@bot.message_handler(commands=['delete'])
def deleting_search(message):
    if not db.get_users_tracking_urls_list(message.chat.id):
        bot.send_message(message.chat.id, '📭 <b>У вас нет активных отслеживаний.</b>', parse_mode='HTML')
        return
    send_tracking_urls_list(uid=message.chat.id)
    msg = bot.send_message(message.chat.id, '🗑️ <b>Отправьте порядковый номер удаляемой ссылки.</b>', parse_mode='HTML')
    bot.register_next_step_handler(msg, waiting_num_to_delete)


def waiting_num_to_delete(message):
    try:
        delete_url_index_in_list = int(message.text)
    except:
        bot.send_message(message.chat.id, '❌ <b>Отправьте только число.</b>', parse_mode='HTML')
        return

    if delete_url_index_in_list <= 0:
        bot.send_message(message.chat.id, '❌ <b>Порядковый номер должен быть больше нуля.</b>', parse_mode='HTML')
        return

    if db.delete_url_from_tracking(message.chat.id, delete_url_index_in_list):
        bot.send_message(message.chat.id, '✅ <b>Отслеживание удалено!</b>', parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, '🔴 <b>Ошибка сервера.</b>\n\nПовторите попытку позже.', parse_mode='HTML')


# # # End deleting search # # #

# # # Send list of tracking urls # # #
@bot.message_handler(commands=['list'])
def send_list(message):
    send_tracking_urls_list(message.chat.id)


# # # End send list of tracking urls # # #


if __name__ == '__main__':
    bot.polling(none_stop=True)
