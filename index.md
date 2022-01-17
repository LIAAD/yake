---
layout: default
title: Home
nav_order: 1
description: "Unsupervised Approach for Automatic Keyword Extraction using Text Features."
permalink: /
---

# Yet Another Keyword Extractor (YAKE)
{: .fs-9 }

Unsupervised Approach for Automatic Keyword Extraction using Text Features.
{: .fs-6 .fw-300 }

[Get started now](docs/getting_started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } 
[View demo](https://share.streamlit.io/arianpasquali/yake/demo){: .btn .fs-5 .mb-4 .mb-md-0 }
[GitHub](https://github.com/LIAAD/yake){: .btn .fs-5 .mb-4 .mb-md-0 }


---

YAKE! is a light-weight unsupervised automatic keyword extraction method which rests on text statistical features extracted from single documents to select the most important keywords of a text. Our system does not need to be trained on a particular set of documents, neither it depends on dictionaries, external-corpus, size of the text, language or domain. 

Interactive demo is available [here](http://yake.inesctec.pt).

## Background

Extracting keywords from texts has become a challenge for individuals and organizations as the information grows in complexity and size. The need to automate this task so that texts can be processed in a timely and adequate manner has led to the emergence of automatic keyword extraction tools. Despite the advances, there is a clear lack of multilingual online tools to automatically extract keywords from single documents. Yake! is a novel feature-based system for multi-lingual keyword extraction, which supports texts of different sizes, domain or languages. Unlike other approaches, Yake! does not rely on dictionaries nor thesauri, neither is trained against any corpora. Instead, it follows an unsupervised approach which builds upon features extracted from the text, making it thus applicable to documents written in different languages without the need for further knowledge. This can be beneficial for a large number of tasks and a plethora of situations where the access to training corpora is either limited or restricted.

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


## License
Copyright (C) 2018, INESC TEC [license](https://github.com/LIAAD/yake/blob/master/LICENSE).


## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. Read more about becoming a contributor in [our GitHub repo](https://github.com/LIAAD/yake/blob/master/CONTRIBUTING.rst).

### Thank you to the contributors of YAKE!

<ul class="list-style-none">
{% for contributor in site.github.contributors %}
  <li class="d-inline-block mr-1">
     <a href="{{ contributor.html_url }}"><img src="{{ contributor.avatar_url }}" width="32" height="32" alt="{{ contributor.login }}"/></a>
  </li>
{% endfor %}
</ul>


If you are feeling nostalgic you can access the old site [here](http://yake.inesctec.pt/).