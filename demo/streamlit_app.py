import streamlit as st
import yake
import pandas as pd

st.set_page_config(page_title="YAKE! Keyword Extractor", page_icon="🔍", layout="wide")

st.sidebar.title("YAKE! Keyword Extractor")
st.sidebar.markdown("""
YAKE! (Yet Another Keyword Extractor) is a lightweight unsupervised automatic keyword extraction method that uses text statistical features to select the most important keywords from a document.
For more information, check out the [YAKE GitHub repository](https://github.com/LIAAD/yake).
""")

# Language selection
languages = {
    "English": "en",
    "Portuguese": "pt",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Dutch": "nl",
    "Arabic": "ar",
    "Czech": "cz",
    "Danish": "da",
    "Finnish": "fi",
    "Greek": "el",
    "Hungarian": "hu",
    "Croatian": "hr",
    "Indonesian": "id",
    "Latvian": "lv",
    "Norwegian": "no",
    "Polish": "pl",
    "Romanian": "ro",
    "Russian": "ru",
    "Swedish": "sv",
    "Hindi": "hi",
}
selected_language = st.sidebar.selectbox("Language", list(languages.keys()))

# Other parameters
max_ngram_size = st.sidebar.slider("Max ngram size", 1, 5, 3)
deduplication_threshold = st.sidebar.slider("Deduplication threshold", 0.0, 1.0, 0.9)
deduplication_algo = st.sidebar.selectbox(
    "Deduplication algorithm", ["leve", "jaro", "seqm"]
)
num_keywords = st.sidebar.slider("Number of keywords to extract", 5, 50, 10)
window_size = st.sidebar.slider("Window size", 1, 5, 2)

# Input options tab
tab1, tab2 = st.tabs(["Enter Text", "Upload File"])

# Text input
with tab1:
    text_input = st.text_area("Paste your text here:", height=200)
    process_text_button = st.button("Extract Keywords", key="process_text")
    input_text = text_input if process_text_button and text_input else None

# File upload
with tab2:
    uploaded_file = st.file_uploader("Choose a text file", type=["txt", "csv", "pdf"])
    process_file_button = st.button("Extract Keywords", key="process_file")
    if process_file_button and uploaded_file:
        try:
            # Simple handling for txt files - in a real app you'd want to handle PDF, etc.
            input_text = uploaded_file.getvalue().decode("utf-8")
        except:
            st.error("Error reading file. Please make sure it's a text file.")
            input_text = None
    else:
        input_text = None if process_file_button else input_text


# Process text if available
if input_text:
    # st.subheader("Text for Analysis")
    # st.write(input_text[:1000] + "..." if len(input_text) > 1000 else input_text)

    with st.spinner("Extracting keywords..."):
        # Configure YAKE
        language = languages[selected_language]
        kw_extractor = yake.KeywordExtractor(
            lan=language,
            n=max_ngram_size,
            dedup_lim=deduplication_threshold,
            dedup_func=deduplication_algo,
            window_size=window_size,
            top=num_keywords,
        )

        # Extract keywords
        keywords = kw_extractor.extract_keywords(input_text)

        # Display results in tabs
        st.subheader("Extracted Keywords")
        st.markdown("The lower the score, the more relevant the keyword is.")

        # Create DataFrame for keywords
        kw_df = pd.DataFrame(keywords, columns=["Keyword", "Score"])

        # Display as table
        st.table(kw_df)
