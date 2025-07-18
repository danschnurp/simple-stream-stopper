from typing import Generator, Dict, Set
from collections import defaultdict, deque


class StopWordAutomaton:
    """
    Efektivní automát pro detekci stop slov pomocí n-gramů.
    Používá trie strukturu pro rychlé vyhledávání prefixů.
    """

    def __init__(self, stop_words: list[str]):
        self.stop_words = stop_words
        self.max_length = max(len(word) for word in stop_words) if stop_words else 0

        # Trie struktura pro prefixové vyhledávání
        self.trie = {}
        self.complete_words = set(stop_words)

        # Sestavíme trie
        for word in stop_words:
            current = self.trie
            for char in word:
                if char not in current:
                    current[char] = {}
                current = current[char]
            current['$'] = True  # Značka konce slova

    def find_stop_word_at_position(self, text: str, start_pos: int) -> tuple[str, int] | None:
        """
        Najde stop slovo začínající na dané pozici.
        Vrací (stop_word, end_position) nebo None.
        """
        if start_pos >= len(text):
            return None

        current = self.trie
        for i in range(start_pos, min(start_pos + self.max_length, len(text))):
            char = text[i]
            if char not in current:
                return None
            current = current[char]
            if '$' in current:
                # Našli jsme kompletní stop slovo
                stop_word = text[start_pos:i + 1]
                return stop_word, i + 1

        return None

    def find_earliest_stop_word(self, text: str) -> tuple[str, int, int] | None:
        """
        Najde nejdříve se vyskytující stop slovo v textu.
        Vrací (stop_word, start_pos, end_pos) nebo None.
        """
        earliest_pos = len(text)
        earliest_word = None
        earliest_end = None

        for i in range(len(text)):
            result = self.find_stop_word_at_position(text, i)
            if result and i < earliest_pos:
                earliest_pos = i
                earliest_word = result[0]
                earliest_end = result[1]

        return (earliest_word, earliest_pos, earliest_end) if earliest_word else None


def cut_stream_stop_words(token_stream: Generator[str, None, None],
                          stop_words: list[str]) -> Generator[str, None, None]:
    """
    Optimalizovaná funkce používající n-gramový automát pro rychlou detekci stop slov.
    """
    if not stop_words:
        yield from token_stream
        return

    # Inicializujeme automát pro stop slova
    automaton = StopWordAutomaton(stop_words)

    # Sliding window buffer pro efektivní zpracování
    buffer = ""
    token_queue = deque()  # (token, start_pos_in_buffer)

    for token in token_stream:
        start_pos = len(buffer)
        buffer += token
        token_queue.append((token, start_pos))

        # Zkontroluj stop slova pomocí automatu
        stop_result = automaton.find_earliest_stop_word(buffer)

        if stop_result:
            stop_word, stop_start, stop_end = stop_result

            # Vydej tokeny/části tokenů před stop slovem
            while token_queue:
                curr_token, token_start = token_queue.popleft()
                token_end = token_start + len(curr_token)

                if token_end <= stop_start:
                    # Celý token je před stop slovem
                    yield curr_token
                elif token_start < stop_start:
                    # Token částečně prekrývá stop slovo
                    prefix_len = stop_start - token_start
                    yield curr_token[:prefix_len]
                    break
                else:
                    # Token je za stop slovem, nevydávej ho
                    break

            return

        # Optimalizace: vydej tokeny, které už nemůžou obsahovat začátek stop slova
        safe_boundary = len(buffer) - automaton.max_length + 1

        emitted_tokens = []
        while token_queue:
            curr_token, token_start = token_queue[0]
            token_end = token_start + len(curr_token)

            if token_end <= safe_boundary:
                emitted_tokens.append(token_queue.popleft()[0])
            else:
                break

        # Vydej bezpečné tokeny
        for token in emitted_tokens:
            yield token

        # Aktualizuj buffer a přepočítej pozice
        if emitted_tokens:
            emitted_length = sum(len(t) for t in emitted_tokens)
            buffer = buffer[emitted_length:]

            # Přepočítej pozice zbývajících tokenů
            updated_queue = deque()
            for token, pos in token_queue:
                updated_queue.append((token, pos - emitted_length))
            token_queue = updated_queue

    # Vydej všechny zbývající tokeny
    while token_queue:
        yield token_queue.popleft()[0]


