=====
Usage
=====

Python API
==========

Basic Usage
-----------

To use YAKE in a project:

.. code-block:: python

    import yake

    text = """Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning
    competitions. Details about the transaction remain somewhat vague, but given that Google is hosting
    its Cloud Next conference in San Francisco this week, the official announcement could come as early
    as tomorrow."""

    # Simple extraction with default parameters
    kw_extractor = yake.KeywordExtractor()
    keywords = kw_extractor.extract_keywords(text)

    for kw, score in keywords:
        print(f"{kw} ({score})")

The lower the score, the more relevant the keyword is:

.. code-block:: none

    google (0.026580863364597897)
    kaggle (0.0289005976239829)
    san francisco (0.048810837074825336)
    machine learning (0.09147989238151344)
    data science (0.097574333771058)

Custom Parameters
----------------

You can customize the keyword extraction process with various parameters:

.. code-block:: python

    # Configure the extractor with custom parameters
    custom_kw_extractor = yake.KeywordExtractor(
        lan="en",                 # Language
        n=3,                      # Maximum ngram size
        dedup_lim=0.9,            # Deduplication threshold
        dedup_func="seqm",        # Deduplication function
        window_size=1,            # Window size
        top=20                    # Number of keywords to extract
    )

    keywords = custom_kw_extractor.extract_keywords(text)


Multilingual Support
------------------

YAKE supports multiple languages:

.. code-block:: python

    # Portuguese example
    custom_kw_extractor = yake.KeywordExtractor(lan="pt")
    keywords = custom_kw_extractor.extract_keywords(portuguese_text)

Command Line Interface
=====================

YAKE can also be used from the command line:

.. code-block:: bash

    yake -ti "Your text goes here" -l en -n 3 -v

Options
-------

.. code-block:: none

    -ti, --text-input TEXT         Input text
    -i, --input-file TEXT          Input file
    -l, --language TEXT            Language 
    -n, --ngram-size INTEGER       Max size of the ngram
    -df, --dedup-func [leve|jaro|seqm]  Deduplication function
    -dl, --dedup-lim FLOAT         Deduplication threshold
    -ws, --window-size INTEGER     Window size
    -t, --top INTEGER              Number of keyphrases to extract
    -v, --verbose                  Show scores in output
    -f, --format [table|json|csv]  Output format
    --list-languages               List available languages for stopwords

List Available Languages:

.. code-block:: bash

    yake --list-languages

	
Example usage with a file:

.. code-block:: bash

    yake -i document.txt -l en -n 3 -t 20 -v


Output Formats
-------------

YAKE CLI supports multiple output formats:

1. Table format (default):

.. code-block:: bash

    yake -ti "Google is acquiring Kaggle" -v

Output:

.. code-block:: none

    +-----------+----------+
    | keyword   |    score |
    |-----------+----------|
    | google    | 0.026581 |
    | kaggle    | 0.028901 |
    +-----------+----------+

2. JSON format:

.. code-block:: bash

    yake -ti "Google is acquiring Kaggle" -v -f json

Output:

.. code-block:: none

    [{"keyword": "google", "score": 0.026580863364597897}, {"keyword": "kaggle", "score": 0.0289005976239829}]

3. CSV format:

.. code-block:: bash

    yake -ti "Google is acquiring Kaggle" -v -f csv

Output:

.. code-block:: none

    keyword,score
    google,0.026580863364597897
    kaggle,0.0289005976239829

