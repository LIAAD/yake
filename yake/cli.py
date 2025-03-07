#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for YAKE keyword extraction."""

import sys
import os
import click
from typing import Optional, List
import yake
from tabulate import tabulate


def get_available_languages() -> List[str]:
    """Get available languages from stopwords files."""
    stopwords_dir = os.path.join(os.path.dirname(__file__), "StopwordsList")
    languages = []
    try:
        for filename in os.listdir(stopwords_dir):
            if filename.startswith("stopwords_") and filename.endswith(".txt"):
                lang = filename.replace("stopwords_", "").replace(".txt", "")
                languages.append(lang)
        return sorted(languages) or ["en"]  # Fallback to English if no languages found
    except (FileNotFoundError, NotADirectoryError):
        return ["en"]  # Fallback to English if directory issues


@click.command()
@click.option(
    "-ti", "--text-input", help="Input text (surrounded by single quotes)", type=str
)
@click.option(
    "-i",
    "--input-file",
    help="Path to input file",
    type=click.Path(exists=True, readable=True, file_okay=True),
)
@click.option(
    "-l",
    "--language",
    help="Language for stopwords",
    default="en",
    show_default=True,
    type=str,
)
@click.option(
    "-n",
    "--ngram-size",
    help="Maximum size of the n-gram",
    default=3,
    show_default=True,
    type=int,
)
@click.option(
    "-df",
    "--dedup-func",
    help="Deduplication function",
    default="seqm",
    show_default=True,
    type=click.Choice(["leve", "jaro", "seqm"], case_sensitive=False),
)
@click.option(
    "-dl",
    "--dedup-lim",
    help="Deduplication threshold",
    default=0.9,
    show_default=True,
    type=float,
)
@click.option(
    "-ws",
    "--window-size",
    help="Window size for feature extraction",
    default=1,
    show_default=True,
    type=int,
)
@click.option(
    "-t",
    "--top",
    help="Number of keywords to extract",
    default=10,
    show_default=True,
    type=int,
)
@click.option("-v", "--verbose", help="Show scores in output", is_flag=True)
@click.option(
    "-f",
    "--format",
    help="Output format",
    default="table",
    type=click.Choice(["table", "json", "csv"]),
    show_default=True,
)
@click.option(
    "--list-languages", is_flag=True, help="List available languages for stopwords"
)
def main(
    text_input: Optional[str],
    input_file: Optional[str],
    language: str,
    ngram_size: int,
    dedup_func: str,
    dedup_lim: float,
    window_size: int,
    top: int,
    verbose: bool,
    format: str,
    list_languages: bool,
) -> int:
    """YAKE: Yet Another Keyword Extractor.

    Extract keywords from text using unsupervised approach.
    """
    # Handle language listing request
    if list_languages:
        available_languages = get_available_languages()
        click.echo("Available languages for stopwords:")
        for lang in available_languages:
            click.echo(f"- {lang}")
        return 0

    def process_text(text_content: str) -> None:
        """Process text content and print keywords.

        Args:
            text_content: Text to process
        """
        # Initialize keyword extractor
        extractor = yake.KeywordExtractor(
            lan=language,
            n=ngram_size,
            dedup_lim=dedup_lim,
            dedup_func=dedup_func,
            window_size=window_size,
            top=top,
        )

        # Extract keywords
        keywords = extractor.extract_keywords(text_content)

        # Prepare output table
        table = []
        for kw in keywords:
            if verbose:
                table.append({"keyword": kw[0], "score": kw[1]})
            else:
                table.append({"keyword": kw[0]})

        # Print results based on format
        if format == "json":
            import json

            click.echo(json.dumps(table))
        elif format == "csv":
            import csv
            import io

            output = io.StringIO()
            headers = list(table[0].keys()) if table else []
            writer = csv.DictWriter(output, fieldnames=headers)
            writer.writeheader()
            writer.writerows(table)
            click.echo(output.getvalue())
        else:  # Default: table format
            click.echo(tabulate(table, headers="keys"))

    # Validate input parameters
    if text_input and input_file:
        click.echo(
            "Error: You can specify either --text-input or --input-file, but not both.",
            err=True,
        )
        return 1
    elif not text_input and not input_file:
        click.echo(
            "Error: You must specify either --text-input or --input-file.", err=True
        )
        return 1

    # Process the input
    try:
        if text_input:
            process_text(text_input)
        else:
            with open(input_file, "r", encoding="utf-8") as f:
                process_text(f.read())
        return 0
    except Exception as e:
        click.echo(f"Error processing text: {str(e)}", err=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
