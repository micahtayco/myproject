import os

def load_quotes():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "quotes.txt")

    try:
        with open(quotes.txt, encoding='utf-8') as file:
            quotes = file.read().splitlines()
            print(quotes)

        if not quotes:
            return ["No quotes found."]

        return quotes

    except FileNotFoundError:
        return ["quotes.txt not found!"]