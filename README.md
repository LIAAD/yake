
# YAKE! - Yet Another Keyword Extractor

YAKE! is a lightweight, unsupervised, automatic keyword extraction method that uses text statistical features to select the most important keywords from a document.


## Key Features

- Unsupervised: No training data required
- Language Independent: Works across different languages
- Domain Independent: Effective for various types of content
- Single-Document: Designed to extract keywords from individual documents

## Installation

```bash
pip install git+https://github.com/LIAAD/yake
```

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install the package

```bash
uv sync
```

### Install in development mode

```bash
uv pip install -e ".[dev]"
```


## Basic Usage

### Python API

```python
import yake

text = "Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow."

# Simple extraction with default parameters
kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(text)

for kw, score in keywords:
    print(f"{kw} ({score})")
```


### Custom Parameters

```python
# Configure the extractor with custom parameters
custom_kw_extractor = yake.KeywordExtractor(
    lan="en",                # Language
    n=3,                     # Maximum ngram size
    dedup_lim=0.9,            # Deduplication threshold
    dedup_func="seqm",        # Deduplication function
    window_size=1,           # Window size
    top=20                   # Number of keywords to extract
)

keywords = custom_kw_extractor.extract_keywords(text)
```


### Command Line

```bash
yake -ti "Your text goes here" -l en -n 3 -v
```

Options:

```
    -ti, --text_input TEXT          Input text
    -i, --input_file TEXT           Input file
    -l, --language TEXT             Language 
    -n, --ngram-size INTEGER        Max size of the ngram
    -df, --dedup-func [leve|jaro|seqm]  Deduplication function
    -dl, --dedup-lim FLOAT          Deduplication threshold
    -ws, --window-size INTEGER      Window size
    -t, --top INTEGER               Number of keyphrases to extract
    -v, --verbose                   Show scores in output
```    


## Example Output

The lower the score, the more relevant the keyword is:

```
google (0.026580863364597897)
kaggle (0.0289005976239829)
san francisco (0.048810837074825336)
machine learning (0.09147989238151344)
data science (0.097574333771058)
```

## Multilingual Support

YAKE! supports multiple languages:

```python
# Portuguese example
custom_kw_extractor = yake.KeywordExtractor(lan="pt")
keywords = custom_kw_extractor.extract_keywords(portuguese_text)
```


## References
Please cite the following works when using YAKE

<b>Published at the Information Sciences Journal</b>

Campos, R., Mangaravite, V., Pasquali, A., Jatowt, A., Jorge, A., Nunes, C. and Jatowt, A. (2020). YAKE! Keyword Extraction from Single Documents using Multiple Local Features. In Information Sciences Journal. Elsevier, Vol 509, pp 257-289. [pdf](https://doi.org/10.1016/j.ins.2019.09.013)

<b>Conference papers at ECIR</b>

Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). A Text Feature Based Automatic Keyword Extraction Method for Single Documents. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 684 - 691. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_63)

Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). YAKE! Collection-independent Automatic Keyword Extractor. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 806 - 810. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_80) *(Best Short Paper Award)*


## Contributing

Please refer to the [CONTRIBUTING.rst](CONTRIBUTING.rst) file for details.
