Yet Another Keyword Extractor (Yake)
========================================

Unsupervised Approach for Automatic Keyword Extraction using Text Features.

YAKE! is a light-weight unsupervised automatic keyword extraction method which rests on text statistical features extracted from single documents to select the most important keywords of a text. Our system does not need to be trained on a particular set of documents, neither it depends on dictionaries, external-corpus, size of the text, language or domain. To demonstrate the merits and the significance of our proposal, we compare it against ten state-of-the-art unsupervised approaches (TF.IDF, KP-Miner, RAKE, TextRank, SingleRank, ExpandRank, TopicRank, TopicalPageRank, PositionRank and MultipartiteRank), and one supervised method (KEA). Experimental results carried out on top of twenty datasets (see Comparison with state-of-the-art) show that our methods significantly outperform state-of-the-art methods under a number of collections of different sizes, languages or domains. In addition to the python package here described, we also make available a [__demo__](http://yake.inesctec.pt) and an [__API__](http://yake.inesctec.pt/apidocs/#!/available_methods/post_yake_v2_extract_keywords).


Main Features
-------------

* Unsupervised approach
* Corpus-Independent
* Domain and Language Independent
* Single-Document

Benchmark
-------------

YAKE!, generically outperforms, statistical methods (tf.idf, kp-miner and rake), state-of-the-art graph-based methods (TextRank, SingleRank, TopicRank, TopicalPageRank, PositionRank, MultipartiteRank and ExpandRank) ans supervised learning methods (KEA) across different datasets, languages and domains. The results listed in the table refer to F1 at 10 scores. Bold face marks the current best results for that specific dataset.


| Dataset                                                                           | Language | #Docs | YAKE      | Previous best | Method                                                                                                           |
| --------------------------------------------------------------------------------- | -------- | ----- | --------- | -------------------------------------------------------------------------------------------------------------------------------- |
| [__110-PT-BN-KP__](https://github.com/LIAAD/KeywordExtractor-Datasets#110)        | PT       | 110   | **0.500** | 0.275          [__SingleRank (Wan and Xiao, 2008)__](http://www.aclweb.org/anthology/C08-1122.pdf)                              |
| [__500N-KPCrowd-v1.1__](https://github.com/LIAAD/KeywordExtractor-Datasets#500)   | EN       | 500   | **0.173** | 0.172          [__TopicRank (Bougouin et al., 2013)__](http://aclweb.org/anthology/I13-1062.pdf)                                |
| [__Inspec__](https://github.com/LIAAD/KeywordExtractor-Datasets#Inspec)           | EN       | 2000  | 0.316     | **0.378**      [__SingleRank (Wan and Xiao, 2008)__](http://www.aclweb.org/anthology/C08-1122.pdf)                              |
| [__Krapivin2009__](https://github.com/LIAAD/KeywordExtractor-Datasets#Krapivin)   | EN       | 2304  | 0.170     | **0.227**      [__KPMiner (El-Beltagy and Rafea, 2010)__](http://www.aclweb.org/anthology/S10-1041.pdf)                         |
| [__Nguyen2007__](https://github.com/LIAAD/KeywordExtractor-Datasets#Nguyen)       | EN       | 209   | 0.256     | **0.314**      [__KPMiner (El-Beltagy and Rafea, 2010)__](http://www.aclweb.org/anthology/S10-1041.pdf)                         |
| [__PubMed__](https://github.com/LIAAD/KeywordExtractor-Datasets#PubMed)           | EN       | 500   | 0.106     | **0.216**      [__KEA (Witten et al., 2005)__](https://www.cs.waikato.ac.nz/ml/publications/2005/chap_Witten-et-al_Windows.pdf) |
| [__Schutz2008__](https://github.com/LIAAD/KeywordExtractor-Datasets#Schutz)       | EN       | 1231  | 0.196     | **0.258**      [__TopicRank (Bougouin et al., 2013)__](http://aclweb.org/anthology/I13-1062.pdf)                                |
| [__www__](https://github.com/LIAAD/KeywordExtractor-Datasets#www)                 | EN       | 1330  | **0.172** | 0.130          TFIDF                                                                                                            |
| [__kdd__](https://github.com/LIAAD/KeywordExtractor-Datasets#kdd)                 | EN       | 755   | **0.156** | 0.115          TFIDF                                                                                                            |
| [__SemEval2010__](https://github.com/LIAAD/KeywordExtractor-Datasets#SemEval2010) | EN       | 243   | 0.211     | **0.261**      [__KPMiner (El-Beltagy and Rafea, 2010)__](http://www.aclweb.org/anthology/S10-1041.pdf)                         |
| [__SemEval2017__](https://github.com/LIAAD/KeywordExtractor-Datasets#SemEval2017) | EN       | 493   | 0.329     | **0.449**      [__SingleRank (Wan and Xiao, 2008)__](http://www.aclweb.org/anthology/C08-1122.pdf)                              |
| [__cacic__](https://github.com/LIAAD/KeywordExtractor-Datasets#cacic)             | ES       | 888   | **0.196** | 0.155          [__KEA (Witten et al., 2005)__](https://www.cs.waikato.ac.nz/ml/publications/2005/chap_Witten-et-al_Windows.pdf) |
| [__citeulike180__](https://github.com/LIAAD/KeywordExtractor-Datasets#citeulike)  | EN       | 183   | 0.256     | **0.317**      [__KEA (Witten et al., 2005)__](https://www.cs.waikato.ac.nz/ml/publications/2005/chap_Witten-et-al_Windows.pdf) |
| [__fao30__](https://github.com/LIAAD/KeywordExtractor-Datasets#fao30)             | EN       | 30    | **0.184** | 0.183          [__KPMiner (El-Beltagy and Rafea, 2010)__](http://www.aclweb.org/anthology/S10-1041.pdf)                         |
| [__fao780__](https://github.com/LIAAD/KeywordExtractor-Datasets#fao780)           | EN       | 779   | **0.187** | 0.174          [__KPMiner (El-Beltagy and Rafea, 2010)__](http://www.aclweb.org/anthology/S10-1041.pdf)                         |
| [__pak2018__](https://github.com/LIAAD/KeywordExtractor-Datasets#pak)             | PL       | 50    | **0.086** | 0.059          TFIDF                                                                                                            |
| [__theses100__](https://github.com/LIAAD/KeywordExtractor-Datasets#theses)        | EN       | 100   | 0.111     | **0.158**      [__KPMiner (El-Beltagy and Rafea, 2010)__](http://www.aclweb.org/anthology/S10-1041.pdf)                         |
| [__wicc__](https://github.com/LIAAD/KeywordExtractor-Datasets#wicc)               | ES       | 1640  | **0.256** | 0.167          [__KEA (Witten et al., 2005)__](https://www.cs.waikato.ac.nz/ml/publications/2005/chap_Witten-et-al_Windows.pdf) |
| [__wiki20__](https://github.com/LIAAD/KeywordExtractor-Datasets#wiki20)           | EN       | 20    | **0.162** | 0.156          [__KPMiner (El-Beltagy and Rafea, 2010)__](http://www.aclweb.org/anthology/S10-1041.pdf)                         |
| [__WikiNews__](https://github.com/LIAAD/KeywordExtractor-Datasets#WKC)            | FR       | 100   | **0.450** | 0.337          TFIDF                                                                                                            |

Rationale
-------------

Extracting keywords from texts has become a challenge for individuals and organizations as the information grows in complexity and size. The need to automate this task so that texts can be processed in a timely and adequate manner has led to the emergence of automatic keyword extraction tools. Despite the advances, there is a clear lack of multilingual online tools to automatically extract keywords from single documents. Yake! is a novel feature-based system for multi-lingual keyword extraction, which supports texts of different sizes, domain or languages. Unlike other approaches, Yake! does not rely on dictionaries nor thesauri, neither is trained against any corpora. Instead, it follows an unsupervised approach which builds upon features extracted from the text, making it thus applicable to documents written in different languages without the need for further knowledge. This can be beneficial for a large number of tasks and a plethora of situations where the access to training corpora is either limited or restricted.


Please cite the following works when using YAKE
------------

Campos, R., Mangaravite, V., Pasquali, A., Jorge, A., Nunes, C., & Jatowt, A. (2018).
A Text Feature Based Automatic Keyword Extraction Method for Single Documents
Proceedings of the 40th European Conference on Information Retrieval (ECIR'18), Grenoble, France. March 26 – 29.
https://link.springer.com/chapter/10.1007/978-3-319-76941-7_63

Campos, R., Mangaravite, V., Pasquali, A., Jorge, A., Nunes, C., & Jatowt, A. (2018).
YAKE! Collection-independent Automatic Keyword Extractor
Proceedings of the 40th European Conference on Information Retrieval (ECIR'18), Grenoble, France. March 26 – 29
https://link.springer.com/chapter/10.1007/978-3-319-76941-7_80

Requirements
-------------
Python3


Installation
-------------

To install Yake using pip

	pip install git+https://github.com/LIAAD/yake

To upgrade using pip::

	pip install git+https://github.com/LIAAD/yake –upgrade

Usage
---------

Command line
************************
How to use it on your favorite command line

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
		  -v, --verbose
		  --help                          Show this message and exit.

Python
************************
How to use it on Python

	import yake

	text_content = """
		Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning
		competitions. Details about the transaction remain somewhat vague , but given that Google is hosting
		its Cloud Next conference in San Francisco this week, the official announcement could come as early
		as tomorrow.  Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the
		acquisition is happening. Google itself declined 'to comment on rumors'.
	"""

	# assuming default parameters
	simple_kwextractor = yake.KeywordExtractor()
	keywords = simple_kwextractor.extract_keywords(text_content)

	for kw in keywords:
		print(kw)

	# specifying parameters
	custom_kwextractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.8, windowsSize=2, top=20)
	keywords = custom_kwextractor.extract_keywords(text_content)

	for kw in keywords:
		print(kw)


Related projects
-------------

yake-dockerfile
************************
https://github.com/feup-infolab/yake-dockerfile - Dockerfile for building an image for this package. 

Credits to https://github.com/silvae86


`pke` - python keyphrase extraction
************************



https://github.com/boudinfl/pke - `pke` is an **open source** python-based **keyphrase extraction** toolkit. It
provides an end-to-end keyphrase extraction pipeline in which each component can
be easily modified or extended to develop new models. `pke` also allows for 
easy benchmarking of state-of-the-art keyphrase extraction models, and 
ships with supervised models trained on the SemEval-2010 dataset (http://aclweb.org/anthology/S10-1004).

Credits to https://github.com/boudinfl
