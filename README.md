# YAKE! (Yet Another Keyword Extractor)

[![ECIR'18 Best Short Paper](https://img.shields.io/badge/ECIR'18-Best%20Short%20Paper-brightgreen.svg)](http://ecir2018.org)
[![PyPI Downloads](https://static.pepy.tech/badge/yake)](https://pepy.tech/projects/yake)
[![PyPI - Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://pypi.org/project/YAKE/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)] (https://colab.research.google.com/github/LIAAD/yake/blob/gh-pages/1YAKE.ipynb)

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

#### Usage (Command line)

How to use it on your favorite command line

``` bash
Usage: yake [OPTIONS]

Options:
	  -ti, --text_input TEXT          Input text, SURROUNDED by single quotes (')
	  -i, --input_file TEXT           Input file
	  -l, --language TEXT             Language
	  -n, --ngram-size INTEGER        Max size of the ngram.
	  -df, --dedup-func [leve|jaro|seqm] *
									  Deduplication function.
	  -dl, --dedup-lim FLOAT          Deduplication limiar.
	  -ws, --window-size INTEGER      Window size.
	  -t, --top INTEGER               Number of keyphrases to extract
	  -v, --verbose                   Gets detailed information (such as the score)
	  --help                          Show this message and exit.
```

Don't know which Deduplication function to use, see more [here](https://liaad.github.io/yake/docs/-getting-started#keyword-deduplication-methods)

#### Usage (Python)

```python
import yake

text = "Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom  and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its   launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner "

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

#### Output
The lower the score, the more relevant the keyword is.
``` bash
('google', 0.026580863364597897)
('kaggle', 0.0289005976239829)
('ceo anthony goldbloom', 0.029946071606210194)
('san francisco', 0.048810837074825336)
('anthony goldbloom declined', 0.06176910090701819)
('google cloud platform', 0.06261974476422487)
('co-founder ceo anthony', 0.07357749587020043)
('acquiring kaggle', 0.08723571551039863)
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
- 🔌 Documentation site: [https://liaad.github.io/yake/docs/--home](https://liaad.github.io/yake/docs/--home)
- 📦 Python package: [https://github.com/LIAAD/yake_demo](https://github.com/LIAAD/yake_demo)
- 💻 Pypi: [https://pypi.org/project/yake/](https://pypi.org/project/yake/)

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