import schedule
import time
import scrap

# Планування виконання скрипта кожну годину
schedule.every(1).hours.do(scrap.run_scraping)

if __name__ == "__main__":
    # Запуск сервера API
    exec(open('api.py', 'r').read())

    # Безкінечний цикл для виконання завдань за розкладом
    while True:
        schedule.run_pending()
        time.sleep(1)

