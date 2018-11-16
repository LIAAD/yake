# -*- coding: utf-8 -*-

"""Console script for yake."""

import click
import yake

@click.command()
@click.option("-i",'--input_file', help='Input file', required=True)
@click.option("-l",'--language', default="en", help='Language', required=False)

@click.option('-n','--ngram-size', default=3, help='Max size of the ngram.', required=False, type=int)
@click.option('-df','--dedup-func', help='Deduplication function.', default='seqm', type=click.Choice(['leve', 'jaro', 'seqm']), required=False)
@click.option('-dl','--dedup-lim', type=float, help='Deduplication limiar.', default=.9, required=False)

@click.option('-ws','--window-size', type=int, help='Window size.', default=1, required=False)
@click.option('-t','--top', type=int,  help='Number of keyphrases to extract', default=10, required=False)
@click.option('-v','--verbose', count=True, required=False)

def keywords(input_file, language, ngram_size, verbose=False, dedup_func="seqm", dedup_lim=.9, window_size=1, top=10):
	
	with open(input_file) as fpath:
		text_content = fpath.read()

		myake = yake.KeywordExtractor(lan=language,n=ngram_size, dedupLim=dedup_lim, dedupFunc=dedup_func, windowsSize=window_size, top=top)
		results = myake.extract_keywords(text_content)

		for kw in results:
			if(verbose):
				print(kw[0], kw[1])
			else:
				print(kw[1])

if __name__ == "__main__":
	main()