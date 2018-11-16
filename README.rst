========================================
Yet Another Keyword Extractor (Yake)
========================================

Unsupervised Approach for Automatic Keyword Extraction using Text Features

* Documentation: https://pypi.python.org/pypi/yake.

Main Features
-------------

* Unsupervised approach
* Multi-Language Support 
* Single document

Rationale
-------------

Extracting keywords from texts has become a challenge for individuals and organizations as the information grows in complexity and size. The need to automate this task so that texts can be processed in a timely and adequate manner has led to the emergence of automatic keyword extraction tools. Despite the advances, there is a clear lack of multilingual online tools to automatically extract keywords from single documents. Yake! is a novel feature-based system for multi-lingual keyword extraction, which supports texts of different sizes, domain or languages. Unlike other approaches, Yake! does not rely on dictionaries nor thesauri, neither is trained against any corpora. Instead, it follows an unsupervised approach which builds upon features extracted from the text, making it thus applicable to documents written in different languages without the need for further knowledge. This can be beneficial for a large number of tasks and a plethora of situations where the access to training corpora is either limited or restricted.


Please cite the following works when using YAKE
------------

Campos, R., Mangaravite, V., Pasquali, A., Jorge, A., Nunes, C., & Jatowt, A. (2018).
A Text Feature Based Automatic Keyword Extraction Method for Single Documents
Proceedings of the 40th European Conference on Information Retrieval (ECIR'18), Grenoble, France. March 26 – 29.

Campos, R., Mangaravite, V., Pasquali, A., Jorge, A., Nunes, C., & Jatowt, A. (2018).
YAKE! Collection-independent Automatic Keyword Extractor
Proceedings of the 40th European Conference on Information Retrieval (ECIR'18), Grenoble, France. March 26 – 29


Requirements
-------------
Python3


Installation
-------------

To install Yake on your terminal ::

	pip install yake

To upgrade using pip::

	pip install yake –upgrade

Usage
---------

How to use it on your favorite command line::

	usage: yake [-h] -i INPUT [INPUT ...] [-df [{leve,jaro,seqm}]]
					 [-dl [DEDUP_LIM]] [-ws [WINDOWS_SIZE]] [-n [NGRAM_SIZE]]
					 [-t [TOP]]
					[-f {WRel,WFreq,WSpread,WCase,WPos,KPF} [{WRel,WFreq,WSpread,WCase,WPos,KPF} ...]]
					[-o [OUTPUT]]

	optional arguments:
	-h, 					--help					show this help message and exit
	-df [{leve,jaro,seqm}], --dedup-func [{leve,jaro,seqm}] Deduplication function.
	-dl [DEDUP_LIM], 		--dedup-lim [DEDUP_LIM] Deduplication limiar.
	-ws [WINDOWS_SIZE], 	--windows-size [WINDOWS_SIZE] Windows size.
	-n [NGRAM_SIZE], 		--ngram-size [NGRAM_SIZE] Max size of the ngram.
	-t [TOP], 				--top [TOP] Max size of rank.
	-f {WRel,WFreq,WSpread,WCase,WPos,KPF} [{WRel,WFreq,WSpread,WCase,WPos,KPF} ...], 
							--features {WRel,WFreq,WSpread,WCase,WPos,KPF} [{WRel,WFreq,WSpread,WCase,WPos,KPF} ...]
							Features to use.
	-o [OUTPUT], --output [OUTPUT] Output directory.

	required arguments:
	-i INPUT [INPUT ...], --input INPUT [INPUT ...] Dataset docs directory.


How to use it on Python::

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
