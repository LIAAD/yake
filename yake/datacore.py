from typing import Set
from segtok.segmenter import split_multi
from segtok.tokenizer import web_tokenizer, split_contractions

import networkx as nx
import numpy as np
import string
import re
from yake.ngrams import ComposedWord
from yake.terms import SingleWord

STOPWORD_WEIGHT = "bi"


class DataCore:
    def __init__(
        self,
        text: str,
        stopword_set: Set[str],
        windowsSize: int,
        n: int,
        tagsToDiscard: Set[str] = None,
        exclude: Set[str] = None,
    ):
        """Initialize the data core for keyword extraction.

        Args:
            text: Input text to process
            stopword_set: Set of stopwords to ignore
            windowsSize: Size of window for co-occurrence matrix
            n: Maximum n-gram size
            tagsToDiscard: Tags to discard during processing
            exclude: Set of characters to exclude
        """
        self.number_of_sentences = 0
        self.number_of_words = 0
        self.terms = {}
        self.candidates = {}
        self.sentences_obj = []
        self.sentences_str = []
        self.G = nx.DiGraph()
        self.exclude = exclude or set(string.punctuation)
        self.tagsToDiscard = tagsToDiscard or set(["u", "d"])
        self.freq_ns = {}
        for i in range(n):
            self.freq_ns[i + 1] = 0.0
        self.stopword_set = stopword_set
        self._build(text, windowsSize, n)

    def build_candidate(self, candidate_string: str):
        """Build a candidate from a string.

        This function processes a candidate string by tokenizing it, tagging each word,
        and creating a ComposedWord object from the resulting terms. It's used to
        convert external strings into the internal candidate representation.

        Args:
            candidate_string: String to build candidate from

        Returns:
            A ComposedWord instance representing the candidate, or an invalid
            ComposedWord if no valid terms were found
        """
        sentences_str = [
            w
            for w in split_contractions(web_tokenizer(candidate_string.lower()))
            if not (w.startswith("'") and len(w) > 1) and len(w) > 0
        ]
        candidate_terms = []
        for i, word in enumerate(sentences_str):
            tag = self.get_tag(word, i)
            term_obj = self.get_term(word, save_non_seen=False)
            if term_obj.tf == 0:
                term_obj = None
            candidate_terms.append((tag, word, term_obj))

        if len([cand for cand in candidate_terms if cand[2] is not None]) == 0:
            invalid_virtual_cand = ComposedWord(None)
            return invalid_virtual_cand

        virtual_cand = ComposedWord(candidate_terms)
        return virtual_cand

    def _build(self, text: str, windowsSize: int, n: int):
        """Build the datacore features.

        This method processes the input text to extract terms, build the co-occurrence graph,
        and generate candidate keyphrases. It performs the following steps:
        1. Pre-filters and tokenizes the text into sentences and words
        2. Processes each word to create term objects
        3. Builds a co-occurrence matrix based on the window size
        4. Generates candidate keyphrases of various n-gram sizes
        5. Updates internal data structures with the extracted information

        Args:
            text: Input text to process
            windowsSize: Size of window for co-occurrence matrix calculation
            n: Maximum n-gram size to consider for candidate keyphrases
        """
        text = self.pre_filter(text)
        self.sentences_str = [
            [
                w
                for w in split_contractions(web_tokenizer(s))
                if not (w.startswith("'") and len(w) > 1) and len(w) > 0
            ]
            for s in list(split_multi(text))
            if len(s.strip()) > 0
        ]
        self.number_of_sentences = len(self.sentences_str)
        pos_text = 0

        for sentence_id, sentence in enumerate(self.sentences_str):
            sentence_obj_aux = []
            block_of_word_obj = []

            for pos_sent, word in enumerate(sentence):
                # Skip words made only of excluded characters
                if all(c in self.exclude for c in word):
                    if block_of_word_obj:
                        sentence_obj_aux.append(block_of_word_obj)
                        block_of_word_obj = []
                else:
                    tag = self.get_tag(word, pos_sent)
                    term_obj = self.get_term(word)
                    term_obj.add_occur(tag, sentence_id, pos_sent, pos_text)
                    pos_text += 1

                    # Create co-occurrence matrix
                    if tag not in self.tagsToDiscard:
                        word_windows = list(
                            range(
                                max(0, len(block_of_word_obj) - windowsSize),
                                len(block_of_word_obj),
                            )
                        )
                        for w in word_windows:
                            if block_of_word_obj[w][0] not in self.tagsToDiscard:
                                self.add_cooccur(block_of_word_obj[w][2], term_obj)

                    # Generate candidate keyphrase list
                    candidate = [(tag, word, term_obj)]
                    cand = ComposedWord(candidate)
                    self.add_or_update_composed_word(cand)

                    word_windows = list(
                        range(
                            max(0, len(block_of_word_obj) - (n - 1)),
                            len(block_of_word_obj),
                        )
                    )[::-1]

                    for w in word_windows:
                        candidate.append(block_of_word_obj[w])
                        self.freq_ns[len(candidate)] += 1.0
                        cand = ComposedWord(candidate[::-1])
                        self.add_or_update_composed_word(cand)

                    # Add term to the block of words' buffer
                    block_of_word_obj.append((tag, word, term_obj))

            if block_of_word_obj:
                sentence_obj_aux.append(block_of_word_obj)

            if sentence_obj_aux:
                self.sentences_obj.append(sentence_obj_aux)

        self.number_of_words = pos_text

    def build_single_terms_features(self, features=None):
        """Build features for single terms.

        Calculates and updates statistical features for all single terms in the text.
        This includes term frequency statistics and other features specified in the
        features parameter. Only non-stopword terms are considered for statistics
        calculation.

        Args:
            features: List of features to build. If None, all available features will be built.
        """
        valid_terms = [term for term in self.terms.values() if not term.stopword]
        if not valid_terms:
            return

        valid_tfs = np.array([x.tf for x in valid_terms])
        avg_tf = valid_tfs.mean()
        std_tf = valid_tfs.std()
        max_tf = max(term.tf for term in self.terms.values())

        for term in self.terms.values():
            term.update_h(
                max_tf=max_tf,
                avg_tf=avg_tf,
                std_tf=std_tf,
                number_of_sentences=self.number_of_sentences,
                features=features,
            )

    def build_mult_terms_features(self, features=None):
        """Build features for multi-word terms.

        Updates the features for all valid multi-word candidate terms (n-grams).
        Only candidates that pass the validity check will have their features updated.

        Args:
            features: List of features to build. If None, all available features will be built.
        """
        for cand in self.candidates.values():
            if cand.is_valid():
                cand.update_h(features=features)

    def pre_filter(self, text: str) -> str:
        """Pre-filter text before processing.

        Performs initial text cleaning and formatting:
        1. Handles line breaks and paragraph structure
        2. Ensures proper spacing between sentences
        3. Replaces tabs with spaces

        Args:
            text: Input text to be filtered

        Returns:
            Filtered text ready for further processing
        """
        prog = re.compile(r"^(\s*([A-Z]))")
        parts = text.split("\n")
        buffer = ""

        for part in parts:
            sep = " "
            if prog.match(part):
                sep = "\n\n"
            buffer += sep + part.replace("\t", " ")

        return buffer

    def get_tag(self, word: str, position: int) -> str:
        """Get tag for a word.

        Determines the type of word based on its characteristics:
        - 'd': Digit (numeric value)
        - 'u': Unknown (mixed alphanumeric or special characters)
        - 'a': All caps (acronym)
        - 'n': Proper noun (capitalized word not at sentence start)
        - 'p': Regular word

        Args:
            word: Word to tag
            position: Position in sentence (used to identify proper nouns)

        Returns:
            Tag as string representing the word type
        """
        try:
            w2 = word.replace(",", "")
            float(w2)
            return "d"  # Digit
        except ValueError:
            cdigit = sum(1 for c in word if c.isdigit())
            calpha = sum(1 for c in word if c.isalpha())

            if (
                (cdigit > 0 and calpha > 0)
                or (cdigit == 0 and calpha == 0)
                or sum(1 for c in word if c in self.exclude) > 1
            ):
                return "u"  # Unknown

            if all(c.isupper() for c in word):
                return "a"  # All caps

            if (
                sum(1 for c in word if c.isupper()) == 1
                and len(word) > 1
                and word[0].isupper()
                and position > 0
            ):
                return "n"  # Proper noun

        return "p"  # Regular word

    def get_term(self, word: str, save_non_seen: bool = True) -> "SingleWord":
        """Get or create a term object for a word.

        Retrieves an existing term object for a word or creates a new one.
        The function also:
        1. Normalizes the word (lowercase, handles plural forms)
        2. Determines if the word is a stopword
        3. Creates a new term object if needed and adds it to the graph

        Args:
            word: Word to get term for
            save_non_seen: Whether to save new terms to the internal dictionary.
                           If False, creates a temporary term without saving it.

        Returns:
            SingleWord instance representing the term
        """
        unique_term = word.lower()
        is_simple_stopword = unique_term in self.stopword_set

        if unique_term.endswith("s") and len(unique_term) > 3:
            unique_term = unique_term[:-1]

        if unique_term in self.terms:
            return self.terms[unique_term]

        # Check if word is a stopword
        simple_unique_term = unique_term
        for punctuation in self.exclude:
            simple_unique_term = simple_unique_term.replace(punctuation, "")

        is_stopword = (
            is_simple_stopword
            or unique_term in self.stopword_set
            or len(simple_unique_term) < 3
        )

        # Create new term
        term_id = len(self.terms)
        term_obj = SingleWord(unique_term, term_id, self.G)
        term_obj.stopword = is_stopword

        if save_non_seen:
            self.G.add_node(term_id)
            self.terms[unique_term] = term_obj

        return term_obj

    def add_cooccur(self, left_term: "SingleWord", right_term: "SingleWord"):
        """Add co-occurrence between terms.

        Updates the co-occurrence graph by adding or incrementing an edge between
        two terms. This information is used to calculate term relatedness and
        importance in the text.

        Args:
            left_term: Left term in the co-occurrence relationship
            right_term: Right term in the co-occurrence relationship
        """
        if right_term.id not in self.G[left_term.id]:
            self.G.add_edge(left_term.id, right_term.id, TF=0.0)
        self.G[left_term.id][right_term.id]["TF"] += 1.0

    def add_or_update_composed_word(self, cand: "ComposedWord"):
        """Add or update a composed word.

        Adds a new candidate composed word (n-gram) to the candidates dictionary
        or updates an existing one by incrementing its frequency. This is used to
        track potential keyphrases in the text.

        Args:
            cand: ComposedWord instance to add or update in the candidates dictionary
        """
        if cand.unique_kw not in self.candidates:
            self.candidates[cand.unique_kw] = cand
        else:
            self.candidates[cand.unique_kw].update_cand(cand)
        self.candidates[cand.unique_kw].tf += 1.0
