import os
import json
import sys
from typing import Generator

import requests
import dotenv

from stream_stopper import cut_stream_stop_words

dotenv.load_dotenv("./.env")



API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload, stream=True)
    for line in response.iter_lines():
        if not line.startswith(b"data:"):
            continue
        if line.strip() == b"data: [DONE]":
            return
        yield json.loads(line.decode("utf-8").lstrip("data:").rstrip("/n"))


def token_stream_from_chunks(chunks: Generator) -> Generator[str, None, None]:
    """Convert API response chunks to token stream."""
    for chunk in chunks:
        try:
            content = chunk["choices"][0]["delta"]["content"]
            if content:  # Skip empty content
                yield content
        except (KeyError, IndexError, TypeError):
            # Handle malformed chunks gracefully
            continue


def test_stopwords(stop_words=("HOTOVO!", "stopni", "Praha"),
                   content="""
                    Jaké je hlavní město Česka?
                    Napiš v češtině text o hlavním městu Česka.
                   """):

    chunks = query({
        "messages": [
            {
                "role": "system",
                "content": f"odpovídej česky, na konci celé odpopovědi napiš {', '.join(stop_words)} a přdej větu: toto se už nezobrazuje..."
            },

            {
                "role": "user",
                "content": content
            }
        ],
        "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
        "stream": True,
    })

    # Create two parallel streams - one for filtering, one for collecting filtered text
    all_chunks = list(chunks)  # Collect all chunks first

    # Stream 1: Display filtered tokens in real-time
    token_stream = token_stream_from_chunks(iter(all_chunks))
    filtered_stream = cut_stream_stop_words(token_stream, list(stop_words))

    filtered_text = ""
    for token in filtered_stream:
        print(token, end="", flush=True)
        filtered_text += token

    print()  # Final newline

    # Stream 2: Show what was filtered out via stderr
    print(f"Filtered text: '{filtered_text}'", file=sys.stderr)

    # Show full unfiltered text for comparison
    full_text = ""
    for chunk in all_chunks:
        try:
            content = chunk["choices"][0]["delta"]["content"]
            if content:
                full_text += content
        except:
            continue

    print(f"Original full text: '{full_text}'", file=sys.stderr)
    print(f"Stop words used: {list(stop_words)}", file=sys.stderr)


def advanced_test_stopwords():
    """More advanced example with multiple stop words and error handling."""

    stop_words = [
        "HOTOVO!", "stopni", "konec", "STOP",
        "toto se už nezobrazuje", "ukončuji"
    ]

    content = """
    Napiš krátký příběh o robotovi. 
    Na konci příběhu napiš HOTOVO! a pak pokračuj nějakým textem který se již nezobrazí.
    """

    try:
        chunks = query({
            "messages": [
                {
                    "role": "system",
                    "content": "Jsi kreativní spisovatel. Píšeš česky a na konci každého příběhu napíšeš HOTOVO! a pak přidáš text: 'toto se už nezobrazuje uživateli...'"
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
            "stream": True,
            "max_tokens": 500,
            "temperature": 0.7
        })

        print("🤖 AI Response (filtered):")
        print("-" * 40)

        # Collect all chunks for dual processing
        all_chunks = list(chunks)

        # Stream 1: Filtered display
        token_stream = token_stream_from_chunks(iter(all_chunks))
        filtered_stream = cut_stream_stop_words(token_stream, stop_words)

        filtered_text = ""
        token_count = 0

        for token in filtered_stream:
            print(token, end="", flush=True)
            filtered_text += token
            token_count += 1

        print()
        print("-" * 40)
        print(f"✅ Stream stopped after {token_count} tokens")
        print(f"🛑 Filtered stop words: {stop_words}")

        # Stream 2: Show filtered text and original via stderr
        print(f"Filtered text: '{filtered_text}'", file=sys.stderr)

        # Show full text
        full_text = ""
        for chunk in all_chunks:
            try:
                content = chunk["choices"][0]["delta"]["content"]
                if content:
                    full_text += content
            except:
                continue

        print(f"Original full text: '{full_text}'", file=sys.stderr)

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error details: {e}", file=sys.stderr)


def demo_comparison():
    """Demonstrate the difference between filtered and unfiltered streams."""

    stop_words = ["KONEC", "stop"]

    content = "Vysvětli stručně co je umělá inteligence. Na konci napiš KONEC a pak pokračuj dlouhým textem."

    chunks = query({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
        "stream": True,
        "max_tokens": 300
    })

    # Collect all tokens first (for demo purposes)
    all_chunks = list(chunks)

    print("🚫 UNFILTERED OUTPUT:")
    print("-" * 50)
    full_text = ""
    for chunk in all_chunks:
        try:
            content = chunk["choices"][0]["delta"]["content"]
            if content:
                print(content, end="", flush=True)
                full_text += content
        except:
            continue

    print("\n\n")
    print("✅ FILTERED OUTPUT:")
    print("-" * 50)

    # Reset and filter
    token_stream = token_stream_from_chunks(iter(all_chunks))
    filtered_stream = cut_stream_stop_words(token_stream, stop_words)

    filtered_text = ""
    for token in filtered_stream:
        print(token, end="", flush=True)
        filtered_text += token

    print(f"\n\n🛑 Stopped at stop words: {stop_words}")

    # Show comparison via stderr
    print(f"Filtered text: '{filtered_text}'", file=sys.stderr)
    print(f"Original full text: '{full_text}'", file=sys.stderr)
    print(f"Characters filtered out: {len(full_text) - len(filtered_text)}", file=sys.stderr)


