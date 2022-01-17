---
layout: default
title: Home
nav_order: 1
description: "Unsupervised Approach for Automatic Keyword Extraction using Text Features."
permalink: /
---

# Yet Another Keyword Extractor (Yake)
{: .fs-9 }

Unsupervised Approach for Automatic Keyword Extraction using Text Features.
{: .fs-6 .fw-300 }

[Get started](docs/getting_started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } 
[View demo](http://yake.inesctec.pt){: .btn .fs-5 .mb-4 .mb-md-0 }
[Github](https://github.com/LIAAD/yake){: .btn .fs-5 .mb-4 .mb-md-0 }

---

YAKE! is a light-weight unsupervised automatic keyword extraction method which rests on text statistical features extracted from single documents to select the most important keywords of a text. Our system does not need to be trained on a particular set of documents, neither it depends on dictionaries, external-corpus, size of the text, language or domain. To demonstrate the merits and the significance of our proposal, we compare it against ten state-of-the-art unsupervised approaches (TF.IDF, KP-Miner, RAKE, TextRank, SingleRank, ExpandRank, TopicRank, TopicalPageRank, PositionRank and MultipartiteRank), and one supervised method (KEA). Experimental results carried out on top of twenty datasets (see Benchmark section below) show that our methods significantly outperform state-of-the-art methods under a number of collections of different sizes, languages or domains. 

An interactive demo is also available [here](http://yake.inesctec.pt).

## Main Features

* Unsupervised approach
* Corpus-Independent
* Domain and Language Independent
* Single-Document


## References

If you use "YAKE" in a work that leads to a scientific publication, we would appreciate it if you would kindly cite
it in your manuscript.

- Campos, R., Mangaravite, V., Pasquali, A., Jatowt, A., Jorge, A., Nunes, C. and Jatowt, A. (2020). YAKE! Keyword Extraction from Single Documents using Multiple Local Features. In Information Sciences Journal. Elsevier, Vol 509, pp 257-289. [pdf](https://doi.org/10.1016/j.ins.2019.09.013)

- Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). A Text Feature Based Automatic Keyword Extraction Method for Single Documents. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 684 - 691. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_63) (ECIR'18 Best Short Paper)

- Campos R., Mangaravite V., Pasquali A., Jorge A.M., Nunes C., and Jatowt A. (2018). YAKE! Collection-independent Automatic Keyword Extractor. In: Pasi G., Piwowarski B., Azzopardi L., Hanbury A. (eds). Advances in Information Retrieval. ECIR 2018 (Grenoble, France. March 26 – 29). Lecture Notes in Computer Science, vol 10772, pp. 806 - 810. [pdf](https://link.springer.com/chapter/10.1007/978-3-319-76941-7_80)


## Credits

This software is authored by the following INESC TEC researchers:
- Ricardo Campos
- Vítor Mangaravite
- Arian Pasquali
- Alípio Jorge
- Célia Nunes
- Adam Jatowt

### License
Copyright (C) 2018, INESC TEC [license](https://github.com/LIAAD/yake/blob/master/LICENSE).


### Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. Read more about becoming a contributor in [our GitHub repo](https://github.com/LIAAD/yake/blob/master/CONTRIBUTING.rst).

#### Thank you to the contributors of YAKE!

<ul class="list-style-none">
{% for contributor in site.github.contributors %}
  <li class="d-inline-block mr-1">
     <a href="{{ contributor.html_url }}"><img src="{{ contributor.avatar_url }}" width="32" height="32" alt="{{ contributor.login }}"/></a>
  </li>
{% endfor %}
</ul>
