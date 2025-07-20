from stream_stopper import cut_stream_stop_words


# Advanced testing with realistic scenarios
def test_enhanced_algorithm():
    print("=== ENHANCED ALGORITHM TESTS ===\n")

    print("TEST 1: Basic example from the task")

    def gen1():
        tokens = ["Ah", "oj, ", "sv", "ete", "!"]
        for token in tokens:
            yield token
        return tokens

    tokens1 = ["Ah", "oj, ", "sv", "ete", "!"]
    stop_words1 = ["svet"]
    result1 = list(cut_stream_stop_words(iter(tokens1), stop_words1))
    print(f"Input tokens: {tokens1}")
    print(f"Stop words: {stop_words1}")
    print(f"Original text: '{(''.join(tokens1))}'")
    print(f"Result: {result1}")
    print(f"Filtered text: '{(''.join(result1))}'")
    print(f"Expected: 'Ahoj, ' (stops before 'svet')\n")

    print("TEST 2: Realistic text stream - news article")

    def realistic_news_stream():
        # Simulate a tokenizer that can split text unpredictably
        text = "Prezident České republiky dnes podepsal nový zákon o digitalizaci. Změny se dotknou všech občanů a budou platit od příštího roku. Vláda očekává úspory v řádu miliard korun."

        # Various tokenization methods (BPE-like, random lengths 1-10 characters)
        import random
        random.seed(42)  # For reproducibility

        tokens = []
        i = 0
        while i < len(text):
            # Random token length 1-10 characters
            token_len = random.randint(1, min(10, len(text) - i))
            token = text[i:i + token_len]
            tokens.append(token)
            yield token
            i += token_len

        return tokens

    # Generate tokens for display
    import random
    random.seed(42)
    text = "Prezident České republiky dnes podepsal nový zákon o digitalizaci. Změny se dotknou všech občanů a budou platit od příštího roku. Vláda očekává úspory v řádu miliard korun."
    tokens2 = []
    i = 0
    while i < len(text):
        token_len = random.randint(1, min(10, len(text) - i))
        tokens2.append(text[i:i + token_len])
        i += token_len

    stop_words2 = ["digitalizaci", "občanů"]
    result2 = list(cut_stream_stop_words(realistic_news_stream(), stop_words2))
    print(f"Input tokens: {tokens2[:10]}..." if len(tokens2) > 10 else f"Input tokens: {tokens2}")
    print(f"Stop words: {stop_words2}")
    print(f"Original text: '{(''.join(tokens2))}'")
    print(f"Result: {result2[:10]}..." if len(result2) > 10 else f"Result: {result2}")
    print(f"Filtered text: '{(''.join(result2))}'")
    print("Expected: text up to the first stop word\n")

    print("TEST 3: Subword tokenization (BPE-like)")

    def subword_stream():
        # Simulate Byte-Pair Encoding tokenization
        tokens = [
            "Č", "esk", "á", " repub", "lika", " má", " bohat", "ou",
            " hist", "orii", ".", " Pra", "ha", " je", " krás", "né",
            " měs", "to", " s", " mnoha", " památ", "kami", "."
        ]
        for token in tokens:
            yield token
        return tokens

    tokens3 = [
        "Č", "esk", "á", " repub", "lika", " má", " bohat", "ou",
        " hist", "orii", ".", " Pra", "ha", " je", " krás", "né",
        " měs", "to", " s", " mnoha", " památ", "kami", "."
    ]
    stop_words3 = ["historie", "Praha"]
    result3 = list(cut_stream_stop_words(subword_stream(), stop_words3))
    print(f"Input tokens: {tokens3}")
    print(f"Stop words: {stop_words3}")
    print(f"Original text: '{(''.join(tokens3))}'")
    print(f"Result: {result3}")
    print(f"Filtered text: '{(''.join(result3))}'")
    print("Expected: text up to 'historie' or 'Praha'\n")

    print("TEST 4: Streaming chat with emojis")

    def chat_stream():
        # Simulate real-time chat stream
        messages = [
            "Ahoj", " všichni", " 😊", " Jak", " se", " máte", "?",
            " Dnes", " je", " krásný", " den", " ☀️", " Těším", " se",
            " na", " víkend", "!", " Zastavte", " prosím", " spam", "."
        ]
        for msg in messages:
            yield msg
        return messages

    tokens4 = [
        "Ahoj", " všichni", " 😊", " Jak", " se", " máte", "?",
        " Dnes", " je", " krásný", " den", " ☀️", " Těším", " se",
        " na", " víkend", "!", " Zastavte", " prosím", " spam", "."
    ]
    stop_words4 = ["spam", "reklama"]
    result4 = list(cut_stream_stop_words(chat_stream(), stop_words4))
    print(f"Input tokens: {tokens4}")
    print(f"Stop words: {stop_words4}")
    print(f"Original text: '{(''.join(tokens4))}'")
    print(f"Result: {result4}")
    print(f"Filtered text: '{(''.join(result4))}'")
    print("Expected: text up to 'spam'\n")

    print("TEST 5: Code stream with comments")

    def code_stream():
        # Code tokenization (can be irregular)
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
    print(f"Result: {result5}")
    print(f"Joined: '{(''.join(result5))}'")
    print("Expected: code up to 'TODO' or 'optimalizovat'\n")

    print("TEST 6: High-frequency stream with small tokens")

    def high_freq_stream():
        # Simulate very fast stream with small tokens
        import itertools

        # Generate text as individual characters and short sequences
        text = "Toto je test vysokofrekvenčního streamu dat s mnoha malými tokeny a občasnými delšími sekvencemi."

        # Mix individual characters and short n-grams
        i = 0
        while i < len(text):
            if i % 7 == 0 and i + 3 < len(text):  # Occasionally longer token
                yield text[i:i + 3]
                i += 3
            else:  # Mostly individual characters
                yield text[i]
                i += 1

    result6 = list(cut_stream_stop_words(high_freq_stream(), ["vysokofrekv", "test"]))
    print(f"Number of tokens: {len(result6)}")
    print(f"Joined: '{(''.join(result6))}'")
    print("Expected: stops at the first stop word\n")

    print("TEST 7: Multilingual stream")

    def multilingual_stream():
        # Mix of languages with different character sets
        tokens = [
            "Hello", " world", "! ", "Ahoj", " světe", "! ",
            "Здравствуй", " мир", "! ", "こんにちは", "世界", "! ",
            "This", " is", " forbidden", " content", "."
        ]
        for token in tokens:
            yield token

    result7 = list(cut_stream_stop_words(multilingual_stream(), ["forbidden", "мир"]))
    print(f"Result: {result7}")
    print(f"Joined: '{(''.join(result7))}'")
    print("Expected: text up to the first stop word\n")

    print("TEST 8: Performance test - large volume stream")

    def large_stream():
        # Simulate truly large stream
        import time

        start_time = time.time()
        count = 0

        # Generate 50k tokens
        for i in range(50000):
            if i == 25000:  # Stop word in the middle
                yield "STOP_WORD"
            else:
                yield f"tok_{i % 100}"
            count += 1

        return count, time.time() - start_time

    result8 = list(cut_stream_stop_words(large_stream(), ["STOP_WORD"]))
    print(f"Number of processed tokens: {len(result8)}")
    print(f"Expected: 25000 tokens (stops at STOP_WORD)\n")


def benchmark_algorithm():
    """Benchmark for performance comparison"""
    import time

    print("=== BENCHMARK TESTS ===\n")

    # Test 1: Different numbers of stop words
    print("Benchmark 1: Effect of number of stop words on performance")

    def generate_stream(size=10000):
        for i in range(size):
            yield f"token{i % 50}"
        yield "FINAL_STOP"

    for num_stops in [1, 5, 10, 20, 50]:
        stop_words = [f"stop{i}" for i in range(num_stops)] + ["FINAL_STOP"]

        start = time.time()
        result = list(cut_stream_stop_words(generate_stream(), stop_words))
        elapsed = time.time() - start

        print(f"  {num_stops:2d} stop words: {elapsed:.4f}s, {len(result)} tokens")

    print("\nBenchmark 2: Effect of stop word length")

    for word_len in [5, 10, 20, 30, 50]:
        stop_words = ["x" * word_len, "FINAL_STOP"]

        start = time.time()
        result = list(cut_stream_stop_words(generate_stream(), stop_words))
        elapsed = time.time() - start

        print(f"  Length {word_len:2d}: {elapsed:.4f}s, {len(result)} tokens")


