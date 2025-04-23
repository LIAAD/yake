"""Utility functions for text processing."""

import re
from segtok.segmenter import split_multi
from segtok.tokenizer import web_tokenizer, split_contractions

STOPWORD_WEIGHT = "bi"

def pre_filter(text):
    """Pre-filter the text to normalize line breaks and spacing."""
    prog = re.compile("^(\\s*([A-Z]))")
    parts = text.split("\n")
    buffer = ""
    for part in parts:
        sep = " "
        if prog.match(part):
            sep = "\n\n"
        buffer += sep + part.replace("\t", " ")
    return buffer

def tokenize_sentences(text):
    """Tokenize text into sentences and words."""
    return [
        [
            w
            for w in split_contractions(web_tokenizer(s))
            if not (w.startswith("'") and len(w) > 1) and len(w) > 0
        ]
        for s in list(split_multi(text))
        if len(s.strip()) > 0
    ]

def get_tag(word, i, exclude):
    """Determine the tag of a word based on its characteristics."""

    # Check if word is numeric 
    if word.replace(",", "").isdigit() or word.replace(",", "").replace(".", "", 1).isdigit():
        return "d"

    # Use counting instead of list comprehensions for better performance
    cdigit = sum(c.isdigit() for c in word)
    calpha = sum(c.isalpha() for c in word)
    cexclude = sum(c in exclude for c in word)

    # Check for unusual combinations
    if (cdigit > 0 and calpha > 0) or (cdigit == 0 and calpha == 0) or cexclude > 1:
        return "u"

    # Check for ALL CAPS (acronym)
    if word.isupper() and len(word) > 0:
        return "a"

    # Check for Proper noun (capitalized)
    if len(word) > 1 and word[0].isupper() and i > 0:
        # Optimized check for single uppercase letter
        if sum(c.isupper() for c in word) == 1:
            return "n"

    return "p"
