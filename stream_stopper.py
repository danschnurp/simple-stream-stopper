from collections import deque
from typing import Generator


class StopWordFilter:
    """
    Efficient filter for stop word detection using n-grams.
    Uses trie structure for fast prefix searching.
    """

    def __init__(self, stop_words: list[str]):
        self.stop_words = stop_words
        self.max_length = max(len(word) for word in stop_words) if stop_words else 0

        # Trie structure for prefix searching
        self.trie = {}
        self.complete_words = set(stop_words)

        # Build the trie
        for word in stop_words:
            current = self.trie
            for char in word:
                if char not in current:
                    current[char] = {}
                current = current[char]
            current['$'] = True  # End of word marker

    def find_stop_word_at_position(self, text: str, start_pos: int) -> tuple[str, int] | None:
        """
        Find a stop word starting at the given position.
        Returns (stop_word, end_position) or None.
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
                # We found a complete stop word
                stop_word = text[start_pos:i + 1]
                return stop_word, i + 1

        return None

    def find_earliest_stop_word(self, text: str) -> tuple[str, int, int] | None:
        """
        Find the earliest occurring stop word in the text.
        Returns (stop_word, start_pos, end_pos) or None.
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
    Optimized function using n-gram filter for fast stop word detection.
    """
    if not stop_words:
        yield from token_stream
        return

    # Initialize filter for stop words
    filter = StopWordFilter(stop_words)

    # Sliding window buffer for efficient processing
    buffer = ""
    token_queue = deque()  # (token, start_pos_in_buffer)

    for token in token_stream:
        start_pos = len(buffer)
        buffer += token
        token_queue.append((token, start_pos))

        # Check for stop words using filter
        stop_result = filter.find_earliest_stop_word(buffer)

        if stop_result:
            stop_word, stop_start, stop_end = stop_result

            # Emit tokens/parts of tokens before the stop word
            while token_queue:
                curr_token, token_start = token_queue.popleft()
                token_end = token_start + len(curr_token)

                if token_end <= stop_start:
                    # Entire token is before the stop word
                    yield curr_token
                elif token_start < stop_start:
                    # Token partially overlaps with stop word
                    prefix_len = stop_start - token_start
                    yield curr_token[:prefix_len]
                    break
                else:
                    # Token is after the stop word, don't emit it
                    break

            return

        # Optimization: emit tokens that can no longer contain the start of a stop word
        safe_boundary = len(buffer) - filter.max_length + 1

        emitted_tokens = []
        while token_queue:
            curr_token, token_start = token_queue[0]
            token_end = token_start + len(curr_token)

            if token_end <= safe_boundary:
                emitted_tokens.append(token_queue.popleft()[0])
            else:
                break

        # Emit safe tokens
        for token in emitted_tokens:
            yield token

        # Update buffer and recalculate positions
        if emitted_tokens:
            emitted_length = sum(len(t) for t in emitted_tokens)
            buffer = buffer[emitted_length:]

            # Recalculate positions of remaining tokens
            updated_queue = deque()
            for token, pos in token_queue:
                updated_queue.append((token, pos - emitted_length))
            token_queue = updated_queue

    # Emit all remaining tokens
    while token_queue:
        yield token_queue.popleft()[0]

