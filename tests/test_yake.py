#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for yake package."""


from click.testing import CliRunner

import yake
from yake.core.highlight import TextHighlighter


def test_phraseless_example():
    text_content = "- not yet"

    pyake = yake.KeywordExtractor()

    result = pyake.extract_keywords(text_content)
    assert len(result) == 0


def test_null_and_blank_example():
    pyake = yake.KeywordExtractor()

    result = pyake.extract_keywords("")
    assert len(result) == 0

    result = pyake.extract_keywords(None)
    assert len(result) == 0


def test_n3_EN():
    text_content = """
    Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning   competitions. Details about the transaction remain somewhat vague , but given that Google is hosting   its Cloud Next conference in San Francisco this week, the official announcement could come as early   as tomorrow.  Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the   acquisition is happening. Google itself declined 'to comment on rumors'.   Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom   and Ben Hamner in 2010. The service got an early start and even though it has a few competitors   like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its   specific niche. The service is basically the de facto home for running data science  and machine learning   competitions.  With Kaggle, Google is buying one of the largest and most active communities for   data scientists - and with that, it will get increased mindshare in this community, too   (though it already has plenty of that thanks to Tensorflow and other projects).   Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month,   Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying   YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too.   Our understanding is that Google will keep the service running - likely under its current name.   While the acquisition is probably more about Kaggle's community than technology, Kaggle did build   some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are   basically the source code for analyzing data sets and developers can share this code on the   platform (the company previously called them 'scripts').  Like similar competition-centric sites,   Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service.   According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its   launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant,   Google chief economist Hal Varian, Khosla Ventures and Yuri Milner"""

    pyake = yake.KeywordExtractor(lan="en", n=3)

    result = pyake.extract_keywords(text_content)
    print(result)
    res = [
        ("Google", 0.02509259635302287),
        ("Kaggle", 0.027297150442917317),
        ("CEO Anthony Goldbloom", 0.04834891465259988),
        ("data science", 0.05499112888517541),
        ("acquiring data science", 0.06029572445726576),
        ("Google Cloud Platform", 0.07461585862381104),
        ("data", 0.07999958986489127),
        ("San Francisco", 0.0913829662674319),
        ("Anthony Goldbloom declined", 0.09740885820462175),
        ("science", 0.09834167930168546),
        ("science community Kaggle", 0.1014394718805728),
        ("machine learning", 0.10754988562466912),
        ("Google Cloud", 0.1136787749431024),
        ("Google is acquiring", 0.114683257931042),
        ("acquiring Kaggle", 0.12012386507741751),
        ("Anthony Goldbloom", 0.1213027418574554),
        ("platform", 0.12404419723925647),
        ("co-founder CEO Anthony", 0.12411964553586782),
        ("CEO Anthony", 0.12462950727635251),
        ("service", 0.1316357590449064),
    ]
    assert result == res

    keywords = [kw[0] for kw in result]
    th = TextHighlighter(max_ngram_size=3)
    textHighlighted = th.highlight(text_content, keywords)
    print(textHighlighted)
    assert (
        textHighlighted
        == "<kw>Google</kw> is acquiring <kw>data science</kw> community <kw>Kaggle</kw>. Sources tell us that <kw>Google</kw> is acquiring <kw>Kaggle</kw>, a <kw>platform</kw> that hosts <kw>data science</kw> and <kw>machine learning</kw>   competitions. Details about the transaction remain somewhat vague , but given that <kw>Google</kw> is hosting   its Cloud Next conference in <kw>San Francisco</kw> this week, the official announcement could come as early   as tomorrow.  Reached by phone, <kw>Kaggle</kw> co-founder <kw>CEO Anthony Goldbloom</kw> declined to deny that the   acquisition is happening. <kw>Google</kw> itself declined 'to comment on rumors'.   <kw>Kaggle</kw>, which has about half a million <kw>data</kw> scientists on its <kw>platform</kw>, was founded by Goldbloom   and Ben Hamner in 2010. The <kw>service</kw> got an early start and even though it has a few competitors   like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its   specific niche. The <kw>service</kw> is basically the de facto home for running <kw>data science</kw>  and <kw>machine learning</kw>   competitions.  With <kw>Kaggle</kw>, <kw>Google</kw> is buying one of the largest and most active communities for   <kw>data</kw> scientists - and with that, it will get increased mindshare in this community, too   (though it already has plenty of that thanks to Tensorflow and other projects).   <kw>Kaggle</kw> has a bit of a history with <kw>Google</kw>, too, but that's pretty recent. Earlier this month,   <kw>Google</kw> and <kw>Kaggle</kw> teamed up to host a $100,000 <kw>machine learning</kw> competition around classifying   YouTube videos. That competition had some deep integrations with the <kw>Google</kw> Cloud <kw>Platform</kw>, too.   Our understanding is that <kw>Google</kw> will keep the <kw>service</kw> running - likely under its current name.   While the acquisition is probably more about Kaggle's community than technology, <kw>Kaggle</kw> did build   some interesting tools for hosting its competition and 'kernels', too. On <kw>Kaggle</kw>, kernels are   basically the source code for analyzing <kw>data</kw> sets and developers can share this code on the   <kw>platform</kw> (the company previously called them 'scripts').  Like similar competition-centric sites,   <kw>Kaggle</kw> also runs a job board, too. It's unclear what <kw>Google</kw> will do with that part of the <kw>service</kw>.   According to Crunchbase, <kw>Kaggle</kw> raised $12.5 million (though PitchBook says it's $12.75) since its   launch in 2010. Investors in <kw>Kaggle</kw> include Index Ventures, SV Angel, Max Levchin, Naval Ravikant,   <kw>Google</kw> chief economist Hal Varian, Khosla Ventures and Yuri Milner"
    )