# Pokročilé testování s realistickými scénáři
def test_enhanced_algorithm():
    print("=== ENHANCED ALGORITHM TESTS ===\n")

    print("TEST 1: Základní příklad z úlohy")

    def gen1():
        for token in ["Ah", "oj, ", "sv", "ete", "!"]:
            yield token

    result1 = list(cut_stream_stop_words(gen1(), ["svet"]))
    print(f"Výsledek: {result1}")
    print(f"Spojeno: '{(''.join(result1))}'")
    print(f"Očekáváno: 'Ahoj, ' (zastaví se před 'svet')\n")

    print("TEST 2: Realistický text stream - novinový článek")

    def realistic_news_stream():
        # Simulace tokerizátoru, který může rozdělit text nepředvídatelně
        text = "Prezident České republiky dnes podepsal nový zákon o digitalizaci. Změny se dotknou všech občanů a budou platit od příštího roku. Vláda očekává úspory v řádu miliard korun."

        # Různé způsoby tokenizace (BPE-like, náhodné délky 1-10 znaků)
        import random
        random.seed(42)  # Pro reprodukovatelnost

        i = 0
        while i < len(text):
            # Náhodná délka tokenu 1-10 znaků
            token_len = random.randint(1, min(10, len(text) - i))
            yield text[i:i + token_len]
            i += token_len

    result2 = list(cut_stream_stop_words(realistic_news_stream(), ["digitalizaci", "občanů"]))
    print(f"Výsledek: {result2}")
    print(f"Spojeno: '{(''.join(result2))}'")
    print("Očekáváno: text až do prvního stop slova\n")

    print("TEST 3: Subword tokenizace (BPE-like)")

    def subword_stream():
        # Simulace Byte-Pair Encoding tokenizace
        tokens = [
            "Č", "esk", "á", " repub", "lika", " má", " bohat", "ou",
            " hist", "orii", ".", " Pra", "ha", " je", " krás", "né",
            " měs", "to", " s", " mnoha", " památ", "kami", "."
        ]
        for token in tokens:
            yield token

    result3 = list(cut_stream_stop_words(subword_stream(), ["historie", "Praha"]))
    print(f"Výsledek: {result3}")
    print(f"Spojeno: '{(''.join(result3))}'")
    print("Očekáváno: text až do 'historie' nebo 'Praha'\n")

    print("TEST 4: Streaming chat s emotikonami")

    def chat_stream():
        # Simulace real-time chat streamu
        messages = [
            "Ahoj", " všichni", " 😊", " Jak", " se", " máte", "?",
            " Dnes", " je", " krásný", " den", " ☀️", " Těším", " se",
            " na", " víkend", "!", " Zastavte", " prosím", " spam", "."
        ]
        for msg in messages:
            yield msg

    result4 = list(cut_stream_stop_words(chat_stream(), ["spam", "reklama"]))
    print(f"Výsledek: {result4}")
    print(f"Spojeno: '{(''.join(result4))}'")
    print("Očekáváno: text až do 'spam'\n")

    print("TEST 5: Kódový stream s komentáři")

    def code_stream():
        # Tokenizace kódu (může být nepravidelná)
        code_tokens = [
            "def", " process", "_data", "(", "data", "):", "\n    ",
            "# TODO", ":", " optimalizovat", " tento", " algoritmus", "\n    ",
            "for", " item", " in", " data", ":", "\n        ",
            "if", " item", ".", "is_", "valid", "():", "\n            ",
            "yield", " item", ".", "transform", "()"
        ]
        for token in code_tokens:
            yield token

    result5 = list(cut_stream_stop_words(code_stream(), ["TODO", "optimalizovat"]))
    print(f"Výsledek: {result5}")
    print(f"Spojeno: '{(''.join(result5))}'")
    print("Očekáváno: kód až do 'TODO' nebo 'optimalizovat'\n")

    print("TEST 6: Vysokofrekvenční stream s malými tokeny")

    def high_freq_stream():
        # Simulace velmi rychlého streamu s malými tokeny
        import itertools

        # Generuj text po jednotlivých znacích a krátkých sekvencích
        text = "Toto je test vysokofrekvenčního streamu dat s mnoha malými tokeny a občasnými delšími sekvencemi."

        # Mix jednotlivých znaků a krátkých n-gramů
        i = 0
        while i < len(text):
            if i % 7 == 0 and i + 3 < len(text):  # Občas delší token
                yield text[i:i + 3]
                i += 3
            else:  # Většinou jednotlivé znaky
                yield text[i]
                i += 1

    result6 = list(cut_stream_stop_words(high_freq_stream(), ["vysokofrekv", "test"]))
    print(f"Počet tokenů: {len(result6)}")
    print(f"Spojeno: '{(''.join(result6))}'")
    print("Očekáváno: zastaví se u prvního stop slova\n")

    print("TEST 7: Multilingual stream")

    def multilingual_stream():
        # Mix jazyků s různými znakovými sadami
        tokens = [
            "Hello", " world", "! ", "Ahoj", " světe", "! ",
            "Здравствуй", " мир", "! ", "こんにちは", "世界", "! ",
            "This", " is", " forbidden", " content", "."
        ]
        for token in tokens:
            yield token

    result7 = list(cut_stream_stop_words(multilingual_stream(), ["forbidden", "мир"]))
    print(f"Výsledek: {result7}")
    print(f"Spojeno: '{(''.join(result7))}'")
    print("Očekáváno: text až do prvního stop slova\n")

    print("TEST 8: Performance test - velkoobjemový stream")

    def large_stream():
        # Simulace skutečně velkého streamu
        import time

        start_time = time.time()
        count = 0

        # Generuj 50k tokenů
        for i in range(50000):
            if i == 25000:  # Stop slovo v polovině
                yield "STOP_WORD"
            else:
                yield f"tok_{i % 100}"
            count += 1

        return count, time.time() - start_time

    result8 = list(cut_stream_stop_words(large_stream(), ["STOP_WORD"]))
    print(f"Počet zpracovaných tokenů: {len(result8)}")
    print(f"Očekáváno: 25000 tokenů (zastaví se u STOP_WORD)\n")


