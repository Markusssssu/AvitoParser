#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль для создания экземпляра Telegram бота
"""

import telebot
from config import BOT_TOKEN

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN) 