def test_n4_EN():
    text_content = "Given a sound clip of a person or people speaking, determine the textual representation of the speech. This is the opposite of text to speech and is one of the extremely difficult problems colloquially termed AI-complete. In natural speech there are hardly any pauses between successive words, and thus speech segmentation is a necessary subtask of speech recognition. In most spoken languages, the sounds representing successive letters blend into each other in a process termed coarticulation, so the conversion of the analog signal to discrete characters can be a very difficult process. Also, given that words in the same language are spoken by people with different accents, the speech recognition software must be able to recognize the wide variety of input as being identical to each other in terms of its textual equivalent."
    
    pyake = yake.KeywordExtractor(lan="en", n=4)
    result = pyake.extract_keywords(text_content)

    res = [
        ('person or people speaking', 0.02371235675412416),
        ('determine the textual representation', 0.023712356754124163),
        ('clip of a person', 0.029892130838734352),
        ('speech', 0.05171467792955825),
        ('problems colloquially termed AI-complete', 0.05774635365736056),
        ('people speaking', 0.06491457949781286),
        ('difficult problems colloquially termed', 0.06622675127498744),
        ('extremely difficult problems colloquially', 0.06668784569227526),
        ('sound clip', 0.0687424852965288),
        ('textual representation', 0.07592882807384618),
        ('speech recognition', 0.07650182723598535),
        ('colloquially termed AI-complete', 0.10009206386398749),
        ('extremely difficult problems', 0.11478755562776954),
        ('difficult problems colloquially', 0.11478755562776954),
        ('problems colloquially termed', 0.11478755562776954),
        ('determine the textual', 0.13265911255112645),
        ('speech recognition software', 0.13385106547208153),
        ('speaking', 0.14715902096033903),
        ('determine', 0.14715902096033903),
        ('person or people', 0.15420935992103177),
    ]

    assert result == res

    keywords = [kw[0] for kw in result]
    th = TextHighlighter(max_ngram_size=4)
    textHighlighted = th.highlight(text_content, keywords)
    print(textHighlighted)
    assert (
            textHighlighted
            == "Given a sound clip of a <kw>person or people speaking</kw>, <kw>determine the textual representation</kw> of the <kw>speech</kw>. This is the opposite of text to <kw>speech</kw> and is one of the extremely difficult <kw>problems colloquially termed AI-complete</kw>. In natural <kw>speech</kw> there are hardly any pauses between successive words, and thus <kw>speech</kw> segmentation is a necessary subtask of <kw>speech</kw> recognition. In most spoken languages, the sounds representing successive letters blend into each other in a process termed coarticulation, so the conversion of the analog signal to discrete characters can be a very difficult process. Also, given that words in the same language are spoken by people with different accents, the <kw>speech</kw> recognition software must be able to recognize the wide variety of input as being identical to each other in terms of its textual equivalent."
    )

