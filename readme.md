# Stream Stopper

## Overview
This project provides an efficient filter for stop word detection using a **trie** structure for fast prefix searching.

## Prerequisites


To run this project, you need to have the following dependencies installed:

- Python 3.11 or higher

You can install the required libraries using pip:

```bash
pip install -r requirements.txt
```

### Hugging Face Token

If you plan to use LLM-based context generation, you will need a Hugging Face API token. You can obtain this token by signing up on the [Hugging Face website](https://huggingface.co/).

Once you have your token, you can set it as an environment variable:

to `.env`


## Test outputs
- they can be found in [output_from_tests.md](output_from_tests.md)



## Implementation and Algorithm

### Class: `StopWordFilter`

The `StopWordFilter` class is responsible for building and querying a trie structure to detect stop words efficiently.

1. **Initialization (`__init__` method)**:
   - **Input**: A list of stop words.
   - **Process**:
     - Calculates the maximum length of the stop words.
     - Initializes an empty trie and a set of complete stop words.
     - Builds the trie by inserting each stop word character by character. Each node in the trie represents a character, and the end of a word is marked with a special character (`'$'`).
   - **Output**: None.

2. **Finding Stop Words at a Position (`find_stop_word_at_position` method)**:
   - **Input**: A text string and a starting position.
   - **Process**:
     - Checks if the starting position is within the bounds of the text.
     - Traverses the trie using characters from the text starting at the given position.
     - If a complete stop word is found, returns the stop word and its end position.
   - **Output**: A tuple containing the stop word and its end position, or `None` if no stop word is found.

3. **Finding the Earliest Stop Word (`find_earliest_stop_word` method)**:
   - **Input**: A text string.
   - **Process**:
     - Iterates through each position in the text and uses `find_stop_word_at_position` to check for stop words.
     - Keeps track of the earliest stop word found.
   - **Output**: A tuple containing the earliest stop word, its start position, and end position, or `None` if no stop word is found.

## Limitations

**Input stop words** require preprocessing and contextual understanding to be effective. 

## Recommended Approaches

### 1. 🤖 LLM-Based Context Generation

**Description:** Provide an LLM with stop words and context, allowing it to generate an advanced set of stop words that incorporates topic-specific context.

**Advantages:**
- High accuracy and contextual relevance
- Adaptive to specific domains and topics
- Intelligent understanding of semantic relationships

**Disadvantages:**
- Slower processing time due to generation overhead
- Requires API calls or model inference
- Higher computational cost

### 2. ⚡ NLP Preprocessing Methods

**Description:** Utilize traditional NLP preprocessing techniques such as stemming for stop word processing.

**Advantages:**
- Fast processing speed
- Low computational overhead
- No external dependencies on language models

**Disadvantages:**
- Can be inaccurate in certain contexts
- Limited contextual understanding
- May not adapt well to domain-specific terminology

