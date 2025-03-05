import streamlit as st
import yake
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from spacy import displacy
import re

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
HTML_WRAPPER = """<div style="overflow-x: hidden; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""


st.sidebar.title("Yet Another Keyword Extractor (YAKE)")
st.sidebar.markdown("""
Unsupervised Approach for Automatic Keyword Extraction using Text Features.
https://liaad.github.io/yake/
"""
)

st.sidebar.markdown("""
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LIAAD/yake/blob/gh-pages/notebooks/YAKE_tutorial.ipynb)
""")

st.sidebar.header('Parameters')

#side bar parameters
max_ngram_size = st.sidebar.slider("Select max ngram size", 1, 10, 3)
deduplication_thresold = st.sidebar.slider("Select deduplication threshold", 0.5, 1.0, 0.9)
numOfKeywords = st.sidebar.slider("Select number of keywords to return", 1, 50, 10)
deduplication_algo = st.sidebar.selectbox('deduplication function', ('leve','jaro','seqm'),2)



input_text_demo = [
    "Extracting keywords from texts has become a challenge for individuals and organizations  as the information grows in complexity and size . The need to automate this task so that text can be processed in a timely and adequate manner has led to the emergence of automatic keyword extraction tools . Yake is a novel  feature-based system for multi-lingual keyword extraction , which supports texts of different sizes, domain or languages. Unlike other approaches, Yake does not rely on dictionaries nor thesauri, neither is trained against any corpora. Instead, it follows an unsupervised approach which builds upon features extracted from the text, making it thus applicable to documents written in different languages without the need for further knowledge. This can be beneficial for a large number of tasks and a plethora of situations where access to training corpora is either limited or restricted.",
    "Google is acquiring data science community Kaggle. Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning   competitions. Details about the transaction remain somewhat vague , but given that Google is hosting   its Cloud Next conference in San Francisco this week, the official announcement could come as early   as tomorrow.  Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the   acquisition is happening. Google itself declined 'to comment on rumors'.   Kaggle, which has about half a million data scientists on its platform, was founded by Goldbloom   and Ben Hamner in 2010. The service got an early start and even though it has a few competitors   like DrivenData, TopCoder and HackerRank, it has managed to stay well ahead of them by focusing on its   specific niche. The service is basically the de facto home for running data science  and machine learning   competitions.  With Kaggle, Google is buying one of the largest and most active communities for   data scientists - and with that, it will get increased mindshare in this community, too   (though it already has plenty of that thanks to Tensorflow and other projects).   Kaggle has a bit of a history with Google, too, but that's pretty recent. Earlier this month,   Google and Kaggle teamed up to host a $100,000 machine learning competition around classifying   YouTube videos. That competition had some deep integrations with the Google Cloud Platform, too.   Our understanding is that Google will keep the service running - likely under its current name.   While the acquisition is probably more about Kaggle's community than technology, Kaggle did build   some interesting tools for hosting its competition and 'kernels', too. On Kaggle, kernels are   basically the source code for analyzing data sets and developers can share this code on the   platform (the company previously called them 'scripts').  Like similar competition-centric sites,   Kaggle also runs a job board, too. It's unclear what Google will do with that part of the service.   According to Crunchbase, Kaggle raised $12.5 million (though PitchBook says it's $12.75) since its   launch in 2010. Investors in Kaggle include Index Ventures, SV Angel, Max Levchin, Naval Ravikant,   Google chief economist Hal Varian, Khosla Ventures and Yuri Milner",
    "Genius quietly laid off a bunch of its engineers — now can it survive as a media company?.  Genius, which raised $56.9 million on the promise that it would one day annotate the entire internet, has been losing its minds. In January, the company quietly laid off a quarter of its staff, with the bulk of the cuts coming from the engineering department. In a post on the Genius blog at the time, co-founder Tom Lehman told employees that Genius planned to shift its emphasis away from the annotation platform that once attracted top-tier investors in favor of becoming a more video-focused media company.  'After taking a careful look at the company and our priorities,' Lehman wrote, 'we’ve had to make some tough decisions about how we want to spend our resources. And unfortunately this meant that today we laid off some very talented people.' The company then took the unusual step of posting the Genius usernames of those it had laid off — 12 full-time and five part-time employees.  'WE NEEDED TO SHIFT RESOURCES FROM CAPTURING KNOWLEDGE... TOWARD PACKAGING AND DISTRIBUTING KNOWLEDGE.' At the same time, Lehman noted that the company was continuing to hire for roles in video and sales. The company recently redesigned its homepage with expanded space for editorial content and advertising. It has also been deepening its Behind the Lyrics partnership with Spotify, for which it contributes a mix of song lyrics and factoids that pop up in a slideshow format when you’re listening to popular songs.  'The change we made in January was in recognition of the fact that we needed to shift resources from capturing knowledge — which we've been doing almost exclusively for the past five years — toward packaging and distributing knowledge into easy-to-consume formats like video and Spotify Behind the Lyrics,' Lehman told The Verge.  It’s not unusual for tech companies to transform over time, though typically they are loath to lay off engineers. But Genius’ shift is more dramatic than most: going from all-encompassing annotator of the internet to a more traditional media company model, chasing video views alongside an ever-growing number of well-capitalized competitors. The move illustrates the company’s difficulty attracting contributors — and an audience for their contributions — particularly outside of the music world.  In an interview last week, Lehman said the company had turned to video in an effort to reach its core audience‚ which continues to be rap fans, beyond its website and mobile apps. 'Video makes it a little bit more accessible,' he said. 'I love the Genius website. One of my favorite websites. But it can be a little frustrating to use. You have to be really, really dedicated to learn everything about a song on Genius. You've got to be down to click and read a lot.'  Genius’ videos to date have included interviews with artists about their craft, and a series where rappers perform original freestyle verses. One of Lehman’s favorite videos traces a whistle sample featured in a series of popular songs back to its origins in a Quentin Tarantino movie. Last week, Genius posted a video about rapper Lil Yachty learning how to make pizza. The company is also investing in original editorial content, aggregating news headlines, doing Q&As with artists like the Track Burnaz, and writing short profiles. ",
]



windowSize = 1

#User text in content
st.header('Demo')

selected_input_text = st.selectbox("Select sample text", input_text_demo)
text = st.text_area("Selected text", selected_input_text, 330)
language = "english"

#use yake to extract keywords
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
keywords = custom_kw_extractor.extract_keywords(text)




#get keywords and their position
ents = []
text_lower = text.lower()

keywords_list = str(keywords[0][0])
for m in re.finditer(keywords_list, text_lower):
    d = dict(start = m.start(), end = m.end(), label = "")
    ents.append(d)

for i in range(1, len(keywords)):
    kwords = str(keywords[i][0])
    keywords_list += (', ' + kwords)
    for m in re.finditer(kwords, text_lower):
        d = dict(start = m.start(), end = m.end(), label = "")
        ents.append(d)
      
#sort the result by ents, as ent rule suggests
sort_ents = sorted(ents, key=lambda x: x["start"])

st.header('Output')

result_view = st.radio("Choose visualization type",('Highlighting', 'Word cloud', 'Table'), index=0)
if result_view == 'Highlighting':
    #use spacy to higlight the keywords
    ex = [{"text": text,
        "ents": sort_ents,
        "title": None}]

    html = displacy.render(ex, style="ent", manual=True)
    html = html.replace("\n", " ")
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
elif result_view == "Table":
    #tabular data (columns: keywords, score)
    df = pd.DataFrame(keywords, columns=("keywords","score"))
    st.table(df)
  
else:
    #create and generate a word cloud image
    wordcloud = WordCloud(width = 1000, height = 600, max_font_size = 80,
                min_font_size=10, prefer_horizontal=1,
                max_words=numOfKeywords,
                background_color="white",
                collocations=False,
                regexp = r"\w[\w ']+").generate(keywords_list)

    #display the generated image
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)
