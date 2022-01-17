---
layout: default
title: Getting started
nav_order: 2
---

# Quick Start
{: .no_toc }

## Installing YAKE!

Installing Yake using pip:

``` bash
pip install git+https://github.com/LIAAD/yake
```

## Usage (Command line)

How to use it on your using the command line:

``` bash
Usage: yake [OPTIONS]

Options:
	-ti, --text_input TEXT          Input text, SURROUNDED by single quotes(\')
	-i, --input_file TEXT           Input file
	-l, --language TEXT             Language
	-n, --ngram-size INTEGER        Max size of the ngram.
	-df, --dedup-func [leve|jaro|seqm]
									Deduplication function.
	-dl, --dedup-lim FLOAT          Deduplication limiar.
	-ws, --window-size INTEGER      Window size.
	-t, --top INTEGER               Number of keyphrases to extract
	-v, --verbose			Gets detailed information (such as the score)
	--help                          Show this message and exit.
``` 
## Usage (Python)

How to use it using Python:

``` python
import yake

text = """Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning 
competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud 
Next conference in San Francisco this week, the official announcement could come as early as tomorrow. 
Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. 
Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, 
was founded by Goldbloom  and Ben Hamner in 2010. 
The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, 
it has managed to stay well ahead of them by focusing on its specific niche. 
The service is basically the de facto home for running data science and machine learning competitions. 
With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, 
it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow 
and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, 
Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. 
That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google 
will keep the service running - likely under its current name. While the acquisition is probably more about 
Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition 
and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can 
share this code on the platform (the company previously called them 'scripts'). 
Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with 
that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) 
since its   launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant,
Google chief economist Hal Varian, Khosla Ventures and Yuri Milner """
```

### Simple usage using default parameters
```bash
kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(text)

for kw in keywords:
    print(kw)
```

### Specifying custom parameters
```bash
language = "en"
max_ngram_size = 3
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 20

kw_extractor = yake.KeywordExtractor(lan=language, 
                                     n=max_ngram_size, 
                                     dedupLim=deduplication_thresold, 
                                     dedupFunc=deduplication_algo, 
                                     windowsSize=windowSize, 
                                     top=numOfKeywords)
                                            
keywords = kw_extractor.extract_keywords(text)

for kw in keywords:
    print(kw)
```

### Output
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
('ceo anthony', 0.08915156857226395)
('anthony goldbloom', 0.09123482372372106)
('machine learning', 0.09147989238151344)
('kaggle co-founder ceo', 0.093805063905847)
('data', 0.097574333771058)
('google cloud', 0.10260128641464673)
('machine learning competitions', 0.10773000650607861)
('francisco this week', 0.11519915079240485)
('platform', 0.1183512305596321)
('conference in san', 0.12392066376108138)
('service', 0.12546743261462942)
('goldbloom', 0.14611408778815776)
```