def test_n3_PT():
    text_content = """
    "Conta-me Histórias." Xutos inspiram projeto premiado. A plataforma "Conta-me Histórias" foi distinguida com o Prémio Arquivo.pt, atribuído a trabalhos inovadores de investigação ou aplicação de recursos preservados da Web, através dos serviços de pesquisa e acesso disponibilizados publicamente pelo Arquivo.pt . Nesta plataforma em desenvolvimento, o utilizador pode pesquisar sobre qualquer tema e ainda executar alguns exemplos predefinidos. Como forma de garantir a pluralidade e diversidade de fontes de informação, esta são utilizadas 24 fontes de notícias eletrónicas, incluindo a TSF. Uma versão experimental (beta) do "Conta-me Histórias" está disponível aqui.
    A plataforma foi desenvolvida por Ricardo Campos investigador do LIAAD do INESC TEC e docente do Instituto Politécnico de Tomar, Arian Pasquali e Vitor Mangaravite, também investigadores do LIAAD do INESC TEC, Alípio Jorge, coordenador do LIAAD do INESC TEC e docente na Faculdade de Ciências da Universidade do Porto, e Adam Jatwot docente da Universidade de Kyoto.
    """

    pyake = yake.KeywordExtractor(lan="pt", n=3)
    result = pyake.extract_keywords(text_content)
    res = [
        ("Conta-me Histórias", 0.006225012963810038),
        ("LIAAD do INESC", 0.01899063587015275),
        ("INESC TEC", 0.01995432290332246),
        ("Conta-me", 0.04513273690417472),
        ("Histórias", 0.04513273690417472),
        ("Prémio Arquivo.pt", 0.05749361520927859),
        ("LIAAD", 0.07738867367929901),
        ("INESC", 0.07738867367929901),
        ("TEC", 0.08109398065524037),
        ("Xutos inspiram projeto", 0.08720742489353424),
        ("inspiram projeto premiado", 0.08720742489353424),
        ("Adam Jatwot docente", 0.09407053486771558),
        ("Arquivo.pt", 0.10261392141666957),
        ("Alípio Jorge", 0.12190479662535166),
        ("Ciências da Universidade", 0.12368384021490342),
        ("Ricardo Campos investigador", 0.12789997272332762),
        ("Politécnico de Tomar", 0.13323587141127738),
        ("Arian Pasquali", 0.13323587141127738),
        ("Vitor Mangaravite", 0.13323587141127738),
        ("preservados da Web", 0.13596322680882506),
    ]
    assert result == res

    keywords = [kw[0] for kw in result]
    th = TextHighlighter(max_ngram_size=3)
    textHighlighted = th.highlight(text_content, keywords)
    print(textHighlighted)

    assert (
        textHighlighted
        == '"<kw>Conta-me Histórias</kw>." <kw>Xutos inspiram projeto</kw> premiado. A plataforma "<kw>Conta-me Histórias</kw>" foi distinguida com o <kw>Prémio Arquivo.pt</kw>, atribuído a trabalhos inovadores de investigação ou aplicação de recursos <kw>preservados da Web</kw>, através dos serviços de pesquisa e acesso disponibilizados publicamente pelo <kw>Arquivo.pt</kw> . Nesta plataforma em desenvolvimento, o utilizador pode pesquisar sobre qualquer tema e ainda executar alguns exemplos predefinidos. Como forma de garantir a pluralidade e diversidade de fontes de informação, esta são utilizadas 24 fontes de notícias eletrónicas, incluindo a TSF. Uma versão experimental (beta) do "<kw>Conta-me Histórias</kw>" está disponível aqui.     A plataforma foi desenvolvida por <kw>Ricardo Campos investigador</kw> do <kw>LIAAD do INESC</kw> <kw>TEC</kw> e docente do Instituto <kw>Politécnico de Tomar</kw>, <kw>Arian Pasquali</kw> e <kw>Vitor Mangaravite</kw>, também investigadores do <kw>LIAAD do INESC</kw> <kw>TEC</kw>, <kw>Alípio Jorge</kw>, coordenador do <kw>LIAAD do INESC</kw> <kw>TEC</kw> e docente na Faculdade de <kw>Ciências da Universidade</kw> do Porto, e <kw>Adam Jatwot docente</kw> da Universidade de Kyoto.'
    )


