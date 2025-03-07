"""Tests for YAKE keyword extraction across different languages."""

import os
import pytest
import yake

# Create test data directory if it doesn't exist
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(TEST_DATA_DIR, exist_ok=True)

# Sample text files
ENGLISH_TEXT_FILE = os.path.join(TEST_DATA_DIR, "english_sample.txt")
PORTUGUESE_TEXT_FILE = os.path.join(TEST_DATA_DIR, "portuguese_sample.txt")
GREEK_TEXT_FILE = os.path.join(TEST_DATA_DIR, "greek_sample.txt")


class TestEnglishExtraction:
    """Tests for English language keyword extraction."""

    @pytest.fixture
    def english_text(self):
        """Sample English text for testing."""
        with open(ENGLISH_TEXT_FILE, "r", encoding="utf-8") as f:
            return f.read()

    def test_n3_extraction(self, english_text):
        """Test extraction with n=3 in English."""
        extractor = yake.KeywordExtractor(lan="en", n=3)
        result = extractor.extract_keywords(english_text)

        expected_results = [
            ("Google", 0.02509259635302287),
            ("Kaggle", 0.027297150442917317),
            ("CEO Anthony Goldbloom", 0.04834891465259988),
            ("data science", 0.05499112888517541),
            ("acquiring data science", 0.06029572445726576),
        ]

        # Test overall length
        assert len(result) == 20

        # Test first 5 results to keep test manageable
        assert result[:5] == expected_results

    def test_n1_extraction(self, english_text):
        """Test extraction with n=1 in English."""
        extractor = yake.KeywordExtractor(lan="en", n=1)
        result = extractor.extract_keywords(english_text)

        # Test top 5 results
        expected_top5 = [
            ("google", 0.02509259635302287),
            ("kaggle", 0.027297150442917317),
            ("data", 0.07999958986489127),
            ("science", 0.09834167930168546),
            ("platform", 0.12404419723925647),
        ]

        assert result[:5] == expected_top5


class TestPortugueseExtraction:
    """Tests for Portuguese language keyword extraction."""

    @pytest.fixture
    def portuguese_text(self):
        """Sample Portuguese text for testing."""
        with open(PORTUGUESE_TEXT_FILE, "r", encoding="utf-8") as f:
            return f.read()

    def test_n3_extraction(self, portuguese_text):
        """Test extraction with n=3 in Portuguese."""
        extractor = yake.KeywordExtractor(lan="pt", n=3)
        result = extractor.extract_keywords(portuguese_text)

        expected_top5 = [
            ("Conta-me Histórias", 0.006225012963810038),
            ("LIAAD do INESC", 0.01899063587015275),
            ("INESC TEC", 0.01995432290332246),
            ("Conta-me", 0.04513273690417472),
            ("Histórias", 0.04513273690417472),
        ]

        assert result[:5] == expected_top5


class TestGreekExtraction:
    """Tests for Greek language keyword extraction."""

    @pytest.fixture
    def greek_text(self):
        """Sample Greek text for testing."""
        with open(GREEK_TEXT_FILE, "r", encoding="utf-8") as f:
            return f.read()

    def test_n1_extraction(self, greek_text):
        """Test extraction with n=1 in Greek."""
        extractor = yake.KeywordExtractor(lan="el", n=1)
        result = extractor.extract_keywords(greek_text)

        expected_top5 = [
            ("Ουκρανίας", 0.04685829498124156),
            ("Χάρκοβο", 0.0630891548728466),
            ("Άμυνας", 0.06395408991254226),
            ("σύμφωνα", 0.07419311338418161),
            ("υπουργείου", 0.1069960715371627),
        ]

        assert result[:5] == expected_top5
