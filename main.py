import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# Функция анализа текста
def analyze_text(words):
    vowels = set("aeiouAEIOU")
    consonants = set(string.ascii_letters) - vowels

    # Генератор для подсчёта гласных и согласных
    def word_analysis(word):
        vowel_count = sum(1 for char in word if char in vowels)
        consonant_count = sum(1 for char in word if char in consonants)
        return word, vowel_count, consonant_count

    return map(word_analysis, words)


# Асинхронная обработка текста
def process_text_async(text):
    words = text.split()
    with ThreadPoolExecutor() as executor:
        # Разбиваем текст на части
        chunk_size = max(len(words) // 4, 1)  # 4 потока
        futures = [
            executor.submit(analyze_text, words[i:i + chunk_size])
            for i in range(0, len(words), chunk_size)
        ]

        # Сбор результатов
        results = []
        for future in as_completed(futures):
            results.extend(list(future.result()))
        return results


# Тестовый запуск
def main():
    sample_text = "This is an example text to demonstrate optimization using Python." * 1000
    start = time.time()
    results = process_text_async(sample_text)
    end = time.time()

    print(f"Processed {len(sample_text.split())} words in {end - start:.2f} seconds.")
    print(f"Sample result: {results[:5]}")


if __name__ == "__main__":
    main()
