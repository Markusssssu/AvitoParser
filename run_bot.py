#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для запуска Telegram бота Avito Tracker
"""

import sys
import os
from config import BOT_TOKEN

def check_config():
    """Проверяем конфигурацию бота"""
    print("🔍 Проверка конфигурации...")
    
    if not BOT_TOKEN:
        print("❌ Ошибка: Токен бота не найден!")
        return False
    
    if not BOT_TOKEN.startswith("7921913612:"):
        print("❌ Ошибка: Неверный формат токена!")
        return False
    
    print("✅ Токен бота найден и корректный")
    return True

def main():
    """Основная функция запуска"""
    print("🤖 Запуск Telegram бота Avito Tracker")
    print("=" * 50)
    
    # Проверяем конфигурацию
    if not check_config():
        sys.exit(1)
    
    try:
        # Импортируем и запускаем бота
        from main import bot
        print("✅ Бот успешно инициализирован")
        print("🚀 Запускаем бота...")
        print("📱 Найдите бота в Telegram и отправьте /start")
        print("⏹️  Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        bot.polling(none_stop=True, timeout=60)
        
    except KeyboardInterrupt:
        print("\n⏹️  Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 