def test_n1_EN():
    text_content = """
    Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week, the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. Google itself declined 'to comment on rumors'. Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom and Ben Hamner in 2010. The service got an early start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The service is basically the de facto home for running data science  and machine learning competitions. With Kaggle, Google is buying one of the largest and most active communities for data scientists - and with that, it will get increased mindshare in this community, too (though it already has plenty of that thanks to Tensorflow and other projects). Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month, Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too. Our understanding is that Google will keep the service running - likely under its current name. While the acquisition is probably more about Kaggle's community than technology, Kaggle did build some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are basically the source code for analyzing data sets and developers can share this code on the platform (the company previously called them 'scripts'). Like similar competition-centric sites, Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service. According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant, Google chief economist Hal Varian, Khosla Ventures and Yuri Milner"""

    pyake = yake.KeywordExtractor(lan="en", n=1)
    result = pyake.extract_keywords(text_content)
    print(result)
    res = [
        ("Google", 0.02509259635302287),
        ("Kaggle", 0.027297150442917317),
        ("data", 0.07999958986489127),
        ("science", 0.09834167930168546),
        ("platform", 0.12404419723925647),
        ("service", 0.1316357590449064),
        ("acquiring", 0.15110282570329972),
        ("learning", 0.1620911439042445),
        ("Goldbloom", 0.1624845364505264),
        ("machine", 0.16721860165903407),
        ("competition", 0.1826862004451857),
        ("Cloud", 0.1849060668345104),
        ("community", 0.202661778267609),
        ("Ventures", 0.2258881919825325),
        ("declined", 0.2872980816826787),
        ("San", 0.2893636939471809),
        ("Francisco", 0.2893636939471809),
        ("early", 0.2946076840223411),
        ("acquisition", 0.2991070691689808),
        ("scientists", 0.3046548516998034),
    ]
    assert result == res

    keywords = [kw[0] for kw in result]
    th = TextHighlighter(max_ngram_size=1)
    textHighlighted = th.highlight(text_content, keywords)
    print(textHighlighted)

    assert (
        textHighlighted
        == "<kw>Google</kw> is <kw>acquiring</kw> <kw>data</kw> <kw>science</kw> <kw>community</kw> <kw>Kaggle</kw>. Sources tell us that <kw>Google</kw> is <kw>acquiring</kw> <kw>Kaggle</kw>, a <kw>platform</kw> that hosts <kw>data</kw> <kw>science</kw> and <kw>machine</kw> <kw>learning</kw> competitions. Details about the transaction remain somewhat vague, but given that <kw>Google</kw> is hosting its <kw>Cloud</kw> Next conference in <kw>San</kw> <kw>Francisco</kw> this week, the official announcement could come as <kw>early</kw> as tomorrow. Reached by phone, <kw>Kaggle</kw> co-founder CEO Anthony <kw>Goldbloom</kw> <kw>declined</kw> to deny that the <kw>acquisition</kw> is happening. <kw>Google</kw> itself <kw>declined</kw> 'to comment on rumors'. <kw>Kaggle</kw>, which has about half a million <kw>data</kw> <kw>scientists</kw> on its <kw>platform</kw>, was founded by <kw>Goldbloom</kw> and Ben Hamner in 2010. The <kw>service</kw> got an <kw>early</kw> start and even though it has a few competitors like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its specific niche. The <kw>service</kw> is basically the de facto home for running <kw>data</kw> <kw>science</kw>  and <kw>machine</kw> <kw>learning</kw> competitions. With <kw>Kaggle</kw>, <kw>Google</kw> is buying one of the largest and most active communities for <kw>data</kw> <kw>scientists</kw> - and with that, it will get increased mindshare in this <kw>community</kw>, too (though it already has plenty of that thanks to Tensorflow and other projects). <kw>Kaggle</kw> has a bit of a history with <kw>Google</kw>, too, but that's pretty recent. Earlier this month, <kw>Google</kw> and <kw>Kaggle</kw> teamed up to host a $100,000 <kw>machine</kw> <kw>learning</kw> <kw>competition</kw> around classifying YouTube videos. That <kw>competition</kw> had some deep integrations with the <kw>Google</kw> <kw>Cloud</kw> <kw>Platform</kw>, too. Our understanding is that <kw>Google</kw> will keep the <kw>service</kw> running - likely under its current name. While the <kw>acquisition</kw> is probably more about Kaggle's <kw>community</kw> than technology, <kw>Kaggle</kw> did build some interesting tools for hosting its <kw>competition</kw> and 'kernels', too. On <kw>Kaggle</kw>, kernels are basically the source code for analyzing <kw>data</kw> sets and developers can share this code on the <kw>platform</kw> (the company previously called them 'scripts'). Like similar competition-centric sites, <kw>Kaggle</kw> also runs a job board, too. It's unclear what <kw>Google</kw> will do with that part of the <kw>service</kw>. According to Crunchbase, <kw>Kaggle</kw> raised $12.5 million (though PitchBook says it's $12.75) since its launch in 2010. Investors in <kw>Kaggle</kw> include Index <kw>Ventures</kw>, SV Angel, Max Levchin, Naval Ravikant, <kw>Google</kw> chief economist Hal Varian, Khosla <kw>Ventures</kw> and Yuri Milner"
    )


