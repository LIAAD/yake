# YAKE! (Yet Another Keyword Extractor)

[![ECIR'18 Best Short Paper](https://img.shields.io/badge/ECIR'18-Best%20Short%20Paper-brightgreen.svg)](http://ecir2018.org)

YAKE! is a lightweight unsupervised automatic keyword extraction method that uses text statistical features to select the most important keywords from a document. It requires no training, external corpus, or dictionaries, and works across multiple languages and domains regardless of text size.

## Features

- 🚀 Unsupervised approach
- 🌐 Language and domain independent
- 📄 Single-document focused
- 🧠 No training or dictionaries required

## Quick Installation

```bash
pip install git+https://github.com/LIAAD/yake
```

or

```bash
pip install yake
```

## Basic Usage

#### Usage (Python)

```python
import yake

text = "YAKE! is a light-weight unsupervised automatic keyword extraction method which rests on text statistical features extracted from single documents to select the most important keywords of a text."

# Simple usage with default parameters
kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(text)

for kw, score in keywords:
    print(f"{kw} ({score})")

# With custom parameters
custom_kw_extractor = yake.KeywordExtractor(
    lan="en",              # language
    n=3,                   # ngram size
    dedupLim=0.9,          # deduplication threshold
    dedupFunc='seqm',      # deduplication function
    windowsSize=1,         # context window
    top=10,                # number of keywords to extract
    features=None          # custom features
)

keywords = custom_kw_extractor.extract_keywords(text)
```

#### Usage (Command line)

How to use it on your favorite command line

``` bash
Usage: yake [OPTIONS]

Options:
	  -ti, --text_input TEXT          Input text, SURROUNDED by single quotes(')
	  -i, --input_file TEXT           Input file
	  -l, --language TEXT             Language
	  -n, --ngram-size INTEGER        Max size of the ngram.
	  -df, --dedup-func [leve|jaro|seqm]
									  Deduplication function.
	  -dl, --dedup-lim FLOAT          Deduplication limiar.
	  -ws, --window-size INTEGER      Window size.
	  -t, --top INTEGER               Number of keyphrases to extract
	  -v, --verbose                   Gets detailed information (such as the score)
	  --help                          Show this message and exit.
```

## Multilingual Support

YAKE! supports multiple languages. Example with Portuguese text:

```python
text = "Alvor – encantadora vila. A aldeia piscatória de Alvor está situada no estuário do Rio Alvor e apesar da evolução constante do turismo no Algarve, mantém a sua arquitetura baixa e encanto da cidade velha, com ruas estreitas de paralelepípedos que nos levam até à Ria de Alvor, uma das belezas naturais mais impressionantes de Portugal. Há muitos hotéis em Alvor por onde escolher e adequar às exigências das suas férias, quanto a gosto e orçamento, bem como uma série de alojamento autossuficiente para aqueles que preferem ter um pouco mais de liberdade durante a sua estadia na Região de Portimão. Há muito para fazer e descobrir em Alvor, quer seja passar os seus dias descobrindo a rede de ruas desta encantadora vila de pescadores, explorar as lojas, ir para a praia para se divertir entre brincadeiras na areia e mergulhos no mar, ou descobrir a flora e fauna da área classificada da Ria de Alvor. O charme de Alvor não se esgota na Vila. Ficar hospedado em Alvor vai proporcionar-lhe momento mágicos entre paisagens de colinas, lagoas rasas e vistas panorâmicas sobre o Oceano Atlântico. Terá oportunidade de praticar o seu swing num dos campos de golfe de classe mundial e explorar as principais atrações históricas e alguns dos segredos mais bem escondidos do Algarve, nas proximidades, em Portimão e Mexilhoeira Grande. Consulte a lista dos nossos parceiros e escolha o hotel em Alvor, onde ficar durante as suas férias no Algarve."
custom_kw_extractor = yake.KeywordExtractor(lan="pt")
keywords = custom_kw_extractor.extract_keywords(text)
```

## Text Highlighting

YAKE! includes a highlighting feature to mark keywords in text:

```python
from yake.highlight import TextHighlighter

th = TextHighlighter(max_ngram_size=3)
highlighted_text = th.highlight(text, keywords)

# With custom HTML tags
custom_th = TextHighlighter(
    max_ngram_size=3,
    highlight_pre="<span class='keyword'>",
    highlight_post="</span>"
)
```

## Where to Find YAKE!

- 🌐 Online demo: [http://yake.inesctec.pt](http://yake.inesctec.pt)
- 🔌 Documentation site: [https://tiagolv.github.io/yakerf/docs](https://tiagolv.github.io/yakerf/docs)
- 📦 Python package: [https://github.com/LIAAD/yake_demo](https://github.com/LIAAD/yake_demo)
- 💻 Pypi [https://pypi.org/project/yake/](https://pypi.org/project/yake/)

## Citation

If you use YAKE in your research, please cite the best suited:

Campos, R., Mangaravite, V., Pasquali, A., Jatowt, A., Jorge, A., Nunes, C. and Jatowt, A. (2020).
YAKE! Keyword Extraction from Single Documents using Multiple Local Features.
Information Sciences Journal. Elsevier, Vol 509, pp 257-289. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_63)

Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018).
A Text Feature Based Automatic Keyword Extraction Method for Single Documents.
ECIR 2018. Lecture Notes in Computer Science, vol 10772, pp. 684-691. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_80)

Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). YAKE! Collection-independent Automatic Keyword Extractor. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 806 - 810. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_80)

## Awards

🏆 [ECIR'18](http://ecir2018.org) Best Short Paper