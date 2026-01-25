import os

from django.conf import settings


def load_bad_words_from_file() -> list[str]:
    """
    從專案根目錄讀取 bad_words.txt
    """
    bad_words = []
    file_path = os.path.join(settings.BASE_DIR, "data", "bad_words.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:

                word = line.strip()

                if word:
                    bad_words.append(word)
    except FileNotFoundError:
        bad_words = ["幹", "fuck"]

    return bad_words