def test_n1_EL():
    text_content = """
    Ανώτατος διοικητής του ρωσικού στρατού φέρεται να σκοτώθηκε κοντά στο Χάρκοβο, σύμφωνα με την υπηρεσία πληροφοριών του υπουργείου Άμυνας της Ουκρανίας. Σύμφωνα με δήλωση του υπουργείου Άμυνας της Ουκρανίας, πρόκειται για τον Vitaly Gerasimov, υποστράτηγο και υποδιοικητή από την Κεντρική Στρατιωτική Περιφέρεια της Ρωσίας."""

    pyake = yake.KeywordExtractor(lan="el", n=1)
    result = pyake.extract_keywords(text_content)
    print(result)
    res = [
        ("Ουκρανίας", 0.04685829498124156),
        ("Χάρκοβο", 0.0630891548728466),
        ("Άμυνας", 0.06395408991254226),
        ("σύμφωνα", 0.07419311338418161),
        ("υπουργείου", 0.1069960715371627),
        ("Ανώτατος", 0.12696931063105557),
        ("διοικητής", 0.18516501832552387),
        ("ρωσικού", 0.18516501832552387),
        ("στρατού", 0.18516501832552387),
        ("φέρεται", 0.18516501832552387),
        ("σκοτώθηκε", 0.18516501832552387),
        ("κοντά", 0.18516501832552387),
        ("υπηρεσία", 0.18516501832552387),
        ("πληροφοριών", 0.18516501832552387),
        ("Gerasimov", 0.1895400421770795),
        ("Ρωσίας", 0.1895400421770795),
        ("Vitaly", 0.24366598777562623),
        ("Κεντρική", 0.24366598777562623),
        ("Στρατιωτική", 0.24366598777562623),
        ("Περιφέρεια", 0.24366598777562623),
    ]
    assert result == res

    keywords = [kw[0] for kw in result]
    th = TextHighlighter(max_ngram_size=1)
    textHighlighted = th.highlight(text_content, keywords)
    print(textHighlighted)

    assert (
        textHighlighted
        == "<kw>Ανώτατος</kw> <kw>διοικητής</kw> του <kw>ρωσικού</kw> <kw>στρατού</kw> <kw>φέρεται</kw> να <kw>σκοτώθηκε</kw> <kw>κοντά</kw> στο <kw>Χάρκοβο</kw>, <kw>σύμφωνα</kw> με την <kw>υπηρεσία</kw> <kw>πληροφοριών</kw> του <kw>υπουργείου</kw> <kw>Άμυνας</kw> της <kw>Ουκρανίας</kw>. <kw>Σύμφωνα</kw> με δήλωση του <kw>υπουργείου</kw> <kw>Άμυνας</kw> της <kw>Ουκρανίας</kw>, πρόκειται για τον <kw>Vitaly</kw> <kw>Gerasimov</kw>, υποστράτηγο και υποδιοικητή από την <kw>Κεντρική</kw> <kw>Στρατιωτική</kw> <kw>Περιφέρεια</kw> της <kw>Ρωσίας</kw>."
    )


test_phraseless_example()
test_null_and_blank_example()
test_n1_EN()
test_n3_EN()
test_n3_PT()
test_n1_EL()
