import pytest
import yake


@pytest.fixture
def keyword_extractor():
    """Fixture that returns a default keyword extractor."""
    return yake.KeywordExtractor()
