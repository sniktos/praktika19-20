import threading
from queue import Queue

# Очереди для передачи данных между потоками
text_queue = Queue()
result_queue = Queue()


def menu():
    """Диалоговое меню для взаимодействия с пользователем."""
    while True:
        print("Меню:")
        print("1. Ввести текст")
        print("2. Выполнить анализ текста")
        print("3. Показать результаты")
        print("4. Выход")

        choice = input("Выберите опцию: ")
        if choice == "1":
            text = input("Введите текст: ")
            text_queue.put(text)
        elif choice == "2":
            if text_queue.empty():
                print("Ошибка: текст не введён.")
            else:
                print("Отправка текста на анализ...")
                process_thread = threading.Thread(target=process_text)
                process_thread.start()
                process_thread.join()
        elif choice == "3":
            if result_queue.empty():
                print("Ошибка: данные ещё не обработаны.")
            else:
                display_results()
        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте ещё раз.")


# Чистая функция для анализа текста
def analyze_text(text):
    """Возвращает анализ текста: список слов с количеством гласных и согласных."""
    vowels = "aeiouAEIOU"
    words = text.split()
    return list(
        map(
            lambda word: (word, sum(1 for c in word if c in vowels),
                          sum(1 for c in word if c.isalpha() and c not in vowels)),
            words
        )
    )


def process_text():
    """Анализ текста во втором потоке."""
    if not text_queue.empty():
        text = text_queue.get()
        results = analyze_text(text)
        result_queue.put(results)
        print("Анализ завершён.")
    else:
        print("Нет текста для анализа.")


def display_results():
    """Вывод результатов в третьем потоке."""
    if not result_queue.empty():
        results = result_queue.get()
        print(f"{'Слово':<15}{'Гласные':<10}{'Согласные':<10}")
        print("-" * 35)
        for word, vowels, consonants in results:
            print(f"{word:<15}{vowels:<10}{consonants:<10}")
        print("-" * 35)
    else:
        print("Нет результатов для отображения.")


# Основной поток для запуска меню
if __name__ == "__main__":
    menu_thread = threading.Thread(target=menu)
    menu_thread.start()
    menu_thread.join()
