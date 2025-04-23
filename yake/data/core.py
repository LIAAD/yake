"""Core data representation class for YAKE keyword extraction."""

import string
import networkx as nx
import numpy as np

from .utils import pre_filter, tokenize_sentences, get_tag
from .single_word import SingleWord
from .composed_word import ComposedWord

class DataCore:
    """Core data representation for document analysis and keyword extraction."""
    def __init__(self, text, stopword_set, config=None):
        """Initialize the data core with text and configuration."""
        # Initialize default configuration
        if config is None:
            config = {}

        # Extract configuration values with defaults
        windows_size = config.get("windows_size", 2)
        n = config.get("n", 3)
        tags_to_discard = config.get("tags_to_discard", set(["u", "d"]))
        exclude = config.get("exclude", set(string.punctuation))

        self._state = {
            # Configuration
            "config": {
                "exclude": exclude,
                "tags_to_discard": tags_to_discard,
                "stopword_set": stopword_set  # Moved here from direct attribute
            },

            # Text analysis results
            "text_stats": {
                "number_of_sentences": 0,
                "number_of_words": 0
            },

            # Data collections
            "collections": {
                "terms": {},            # Dictionary of term objects
                "candidates": {},       # Dictionary of candidate objects
                "sentences_obj": [],    # Processed sentence objects
                "sentences_str": [],    # Raw sentence strings
                "freq_ns": {}           # Frequency of n-grams
            },

            # Graph for co-occurrence analysis
            "g": nx.DiGraph()  # Moved here from direct attribute
        }

        # Initialize n-gram frequencies
        for i in range(n):
            self._state["collections"]["freq_ns"][i + 1] = 0.0

        # Build the data structures
        self._build(text, windows_size, n)

    # --- Property accessors for backward compatibility ---

    # Configuration properties
    @property
    def exclude(self):
        return self._state["config"]["exclude"]

    @property
    def tags_to_discard(self):
        return self._state["config"]["tags_to_discard"]

    @property
    def stopword_set(self):
        return self._state["config"]["stopword_set"]

    @property
    def g(self):
        return self._state["g"]

    # Text statistics properties
    @property
    def number_of_sentences(self):
        return self._state["text_stats"]["number_of_sentences"]

    @number_of_sentences.setter
    def number_of_sentences(self, value):
        self._state["text_stats"]["number_of_sentences"] = value

    @property
    def number_of_words(self):
        return self._state["text_stats"]["number_of_words"]

    @number_of_words.setter
    def number_of_words(self, value):
        self._state["text_stats"]["number_of_words"] = value

    # Collection properties
    @property
    def terms(self):
        return self._state["collections"]["terms"]

    @property
    def candidates(self):
        return self._state["collections"]["candidates"]

    @property
    def sentences_obj(self):
        return self._state["collections"]["sentences_obj"]

    @property
    def sentences_str(self):
        return self._state["collections"]["sentences_str"]

    @sentences_str.setter
    def sentences_str(self, value):
        self._state["collections"]["sentences_str"] = value

    @property
    def freq_ns(self):
        return self._state["collections"]["freq_ns"]

    # --- Internal utility methods ---
    def _build(self, text, windows_size, n):
        """Build the data structures from the text."""
        text = pre_filter(text)
        self.sentences_str = tokenize_sentences(text)
        self.number_of_sentences = len(self.sentences_str)
        pos_text = 0

        # Create a processing context dictionary to pass fewer arguments
        context = {"windows_size": windows_size, "n": n}

        for sentence_id, sentence in enumerate(self.sentences_str):
            pos_text = self._process_sentence(sentence, sentence_id, pos_text, context)
        self.number_of_words = pos_text

    def _process_sentence(self, sentence, sentence_id, pos_text, context):
        """Process a single sentence."""
        sentence_obj_aux = []
        block_of_word_obj = []

        # Extend the context with sentence information
        processing_context = context.copy()
        processing_context["sentence_id"] = sentence_id

        for pos_sent, word in enumerate(sentence):
            if len([c for c in word if c in self.exclude]) == len(word):
                if len(block_of_word_obj) > 0:
                    sentence_obj_aux.append(block_of_word_obj)
                    block_of_word_obj = []
            else:
                word_context = {
                    "pos_sent": pos_sent,
                    "block_of_word_obj": block_of_word_obj,
                }
                pos_text = self._process_word(
                    word, pos_text, processing_context, word_context
                )

        if len(block_of_word_obj) > 0:
            sentence_obj_aux.append(block_of_word_obj)
        if len(sentence_obj_aux) > 0:
            self.sentences_obj.append(sentence_obj_aux)
        return pos_text

    def _process_word(self, word, pos_text, context, word_context):
        """Process a single word."""
        sentence_id = context["sentence_id"]
        windows_size = context["windows_size"]
        n = context["n"]
        pos_sent = word_context["pos_sent"]
        block_of_word_obj = word_context["block_of_word_obj"]

        tag = self.get_tag(word, pos_sent)
        term_obj = self.get_term(word)
        term_obj.add_occur(tag, sentence_id, pos_sent, pos_text)
        pos_text += 1
        if tag not in self.tags_to_discard:
            self._update_cooccurrence(block_of_word_obj, term_obj, windows_size)
        self._generate_candidates((tag, word), term_obj, block_of_word_obj, n)
        block_of_word_obj.append((tag, word, term_obj))
        return pos_text

    def _update_cooccurrence(self, block_of_word_obj, term_obj, windows_size):
        """Update co-occurrence information between terms."""
        word_windows = list(
            range(max(0, len(block_of_word_obj) - windows_size), len(block_of_word_obj))
        )
        for w in word_windows:
            if block_of_word_obj[w][0] not in self.tags_to_discard:
                self.add_cooccur(block_of_word_obj[w][2], term_obj)

    def _generate_candidates(self, term, term_obj, block_of_word_obj, n):
        """Generate keyword candidates from terms."""
        candidate = [term + (term_obj,)]
        cand = ComposedWord(candidate)
        self.add_or_update_composedword(cand)
        word_windows = list(
            range(max(0, len(block_of_word_obj) - (n - 1)), len(block_of_word_obj))
        )[::-1]
        for w in word_windows:
            candidate.append(block_of_word_obj[w])
            self.freq_ns[len(candidate)] += 1.0
            cand = ComposedWord(candidate[::-1])
            self.add_or_update_composedword(cand)

    # --- Public API methods ---

    def get_tag(self, word, i):
        """Get the tag for a word."""
        return get_tag(word, i, self.exclude)

    def build_candidate(self, candidate_string):
        """Build a candidate from a string."""
        from segtok.tokenizer import web_tokenizer, split_contractions

        tokenized_words = [
            w
            for w in split_contractions(web_tokenizer(candidate_string.lower()))
            if not (w.startswith("'") and len(w) > 1) and len(w) > 0
        ]

        candidate_terms = []
        for index, word in enumerate(tokenized_words):
            tag = self.get_tag(word, index)
            term_obj = self.get_term(word, save_non_seen=False)

            # Skip terms with zero term frequency
            if term_obj.tf == 0:
                term_obj = None

            candidate_terms.append((tag, word, term_obj))

        # Check if the candidate has any valid terms
        if not any(term[2] for term in candidate_terms):
            return ComposedWord(None)

        return ComposedWord(candidate_terms)

    def build_single_terms_features(self, features=None):
        """Build features for single terms."""
        valid_terms = [term for term in self.terms.values() if not term.stopword]
        valid_tfs = np.array([x.tf for x in valid_terms])

        if len(valid_tfs) == 0:
            return

        avg_tf = valid_tfs.mean()
        std_tf = valid_tfs.std()
        max_tf = max(x.tf for x in self.terms.values())
        stats = {
            "max_tf": max_tf,
            "avg_tf": avg_tf,
            "std_tf": std_tf,
            "number_of_sentences": self.number_of_sentences,
        }
        list(map(lambda x: x.update_h(stats, features=features), self.terms.values()))

    def build_mult_terms_features(self, features=None):
        """Build features for multi-word terms."""
        list(
            map(
                lambda x: x.update_h(features=features),
                [cand for cand in self.candidates.values() if cand.is_valid()],
            )
        )

    def get_term(self, str_word, save_non_seen=True):
        """Get or create a term object for a word."""
        unique_term = str_word.lower()
        simples_sto = unique_term in self.stopword_set
        if unique_term.endswith("s") and len(unique_term) > 3:
            unique_term = unique_term[:-1]

        if unique_term in self.terms:
            return self.terms[unique_term]

        simples_unique_term = unique_term
        for pontuation in self.exclude:
            simples_unique_term = simples_unique_term.replace(pontuation, "")
        isstopword = (
            simples_sto
            or unique_term in self.stopword_set
            or len(simples_unique_term) < 3
        )

        term_id = len(self.terms)
        term_obj = SingleWord(unique_term, term_id, self.g)
        term_obj.stopword = isstopword

        if save_non_seen:
            self.g.add_node(term_id)
            self.terms[unique_term] = term_obj

        return term_obj

    def add_cooccur(self, left_term, right_term):
        """Add a co-occurrence relationship between two terms."""
        if right_term.id not in self.g[left_term.id]:
            self.g.add_edge(left_term.id, right_term.id, tf=0.0)
        self.g[left_term.id][right_term.id]["tf"] += 1.0

    def add_or_update_composedword(self, cand):
        """Add or update a composed word in the candidates collection."""
        if cand.unique_kw not in self.candidates:
            self.candidates[cand.unique_kw] = cand
        else:
            self.candidates[cand.unique_kw].uptade_cand(cand)
        self.candidates[cand.unique_kw].tf += 1.0
