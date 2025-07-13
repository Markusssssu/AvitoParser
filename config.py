#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Конфигурационный файл для Telegram бота Avito Tracker
"""

# Токен вашего Telegram бота
BOT_TOKEN = "7921913612:AAGXyzzI9xUK--5r2N9LFi7VdqEw9ibfmjo"

# Настройки базы данных
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'avito_bot'
}

# Настройки парсера
PARSER_CONFIG = {
    'debug': False,  # Включить отладку парсера
    'delay_between_requests': 1,  # Задержка между запросами в секундах
    'max_retries': 3  # Максимальное количество попыток при ошибке
}

# Настройки уведомлений
NOTIFICATION_CONFIG = {
    'check_interval': 120,  # Интервал проверки новых объявлений в секундах (2 минуты)
    'max_ads_per_message': 5  # Максимальное количество объявлений в одном сообщении
} 