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

## Basic Usage

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

## Multilingual Support

YAKE! supports multiple languages. Example with Portuguese text:

```python
text_pt = "YAKE! é um extrator de palavras-chave automático não supervisionado."
custom_kw_extractor = yake.KeywordExtractor(lan="pt")
keywords = custom_kw_extractor.extract_keywords(text_pt)
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
- 🔌 Documentation site: [Documentation](http://github.io/yakerf/docs/)
- 📦 Python package: [GitHub](https://github.com/LIAAD/yake_demo)

## Citation

If you use YAKE in your research, please cite:

```
Campos, R., Mangaravite, V., Pasquali, A., Jatowt, A., Jorge, A., Nunes, C. and Jatowt, A. (2020).
YAKE! Keyword Extraction from Single Documents using Multiple Local Features.
Information Sciences Journal. Elsevier, Vol 509, pp 257-289.
```

```
Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018).
A Text Feature Based Automatic Keyword Extraction Method for Single Documents.
ECIR 2018. Lecture Notes in Computer Science, vol 10772, pp. 684-691.
```

## Awards

🏆 [ECIR'18](http://ecir2018.org) Best Short Paper