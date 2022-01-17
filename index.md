# Yet Another Keyword Extractor (Yake)

Unsupervised Approach for Automatic Keyword Extraction using Text Features.

YAKE! is a light-weight unsupervised automatic keyword extraction method which rests on text statistical features extracted from single documents to select the most important keywords of a text. Our system does not need to be trained on a particular set of documents, neither it depends on dictionaries, external-corpus, size of the text, language or domain. To demonstrate the merits and the significance of our proposal, we compare it against ten state-of-the-art unsupervised approaches (TF.IDF, KP-Miner, RAKE, TextRank, SingleRank, ExpandRank, TopicRank, TopicalPageRank, PositionRank and MultipartiteRank), and one supervised method (KEA). Experimental results carried out on top of twenty datasets (see Benchmark section below) show that our methods significantly outperform state-of-the-art methods under a number of collections of different sizes, languages or domains. In addition to the python package here described, we also make available a <a href="http://yake.inesctec.pt" target="_blank">demo</a>, an <a href="http://yake.inesctec.pt/apidocs/#!/available_methods/post_yake_v2_extract_keywords" target="_blank">API</a> and a <a href="https://play.google.com/store/apps/details?id=com.yake.yake" target="_blank">mobile app</a>.

## Main Features

* Unsupervised approach
* Corpus-Independent
* Domain and Language Independent
* Single-Document

## Benchmark

For Benchmark results check out our paper published on Information Science Journal (see the references section). 

## Rationale

Extracting keywords from texts has become a challenge for individuals and organizations as the information grows in complexity and size. The need to automate this task so that texts can be processed in a timely and adequate manner has led to the emergence of automatic keyword extraction tools. Despite the advances, there is a clear lack of multilingual online tools to automatically extract keywords from single documents. Yake! is a novel feature-based system for multi-lingual keyword extraction, which supports texts of different sizes, domain or languages. Unlike other approaches, Yake! does not rely on dictionaries nor thesauri, neither is trained against any corpora. Instead, it follows an unsupervised approach which builds upon features extracted from the text, making it thus applicable to documents written in different languages without the need for further knowledge. This can be beneficial for a large number of tasks and a plethora of situations where the access to training corpora is either limited or restricted.

## Installing YAKE!

To install Yake using pip:

``` bash
pip install git+https://github.com/LIAAD/yake
```

To upgrade using pip:

``` bash
pip install git+https://github.com/LIAAD/yake –-upgrade
```
#### Usage (Command line)

How to use it on your favorite command line
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
### Usage (Python)

How to use it on Python

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

#### assuming default parameters
```bash
kw_extractor = yake.KeywordExtractor()
keywords = kw_extractor.extract_keywords(text)

for kw in keywords:
	print(kw)
```

#### specifying parameters
```bash
language = "en"
max_ngram_size = 3
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 20

custom_kw_extractor = yake.KeywordExtractor(lan=language, 
                                            n=max_ngram_size, 
                                            dedupLim=deduplication_thresold, 
                                            dedupFunc=deduplication_algo, 
                                            windowsSize=windowSize, 
                                            top=numOfKeywords, 
                                            features=None)
                                            
keywords = custom_kw_extractor.extract_keywords(text)

for kw in keywords:
    print(kw)
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

## References

Please cite the following works when using YAKE

In-depth journal paper at Information Sciences Journal
Campos, R., Mangaravite, V., Pasquali, A., Jatowt, A., Jorge, A., Nunes, C. and Jatowt, A. (2020). YAKE! Keyword Extraction from Single Documents using Multiple Local Features. In Information Sciences Journal. Elsevier, Vol 509, pp 257-289. [pdf](https://doi.org/10.1016/j.ins.2019.09.013)

Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). A Text Feature Based Automatic Keyword Extraction Method for Single Documents. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 684 - 691. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_63) (ECIR'18 Best Short Paper)

Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). YAKE! Collection-independent Automatic Keyword Extractor. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 806 - 810. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_80)




