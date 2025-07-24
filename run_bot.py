from main import bot
import time
import traceback
import threading
from updates import send_updates
from config import NOTIFICATION_CONFIG


def updates_worker():
    while True:
        try:
            send_updates()
        except Exception as e:
            print(f"🔴 Ошибка в updates_worker: {e}")
            traceback.print_exc()
        time.sleep(NOTIFICATION_CONFIG['check_interval'])

def run_bot():
    # Запускаем обновления в отдельном потоке
    threading.Thread(target=updates_worker, daemon=True).start()
    while True:
        try:
            print("🟢 Бот Джанго запущен | " + time.strftime("%Y-%m-%d %H:%M:%S"))
            bot.infinity_polling()
        except Exception as e:
            print(f"🔴 Ошибка: {e}")
            traceback.print_exc()
            print("🔄 Перезапуск через 5 секунд...")
            time.sleep(5)

if __name__ == '__main__':
    run_bot()