def benchmark_algorithm():
    """Benchmark pro porovnání výkonu"""
    import time

    print("=== BENCHMARK TESTS ===\n")

    # Test 1: Různé počty stop slov
    print("Benchmark 1: Vliv počtu stop slov na výkon")

    def generate_stream(size=10000):
        for i in range(size):
            yield f"token{i % 50}"
        yield "FINAL_STOP"

    for num_stops in [1, 5, 10, 20, 50]:
        stop_words = [f"stop{i}" for i in range(num_stops)] + ["FINAL_STOP"]

        start = time.time()
        result = list(cut_stream_stop_words(generate_stream(), stop_words))
        elapsed = time.time() - start

        print(f"  {num_stops:2d} stop slov: {elapsed:.4f}s, {len(result)} tokenů")

    print("\nBenchmark 2: Vliv délky stop slov")

    for word_len in [5, 10, 20, 30, 50]:
        stop_words = ["x" * word_len, "FINAL_STOP"]

        start = time.time()
        result = list(cut_stream_stop_words(generate_stream(), stop_words))
        elapsed = time.time() - start

        print(f"  Délka {word_len:2d}: {elapsed:.4f}s, {len(result)} tokenů")


if __name__ == "__main__":
    test_enhanced_algorithm()
    print("\n" + "=" * 50 + "\n")
    benchmark_algorithm()