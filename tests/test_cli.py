"""Tests for the CLI interface."""

import json
import os
import tempfile
import pytest
from click.testing import CliRunner
from yake.cli import main, get_available_languages


class TestCLI:
    """Test suite for YAKE CLI functionality."""

    @pytest.fixture
    def runner(self):
        """Fixture that returns a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def sample_text(self):
        """Fixture that provides sample text for keyword extraction."""
        return "YAKE is a light-weight unsupervised automatic keyword extraction method which rests on statistical text features extracted from single documents."

    @pytest.fixture
    def sample_file(self, sample_text):
        """Fixture that creates a temporary file with sample text."""
        with tempfile.NamedTemporaryFile(
            mode="w+", delete=False, encoding="utf-8"
        ) as f:
            f.write(sample_text)
            filename = f.name

        yield filename

        # Cleanup after test
        if os.path.exists(filename):
            os.unlink(filename)

    def test_help_command(self, runner):
        """Test the help command."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "YAKE: Yet Another Keyword Extractor" in result.output
        assert "--text-input" in result.output
        assert "--input-file" in result.output

    def test_list_languages(self, runner):
        """Test the language listing functionality."""
        result = runner.invoke(main, ["--list-languages"])
        assert result.exit_code == 0
        assert "Available languages for stopwords:" in result.output
        # At least English should be available
        assert "- en" in result.output

    def test_text_input(self, runner, sample_text):
        """Test keyword extraction from text input."""
        result = runner.invoke(main, ["--text-input", sample_text])
        assert result.exit_code == 0
        assert "keyword" in result.output
        # Common keywords that should be extracted
        assert "keyword extraction" in result.output or "extraction" in result.output

    def test_file_input(self, runner, sample_file):
        """Test keyword extraction from file input."""
        result = runner.invoke(main, ["--input-file", sample_file])
        assert result.exit_code == 0
        assert "keyword" in result.output

    def test_verbose_output(self, runner, sample_text):
        """Test verbose output with scores."""
        result = runner.invoke(main, ["--text-input", sample_text, "--verbose"])
        assert result.exit_code == 0
        assert "keyword" in result.output
        assert "score" in result.output

    def test_json_format(self, runner, sample_text):
        """Test JSON output format."""
        result = runner.invoke(main, ["--text-input", sample_text, "--format", "json"])
        assert result.exit_code == 0
        # Ensure output is valid JSON
        parsed = json.loads(result.output)
        assert isinstance(parsed, list)
        assert len(parsed) > 0
        assert "keyword" in parsed[0]

    def test_csv_format(self, runner, sample_text):
        """Test CSV output format."""
        result = runner.invoke(main, ["--text-input", sample_text, "--format", "csv"])
        assert result.exit_code == 0
        # Check CSV header
        assert "keyword" in result.output.splitlines()[0]

    def test_ngram_size_option(self, runner, sample_text):
        """Test the ngram-size option."""
        result = runner.invoke(main, ["--text-input", sample_text, "--ngram-size", "1"])
        assert result.exit_code == 0
        # With ngram-size=1, we should only see single words
        for line in result.output.splitlines():
            if "keyword" not in line and line.strip():  # Skip header and empty lines
                # Count words in each keyword
                assert len(line.split()) == 1 or " " not in line

    def test_top_option(self, runner, sample_text):
        """Test the top option to limit number of keywords."""
        result = runner.invoke(main, ["--text-input", sample_text, "--top", "3"])
        assert result.exit_code == 0
        # Count actual keywords (excluding header and separators)
        keywords = [
            line
            for line in result.output.splitlines()
            if line.strip() and "keyword" not in line
        ]
        assert len(keywords) <= 3

    def test_language_option(self, runner, sample_text):
        """Test the language option."""
        # Try with English
        result_en = runner.invoke(
            main, ["--text-input", sample_text, "--language", "en"]
        )
        assert result_en.exit_code == 0

        # Try with another language if available
        languages = get_available_languages()
        if len(languages) > 1:
            other_lang = next(lang for lang in languages if lang != "en")
            result_other = runner.invoke(
                main, ["--text-input", sample_text, "--language", other_lang]
            )
            assert result_other.exit_code == 0
            # Results should be different with different languages
            assert result_en.output != result_other.output

    def test_error_no_input(self, runner):
        """Test error when no input is provided."""
        result = runner.invoke(main, [])

        assert (
            "Error: You must specify either --text-input or --input-file"
            in result.output
        )

    def test_error_both_inputs(self, runner, sample_text, sample_file):
        """Test error when both inputs are provided."""
        result = runner.invoke(
            main, ["--text-input", sample_text, "--input-file", sample_file]
        )

        assert (
            "Error: You can specify either --text-input or --input-file, but not both"
            in result.output
        )

    def test_nonexistent_file(self, runner):
        """Test error when input file does not exist."""
        result = runner.invoke(main, ["--input-file", "nonexistent_file.txt"])
        assert result.exit_code != 0  # Should fail
