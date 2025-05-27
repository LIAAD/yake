"""
Text processing utility module for YAKE keyword extraction.

This module provides essential text preprocessing functions for the YAKE algorithm,
including text normalization, sentence segmentation, tokenization, and word
categorization. These utilities form the foundation for clean and consistent
text analysis throughout the keyword extraction pipeline.
"""

import re
from segtok.segmenter import split_multi
from segtok.tokenizer import web_tokenizer, split_contractions

# Stopword weighting method for multi-word term scoring:
# - "bi": Use bi-directional weighting (default, considers term connections)
# - "h": Use direct term scores (treat stopwords like normal words)
# - "none": Ignore stopwords completely
STOPWORD_WEIGHT = "bi"


def pre_filter(text):
    """Pre-filter text before processing.

    This function prepares raw text for keyword extraction by normalizing its format.
    It performs several transformations:

    1. Splits the text into parts based on newline characters
    2. Detects if a part starts with a capital letter (potentially a new paragraph)
    3. Adds appropriate spacing between parts:
       - Double newlines for parts starting with capital letters (likely new paragraphs)
       - Single spaces for other parts (likely continuing text)
    4. Replaces all tab characters with spaces for consistent formatting

    This preprocessing helps maintain paragraph structure while normalizing
    whitespace, which improves the accuracy of subsequent text analysis steps
    like sentence boundary detection and keyword extraction.

    Args:
        text: Raw input text to be pre-filtered

    Returns:
        Normalized text with consistent spacing and paragraph structure
    """
    # Regular expression to detect lines starting with capital letters
    prog = re.compile("^(\\s*([A-Z]))")

    # Split the text into lines
    parts = text.split("\n")
    buffer = ""

    # Process each line
    for part in parts:
        # Determine separator: preserve paragraph breaks for lines starting with capital letters
        sep = " "
        if prog.match(part):
            sep = "\n\n"

        # Append the processed line to the buffer, replacing tabs with spaces
        buffer += sep + part.replace("\t", " ")

    return buffer


def tokenize_sentences(text):
    """
    Split text into sentences and tokenize into words.

    This function performs two-level tokenization: first dividing the text into
    sentences using segtok's sentence segmenter, then tokenizing each sentence
    into individual words. It also handles contractions and filters out empty
    or invalid tokens.

    Args:
        text (str): The input text to be tokenized

    Returns:
        list: A nested list structure where each inner list contains the tokens
              for a single sentence in the original text
    """
    return [
        # Inner list: tokenize each sentence into words
        [
            w  # Keep only valid word tokens
            for w in split_contractions(web_tokenizer(s))
            # Filter out standalone apostrophes and empty tokens
            if not (w.startswith("'") and len(w) > 1) and len(w) > 0
        ]
        # Outer list: iterate through sentences
        for s in list(split_multi(text))
        # Skip empty sentences
        if len(s.strip()) > 0
    ]


def get_tag(word, i, exclude):
    """
    Determine the linguistic tag of a word based on its characteristics.

    This function categorizes words into different types based on their
    orthographic features (capitalization, digits, special characters).
    These tags are used to identify proper nouns, acronyms, numbers, and
    unusual token patterns, which affect keyword scoring and filtering.

    Args:
        word (str): The word to classify
        i (int): Position of the word within its sentence (0 = first word)
        exclude (set): Set of characters to consider as punctuation/special chars

    Returns:
        str: A single character tag representing the word type:
            - "d": Digit or numeric value
            - "u": Unusual word (mixed alphanumeric or special characters)
            - "a": Acronym (all uppercase)
            - "n": Proper noun (capitalized, not at start of sentence)
            - "p": Plain word (default)
    """
    # Check if word is numeric (with possible commas and a decimal point)
    if (
        word.replace(",", "").isdigit()
        or word.replace(",", "").replace(".", "", 1).isdigit()
    ):
        return "d"

    # Count character types for classification
    cdigit = sum(c.isdigit() for c in word)
    calpha = sum(c.isalpha() for c in word)
    cexclude = sum(c in exclude for c in word)

    # Classify unusual tokens: mixed alphanumeric, special chars, or multiple punctuation
    if (cdigit > 0 and calpha > 0) or (cdigit == 0 and calpha == 0) or cexclude > 1:
        return "u"

    # Identify acronyms (all uppercase words)
    if word.isupper() and len(word) > 0:
        return "a"

    # Identify proper nouns (capitalized words not at sentence beginning)
    if len(word) > 1 and word[0].isupper() and i > 0:
        # Check that only the first letter is uppercase (not an all-caps word)
        if sum(c.isupper() for c in word) == 1:
            return "n"

    # Default case: plain word
    return "p"
