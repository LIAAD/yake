"""Tests for the Levenshtein distance and similarity ratio."""

import pytest
from yake.Levenshtein import Levenshtein


class TestLevenshtein:
    """Test suite for Levenshtein distance and similarity ratio functions."""

    def test_distance_same_strings(self):
        """Test distance between identical strings."""
        assert Levenshtein.distance("test", "test") == 0
        assert Levenshtein.distance("", "") == 0
        assert Levenshtein.distance("python", "python") == 0

    def test_distance_different_strings(self):
        """Test distance between different strings."""
        assert Levenshtein.distance("kitten", "sitting") == 3
        assert Levenshtein.distance("saturday", "sunday") == 3
        assert Levenshtein.distance("abc", "def") == 3

    def test_distance_empty_strings(self):
        """Test distance with one empty string."""
        assert Levenshtein.distance("", "test") == 4
        assert Levenshtein.distance("python", "") == 6

    def test_distance_special_chars(self):
        """Test distance with special characters and non-ASCII."""
        assert Levenshtein.distance("café", "cafe") == 1
        assert Levenshtein.distance("über", "uber") == 1
        assert Levenshtein.distance("résumé", "resume") == 2

    def test_distance_case_sensitivity(self):
        """Test that distance is case-sensitive."""
        assert Levenshtein.distance("Test", "test") == 1
        assert Levenshtein.distance("PYTHON", "python") == 6

    def test_ratio_same_strings(self):
        """Test similarity ratio between identical strings."""
        assert Levenshtein.ratio("test", "test") == 1.0
        assert Levenshtein.ratio("", "") == 1.0
        assert Levenshtein.ratio("python", "python") == 1.0

    def test_ratio_different_strings(self):
        """Test similarity ratio between different strings."""
        # kitten -> sitting (3 operations, max length 7)
        assert Levenshtein.ratio("kitten", "sitting") == pytest.approx(1.0 - 3 / 7)

        # saturday -> sunday (3 operations, max length 8)
        assert Levenshtein.ratio("saturday", "sunday") == pytest.approx(1.0 - 3 / 8)

        # completely different strings
        assert Levenshtein.ratio("abc", "def") == 0.0

    def test_ratio_empty_strings(self):
        """Test similarity ratio with one empty string."""
        assert Levenshtein.ratio("", "test") == 0.0
        assert Levenshtein.ratio("python", "") == 0.0

    def test_ratio_special_chars(self):
        """Test similarity ratio with special characters."""
        assert Levenshtein.ratio("café", "cafe") == pytest.approx(0.75)
        assert Levenshtein.ratio("über", "uber") == pytest.approx(0.75)

    def test_ratio_case_sensitivity(self):
        """Test that similarity ratio is case-sensitive."""
        assert Levenshtein.ratio("Test", "test") == 0.75
        assert Levenshtein.ratio("PYTHON", "python") == 0.0

    def test_with_list_sequences(self):
        """Test with list sequences instead of strings."""
        assert Levenshtein.distance([1, 2, 3], [1, 2, 4]) == 1
        assert Levenshtein.ratio([1, 2, 3], [1, 2, 3]) == 1.0
        assert Levenshtein.ratio([1, 2, 3], [4, 5, 6]) == 0.0
