# -*- coding: utf-8 -*-

"""Console script for yake."""

import click
import yake
from tabulate import tabulate

@click.command()
@click.option("-ti",'--text_input', help='Input text, SURROUNDED by single quotes(\')', required=False)
@click.option("-i",'--input_file', help='Input file', required=False)
@click.option("-l",'--language', default="en", help='Language', required=False)

@click.option('-n','--ngram-size', default=3, help='Max size of the ngram.', required=False, type=int)
@click.option('-df','--dedup-func', help='Deduplication function.', default='seqm', type=click.Choice(['leve', 'jaro', 'seqm']), required=False)
@click.option('-dl','--dedup-lim', type=float, help='Deduplication limiar.', default=.9, required=False)

@click.option('-ws','--window-size', type=int, help='Window size.', default=1, required=False)
@click.option('-t','--top', type=int,  help='Number of keyphrases to extract', default=10, required=False)
@click.option('-v','--verbose', count=True, required=False)

def keywords(text_input, input_file, language, ngram_size, verbose=False, dedup_func="seqm", dedup_lim=.9, window_size=1, top=10):

	def run_yake(text_content):
		myake = yake.KeywordExtractor(lan=language, n=ngram_size, dedupLim=dedup_lim, dedupFunc=dedup_func,
									  windowsSize=window_size, top=top)
		results = myake.extract_keywords(text_content)

		table = []
		for kw in results:
			if (verbose):
				table.append({"keyword":kw[0], "score":kw[1]})
			else:
				table.append({"keyword":kw[0]})

		print(tabulate(table, headers="keys"))

	if text_input and input_file:
		print("You should specify either an input file or direct text input, but not both!")
		exit(1)
	elif not text_input and not input_file:
			print("You should specify either an input file or direct text input")
			exit(1)
	else:
		if text_input:
			run_yake(text_input)
		else:
			with open(input_file) as fpath:
				text_content = fpath.read()
				run_yake(text_content)

if __name__ == "__main__":
	keywords()
