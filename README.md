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

## Where can I find YAKE!?
YAKE! is available online [http://yake.inesctec.pt], on [Google Play](https://play.google.com/store/apps/details?id=com.yake.yake), as an open source Python package [https://github.com/LIAAD/yake] and as an [API](http://yake.inesctec.pt/apidocs/#/available_methods/post_yake_v2_extract_keywords).

## Installing YAKE!

There are three installation alternatives.

- To run YAKE! in the command line (say, to integrate in a script), but you do not need an HTTP server on top, you can use our [simple YAKE! Docker image](#cli-image). This container will allow you to run text extraction as a command, and then exit.
- To run YAKE! as an HTTP server featuring a RESTful API (say to integrate in a web application or host your own YAKE!), you can use our [RESTful API server image](#rest-api-image). This container/server *will run in the background*.
- To install YAKE! straight "on the metal" or you want to integrate it in your Python app, you can [install it and its dependencies](#standalone-installation).

<a name="cli-image"></a>
### Option 1. YAKE as a CLI utility inside a Docker container

First, install Docker. Ubuntu users, please see our [script below](#installing-docker) for a complete installation script.

Then, run:

```bash
docker run liaad/yake:latest -ti "Caffeine is a central nervous system (CNS) stimulant of the methylxanthine class.[10] It is the world's most widely consumed psychoactive drug. Unlike many other psychoactive substances, it is legal and unregulated in nearly all parts of the world. There are several known mechanisms of action to explain the effects of caffeine. The most prominent is that it reversibly blocks the action of adenosine on its receptor and consequently prevents the onset of drowsiness induced by adenosine. Caffeine also stimulates certain portions of the autonomic nervous system."
```
*Example text from Wikipedia*

<a name="rest-api-image"></a>
### Option 2. REST API Server in a Docker container

This install will provide you a mirror of the original REST API of YAKE! available [here](https://boiling-castle-88317.herokuapp.com).

```bash
docker run -p 5000:5000 -d liaad/yake-server:latest
```

After it starts up, the container will run in the background, at http://127.0.0.1:5000. To access the YAKE! API documentation, go to http://127.0.0.1:5000/apidocs/.

You can test the RESTful API using `curl`:

```bash
curl -X POST "http://localhost:5000/yake/" -H "accept: application/json" -H "Content-Type: application/json" \
-d @- <<'EOF'
{
  "language": "en",
  "max_ngram_size": 3,
  "number_of_keywords": 10,
  "text": "Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague , but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists ..."
}
EOF
```
*Example text from Wikipedia*

<a name="standalone-installation"></a>
### Option 3. Standalone Installation (for development or integration)

#### Requirements

Python3

#### Installation

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
	-ti, --text_input TEXT          Input text, SURROUNDED by single quotes(')
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

text = "Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning "\
"competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud "\
"Next conference in San Francisco this week, the official announcement could come as early as tomorrow. "\
"Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. "\
"Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, "\
"was founded by Goldbloom  and Ben Hamner in 2010. "\
"The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, "\
"it has managed to stay well ahead of them by focusing on its specific niche. "\
"The service is basically the de facto home for running data science and machine learning competitions. "\
"With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, "\
"it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow "\
"and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, "\
"Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. "\
"That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google "\
"will keep the service running - likely under its current name. While the acquisition is probably more about "\
"Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition "\
"and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can "\
"share this code on the platform (the company previously called them 'scripts'). "\
"Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with "\
"that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) "\
"since its   launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, "\
"Google chief economist Hal Varian, Khosla Ventures and Yuri Milner "
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

custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
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

### Highlighting Feature
Highlighting feature will tag every keyword in the text with the default tag `<kw>`.

``` python

from yake.highlight import TextHighlighter

th = TextHighlighter(max_ngram_size = 3)
th.highlight(text, keywords)

```
#### Output
By default, keywords will be highlighted using the tag 'kw'.
``` 
Sources tell us that <kw>google</kw> is <kw>acquiring kaggle</kw>, a platform that <kw>hosts data science</kw> and <kw>machine learning</kw> competitions. Details about the transaction remain somewhat vague , but given that <kw>google</kw> is hosting its Cloud Next conference in <kw>san francisco</kw> this week, the official announcement could come as early as tomorrow.  Reached by phone, Kaggle co-founder <kw>ceo anthony goldbloom</kw> declined to deny that the acquisition is happening. <kw>google</kw> itself declined 'to comment on rumors'.
.....
.....
```


### Custom Highlighting Feature
Besides tagging a text with the default tag, users can also specify their own custom highlight. In the following text, the tag `<span class='my_class' >` makes use of an hyphotetical function `my_class` whose purpose would be to highlight in white colour or the relevant keywords.

#### Output
```python

from yake.highlight import TextHighlighter
th = TextHighlighter(max_ngram_size = 3, highlight_pre = "<span class='my_class' >", highlight_post= "</span>")
th.highlight(text, keywords)
```

```
self.highlight_postSources tell us that <span class='my_class' >google</span> is <span class='my_class' >acquiring kaggle</span>, a platform that <span class='my_class' >hosts data science</span> and <span class='my_class' >machine learning</span> self.highlight_postcompetitions. Details about the transaction remain somewhat vague , but given that <span class='my_class' >google</span> is hosting self.highlight_postits Cloud Next conference in <span class='my_class' >san francisco</span> this week, the official announcement could come as early self.highlight_postas tomorrow.  Reached by phone, Kaggle co-founder <span class='my_class' >ceo anthony goldbloom</span> declined to deny that the self.highlight_postacquisition is happening. <span class='my_class' >google</span> itself declined 'to comment on rumors'.
.....
.....
```

### Languages others than English
While English (`en`) is the default language, users can use YAKE! to extract keywords from whatever language they want to by specifying the the corresponding language universal code. The below example shows how to extract keywords from a portuguese text.
``` bash
text = '''
"Conta-me Histórias." Xutos inspiram projeto premiado. A plataforma "Conta-me Histórias" foi distinguida com o Prémio Arquivo.pt, atribuído a trabalhos inovadores de investigação ou aplicação de recursos preservados da Web, através dos serviços de pesquisa e acesso disponibilizados publicamente pelo Arquivo.pt . Nesta plataforma em desenvolvimento, o utilizador pode pesquisar sobre qualquer tema e ainda executar alguns exemplos predefinidos. Como forma de garantir a pluralidade e diversidade de fontes de informação, esta são utilizadas 24 fontes de notícias eletrónicas, incluindo a TSF. Uma versão experimental (beta) do "Conta-me Histórias" está disponível aqui.
A plataforma foi desenvolvida por Ricardo Campos investigador do LIAAD do INESC TEC e docente do Instituto Politécnico de Tomar, Arian Pasquali e Vitor Mangaravite, também investigadores do LIAAD do INESC TEC, Alípio Jorge, coordenador do LIAAD do INESC TEC e docente na Faculdade de Ciências da Universidade do Porto, e Adam Jatwot docente da Universidade de Kyoto.
'''

custom_kw_extractor = yake.KeywordExtractor(lan="pt")
keywords = custom_kw_extractor.extract_keywords(text)

for kw in keywords:
    print(kw)
```

#### Output
``` bash
('conta-me histórias', 0.006225012963810038)
('liaad do inesc', 0.01899063587015275)
('inesc tec', 0.01995432290332246)
('conta-me', 0.04513273690417472)
('histórias', 0.04513273690417472)
('prémio arquivo.pt', 0.05749361520927859)
('liaad', 0.07738867367929901)
('inesc', 0.07738867367929901)
('tec', 0.08109398065524037)
('xutos inspiram projeto', 0.08720742489353424)
('inspiram projeto premiado', 0.08720742489353424)
('adam jatwot docente', 0.09407053486771558)
('arquivo.pt', 0.10261392141666957)
('alípio jorge', 0.12190479662535166)
('ciências da universidade', 0.12368384021490342)
('ricardo campos investigador', 0.12789997272332762)
('politécnico de tomar', 0.13323587141127738)
('arian pasquali', 0.13323587141127738)
('vitor mangaravite', 0.13323587141127738)
('preservados da web', 0.13596322680882506)
```

## Related projects

### YAKE! Mobile APP
YAKE! is now available on [Google Play](https://play.google.com/store/apps/details?id=com.yake.yake)

### `pke` - python keyphrase extraction

https://github.com/boudinfl/pke - `pke` is an **open source** python-based **keyphrase extraction** toolkit. It
provides an end-to-end keyphrase extraction pipeline in which each component can
be easily modified or extended to develop new models. `pke` also allows for
easy benchmarking of state-of-the-art keyphrase extraction models, and
ships with supervised models trained on the SemEval-2010 dataset (http://aclweb.org/anthology/S10-1004).

Credits to https://github.com/boudinfl

### `SparkNLP` - State of the Art Natural Language Processing framework
https://github.com/JohnSnowLabs/spark-nlp - `SparkNLP` from [John Snow Labs](https://www.johnsnowlabs.com/) is an open source framework with full Python, Scala, and Java Support. Check [their documentation](https://nlp.johnsnowlabs.com/docs/en/annotators#yakekeywordextraction), [demo](https://demo.johnsnowlabs.com/public/KEYPHRASE_EXTRACTION/) and [google colab](https://colab.research.google.com/github/JohnSnowLabs/spark-nlp-workshop/blob/master/tutorials/streamlit_notebooks/KEYPHRASE_EXTRACTION.ipynb). A video on how to use spark nlp with yake can also be found here: https://events.johnsnowlabs.com/john-snow-labs-nlu-become-a-data-science-superhero-with-one-line-of-python-code

### General Index by Archive.org
https://archive.org/details/GeneralIndex - A catalogue of 19 billions of YAKE keywords extracted from 107 million papers that can be found on [Archive.org](https://archive.org/details/GeneralIndex). An article about the General Index project can also be found in [Nature](https://www.nature.com/articles/d41586-021-02895-8).

### `textacy` - NLP, before and after spaCy

https://github.com/chartbeat-labs/textacy - `textacy` is a Python library for performing a variety of natural language processing (NLP) tasks, built on the high-performance spaCy library. among other features it supports keyword extration using YAKE.

Credits to https://github.com/chartbeat-labs

<a name="installing-docker"></a>

### `Annif` - Tool for automated subject indexing and classification
https://github.com/NatLibFi/Annif/ - `Annif` is a multi-algorithm automated subject indexing tool for libraries, archives and museums. This repository is used for developing a production version of the system, based on ideas from the initial prototype. Official website http://annif.org/.

### `Portulan Clarin` - Services and data for researchers, innovators, students and language professionals
https://portulanclarin.net/workbench/liaad-yake/ - `Portulan Clarin` is a Research Infrastructure for the Science and Technology of Language, belonging to the Portuguese National Roadmap of  Research Infrastructures of Strategic Relevance, and part of the international research infrastructure CLARIN ERIC. It includes a demo of YAKE! among many other language technologies. Official website https://portulanclarin.net/.

## How to install Docker

Here is the "just copy and paste" installations script for Docker in Ubuntu. Enjoy.

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# Add Docker repo
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update

# Install Docker
sudo apt-get install -y docker-ce

# Start Docker Daemon
sudo service docker start

# Add yourself to the Docker user group, otherwise docker will complain that
# it does not know if the Docker Daemon is running
sudo usermod -aG docker ${USER}

# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
source ~/.bashrc
docker-compose --version
echo "Done!"
```

Credits to https://github.com/silvae86 for the Docker scripts.

## References
Please cite the following works when using YAKE

<b>In-depth journal paper at Information Sciences Journal</b>

Campos, R., Mangaravite, V., Pasquali, A., Jatowt, A., Jorge, A., Nunes, C. and Jatowt, A. (2020). YAKE! Keyword Extraction from Single Documents using Multiple Local Features. In Information Sciences Journal. Elsevier, Vol 509, pp 257-289. [pdf](https://doi.org/10.1016/j.ins.2019.09.013)

<b>ECIR'18 Best Short Paper</b>

Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). A Text Feature Based Automatic Keyword Extraction Method for Single Documents. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 684 - 691. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_63)

Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). YAKE! Collection-independent Automatic Keyword Extractor. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 806 - 810. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_80)

## Awards
[ECIR'18](http://ecir2018.org) Best Short Paper
