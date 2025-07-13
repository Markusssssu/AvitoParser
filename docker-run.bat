@echo off
chcp 65001 >nul

echo 🤖 Запуск Telegram Avito Bot через Docker
echo ==========================================

REM Проверяем, установлен ли Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker не установлен. Установите Docker и попробуйте снова.
    pause
    exit /b 1
)

REM Проверяем, установлен ли Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose не установлен. Установите Docker Compose и попробуйте снова.
    pause
    exit /b 1
)

echo ✅ Docker и Docker Compose найдены

REM Создаем директорию для данных MongoDB
echo 📁 Создание директории для данных...
if not exist "dockerdata\db" mkdir "dockerdata\db"

REM Останавливаем существующие контейнеры
echo 🛑 Остановка существующих контейнеров...
docker-compose down

REM Собираем и запускаем контейнеры
echo 🔨 Сборка и запуск контейнеров...
docker-compose up --build -d

REM Проверяем статус контейнеров
echo 📊 Проверка статуса контейнеров...
timeout /t 5 /nobreak >nul
docker-compose ps

echo.
echo 🎉 Бот запущен!
echo 📱 Найдите бота в Telegram и отправьте /start
echo.
echo 📋 Полезные команды:
echo   docker-compose logs -f bot     # Просмотр логов бота
echo   docker-compose logs -f updates # Просмотр логов обновлений
echo   docker-compose down           # Остановка бота
echo   docker-compose restart        # Перезапуск бота
echo.
echo 🔗 MongoDB доступна на localhost:27017
echo.
pause 