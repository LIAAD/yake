"""Basic tests for YAKE keyword extraction functionality."""


def test_phraseless_example(keyword_extractor):
    """Test extraction with minimal content."""
    text_content = "- not yet"
    result = keyword_extractor.extract_keywords(text_content)
    assert len(result) == 0


def test_null_and_blank_example(keyword_extractor):
    """Test extraction with empty string and None input."""
    result = keyword_extractor.extract_keywords("")
    assert len(result) == 0

    result = keyword_extractor.extract_keywords(None)
    assert len(result) == 0
