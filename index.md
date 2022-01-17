# Yet Another Keyword Extractor (Yake)

Unsupervised Approach for Automatic Keyword Extraction using Text Features.

[Get started](http://www.google.com){: .btn}
[Demo](http://yake.inesctec.pt){: .btn}
[Github](https://github.com/LIAAD/yake){: .btn}

YAKE! is a light-weight unsupervised automatic keyword extraction method which rests on text statistical features extracted from single documents to select the most important keywords of a text. Our system does not need to be trained on a particular set of documents, neither it depends on dictionaries, external-corpus, size of the text, language or domain. To demonstrate the merits and the significance of our proposal, we compare it against ten state-of-the-art unsupervised approaches (TF.IDF, KP-Miner, RAKE, TextRank, SingleRank, ExpandRank, TopicRank, TopicalPageRank, PositionRank and MultipartiteRank), and one supervised method (KEA). Experimental results carried out on top of twenty datasets (see Benchmark section below) show that our methods significantly outperform state-of-the-art methods under a number of collections of different sizes, languages or domains. 

An interactive demo is also available [here](http://yake.inesctec.pt).

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

If you use "YAKE" in a work that leads to a scientific publication, we would appreciate it if you would kindly cite
it in your manuscript.

- Campos, R., Mangaravite, V., Pasquali, A., Jatowt, A., Jorge, A., Nunes, C. and Jatowt, A. (2020). YAKE! Keyword Extraction from Single Documents using Multiple Local Features. In Information Sciences Journal. Elsevier, Vol 509, pp 257-289. [pdf](https://doi.org/10.1016/j.ins.2019.09.013)

- Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). A Text Feature Based Automatic Keyword Extraction Method for Single Documents. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 684 - 691. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_63) (ECIR'18 Best Short Paper)

- Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). YAKE! Collection-independent Automatic Keyword Extractor. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 806 - 810. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_80)


## Used by

List of relevant projects using YAKE:

- [SparkNLP](https://github.com/JohnSnowLabs/spark-nlp) by [John Snow Labs](https://www.johnsnowlabs.com/). 
Open source framework with full Python, Scala, and Java Support. Check [their documentation](https://nlp.johnsnowlabs.com/docs/en/annotators#yakekeywordextraction), [demo](https://demo.johnsnowlabs.com/public/KEYPHRASE_EXTRACTION/) and [google colab](https://colab.research.google.com/github/JohnSnowLabs/spark-nlp-workshop/blob/master/tutorials/streamlit_notebooks/KEYPHRASE_EXTRACTION.ipynb). A video on how to use spark nlp with yake can also be found [here](https://events.johnsnowlabs.com/john-snow-labs-nlu-become-a-data-science-superhero-with-one-line-of-python-code): 

- [pke](https://github.com/boudinfl/pke) - Python Keyphrase Extraction module.
IT is Is an open source python-based keyphrase extraction toolkit. It provides an end-to-end keyphrase extraction pipeline in which each component can be easily modified or extended to develop new models. Credits to Florian Boudin.
 
- [Textacy](https://github.com/chartbeat-labs/textacy) - NLP, before and after spaCy.
Python library for performing a variety of natural language processing (NLP) tasks, built on the high-performance spaCy library. among other features it supports keyword extration using YAKE.

- [General Index](https://archive.org/details/GeneralIndex) by Archive.org. 
A catalogue of 19 billions of YAKE keywords extracted from 107 million papers. An article about the General Index project can also be found in [Nature](https://www.nature.com/articles/d41586-021-02895-8).

- [Annif](https://github.com/NatLibFi/Annif) - Tool for automated subject indexing and classification
Multi-algorithm automated subject indexing tool for libraries, archives and museums. This repository is used for developing a production version of the system, based on ideas from the initial prototype. Official [website](http://annif.org/).

- [Portulan Clarin](https://portulanclarin.net/workbench/liaad-yake/) - Services and data for researchers, innovators, students and language professionals
Research Infrastructure for the Science and Technology of Language, belonging to the Portuguese National Roadmap of  Research Infrastructures of Strategic Relevance, and part of the international research infrastructure CLARIN ERIC. It includes a demo of YAKE! among many other language technologies. Official [website](https://portulanclarin.net/).

- [Tell me stories](https://contamehistorias.pt/arquivopt)
Tell me stories is a research project that allows users to automatically build news narratives based on news preserved by the [Portuguese Web Archive](https://arquivo.pt). 

## Credits

This software is authored by the following INESC TEC researchers:
- Ricardo Campos
- Vítor Mangaravite
- Arian Pasquali
- Alípio Jorge
- Célia Nunes
- Adam Jatowt

## License Agreement

Copyright (C) 2018, INESC TEC

YAKE! Collection-independent Automatic Keyword Extractor: a novel feature-based system for multi-lingual keyword extraction, which supports texts of different sizes, domain or languages. Unlike most of the systems, YAKE! does not rely on dictionaries nor thesauri, neither is trained against any corpora. Instead, we follow an unsupervised approach which builds upon features extracted from the text, making it thus applicable to documents written in different languages without the need for further knowledge. This can be beneficial for a large number of tasks and a plethora of situations where the access to training corpora is either limited or restricted.

This software is authored by the following INESC TEC researchers:
Ricardo Campos,
Vítor Mangaravite,
Arian Pasquali,
Alípio Jorge,
Célia Nunes, and 
Adam Jatowt

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

A commercial license is also available for use in industrial projects and collaborations that do not wish to use the GPL 3 license.

You can reach INESC TEC at info@inesctec.pt, or
Campus da Faculdade de Engenharia da Universidade do Porto
Rua Dr. Roberto Frias
4200-465 Porto
Portugal

----
You can find the full license agreement available [here](https://github.com/LIAAD/yake/blob/master/LICENSE).
