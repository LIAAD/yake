import re
from typing import Set
import os
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# Constants
STOPWORD_WEIGHT = "bi"


def load_stopwords(language: str, stopwords: Optional[List[str]] = None) -> Set[str]:
    """Load stopwords from a file or use provided list.

    Args:
        language: Language code for stopwords
        stopwords: Custom stopwords list

    Returns:
        Set of stopwords
    """
    if stopwords is not None:
        return set(stopwords)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    lang_code = language[:2].lower()
    local_path = os.path.join("StopwordsList", f"stopwords_{lang_code}.txt")

    if not os.path.exists(os.path.join(dir_path, local_path)):
        local_path = os.path.join("StopwordsList", "stopwords_noLang.txt")

    resource_path = os.path.join(dir_path, local_path)

    try:
        with open(resource_path, encoding="utf-8") as stop_file:
            return set(stop_file.read().lower().split("\n"))
    except UnicodeDecodeError:
        logger.warning("Reading stopword list with ISO-8859-1 encoding")
        with open(resource_path, encoding="ISO-8859-1") as stop_file:
            return set(stop_file.read().lower().split("\n"))


# Utility functions
def pre_filter(text: str) -> str:
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
    prog = re.compile(r"^(\s*([A-Z]))")
    parts = text.split("\n")
    buffer = ""

    for part in parts:
        sep = " "
        if prog.match(part):
            sep = "\n\n"
        buffer += sep + part.replace("\t", " ")

    return buffer
