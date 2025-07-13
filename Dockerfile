FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /bot

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем пользователя для безопасности
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /bot
USER botuser

# Команда по умолчанию
CMD ["python", "run_bot.py"]