"""CLI para extração de palavras-chave utilizando YAKE!"""

import sys
import click
from tabulate import tabulate
import yake

@click.command()
@click.option(
    "-ti", "--text_input",
    help="Input text, SURROUNDED by single quotes(')",
    required=False,
)
@click.option(
    "-i", "--input_file",
    help="Input file",
    required=False,
)
@click.option(
    "-l", "--language",
    default="en",
    help="Language",
    required=False,
)
@click.option(
    "-n", "--ngram_size",
    default=3,
    help="Max size of the ngram",
    type=int,
)
@click.option(
    "-df", "--dedup_func", 
    help="Deduplication function",
    default="seqm",
    type=click.Choice(["leve", "jaro", "seqm"]),
)
@click.option(
    "-dl", "--dedup_lim",
    help="Deduplication limiar",
    default=0.9,
    type=float,
)
@click.option(
    "-ws", "--window_size",
    help="Window size",
    default=1,
    type=int,
)
@click.option(
    "-t", "--top",
    help="Number of keyphrases to extract",
    default=10,
    type=int,
)
@click.option(
    "-v", "--verbose",
    count=True,
    help="Verbose output",
)
@click.pass_context
def keywords(ctx,
    text_input, input_file, language, ngram_size, dedup_func, dedup_lim, window_size, top, verbose
):
    """Extract keywords using YAKE!"""

    def run_yake(text_content):
        extractor = yake.KeywordExtractor(
            lan=language, n=ngram_size, dedupLim=dedup_lim,
            dedupFunc=dedup_func, windowsSize=window_size, top=top
        )
        results = extractor.extract_keywords(text_content)

        table = [
            {"keyword": kw[0], "score": kw[1]} if verbose else {"keyword": kw[0]}
            for kw in results
        ]
        print(tabulate(table, headers="keys"))

    if text_input and input_file:
        print("Specify either an input file or direct text input, not both!")
        sys.exit(1)
    elif not text_input and not input_file:
        print("Specify either an input file or direct text input")
        sys.exit(1)

    if text_input:
        run_yake(text_input)
    else:
        try:
            with open(input_file, encoding="utf-8") as f:
                run_yake(f.read())
        except FileNotFoundError:
            print(f"File '{input_file}' not found.")
            sys.exit(1)

