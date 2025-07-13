#!/bin/bash

# Скрипт для запуска Telegram Avito Bot через Docker

echo "🤖 Запуск Telegram Avito Bot через Docker"
echo "=========================================="

# Проверяем, установлен ли Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и попробуйте снова."
    exit 1
fi

# Проверяем, установлен ли Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
    exit 1
fi

echo "✅ Docker и Docker Compose найдены"

# Создаем директорию для данных MongoDB
echo "📁 Создание директории для данных..."
mkdir -p dockerdata/db

# Останавливаем существующие контейнеры
echo "🛑 Остановка существующих контейнеров..."
docker-compose down

# Собираем и запускаем контейнеры
echo "🔨 Сборка и запуск контейнеров..."
docker-compose up --build -d

# Проверяем статус контейнеров
echo "📊 Проверка статуса контейнеров..."
sleep 5
docker-compose ps

echo ""
echo "🎉 Бот запущен!"
echo "📱 Найдите бота в Telegram и отправьте /start"
echo ""
echo "📋 Полезные команды:"
echo "  docker-compose logs -f bot     # Просмотр логов бота"
echo "  docker-compose logs -f updates # Просмотр логов обновлений"
echo "  docker-compose down           # Остановка бота"
echo "  docker-compose restart        # Перезапуск бота"
echo ""
echo "🔗 MongoDB доступна на localhost:27017" 