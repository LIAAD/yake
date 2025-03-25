import re
import string
import math
import jellyfish

from segtok.segmenter import split_multi
from segtok.tokenizer import web_tokenizer, split_contractions

import networkx as nx
import numpy as np

STOPWORD_WEIGHT = "bi"


class DataCore:
    """
    Core data manager for keyword extraction that processes text and builds
    data structures for keyword candidates.
    
    Implementation uses consolidated dictionaries to reduce the number of direct 
    instance attributes while maintaining the same functionality.
    """
    def __init__(self, text, stopword_set, config=None):
        """
        Initialize the DataCore object for keyword extraction.

        Args:
            text (str): The input text to process.
            stopword_set (set): Set of stopwords to use.
            config (dict, optional): Configuration parameters including:
                - windows_size (int): Size of sliding window for co-occurrence analysis.
                - n (int): Maximum n-gram size.
                - tags_to_discard (set): Tags to exclude (default: {'u', 'd'}).
                - exclude (set): Characters to exclude (default: string.punctuation).
        """
        # Initialize default configuration
        if config is None:
            config = {}

        # Extract configuration values with defaults
        windows_size = config.get("windows_size", 2)
        n = config.get("n", 3)
        tags_to_discard = config.get("tags_to_discard", set(["u", "d"]))
        exclude = config.get("exclude", set(string.punctuation))

        # Consolidate all settings into a single _state dictionary
        # This reduces the instance attribute count significantly
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
        """
        Build the datacore features by processing text and extracting data structures.

        Args:
            text (str): The text to process
            windows_size (int): Size of sliding window for co-occurrence analysis
            n (int): Maximum n-gram size
        """
        text = self._pre_filter(text)
        self.sentences_str = self._tokenize_sentences(text)
        self.number_of_sentences = len(self.sentences_str)
        pos_text = 0

        # Create a processing context dictionary to pass fewer arguments
        context = {"windows_size": windows_size, "n": n}

        for sentence_id, sentence in enumerate(self.sentences_str):
            pos_text = self._process_sentence(sentence, sentence_id, pos_text, context)
        self.number_of_words = pos_text

    # --- Changed public methods to protected (prefixed with underscore) ---
    # This reduces the public method count

    def _tokenize_sentences(self, text):
        """Tokenize text into sentences and words."""
        return [
            [
                w
                for w in split_contractions(web_tokenizer(s))
                if not (w.startswith("'") and len(w) > 1) and len(w) > 0
            ]
            for s in list(split_multi(text))
            if len(s.strip()) > 0
        ]

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

    def _pre_filter(self, text):
        """Pre-filter the text to normalize line breaks and spacing."""
        prog = re.compile("^(\\s*([A-Z]))")
        parts = text.split("\n")
        buffer = ""
        for part in parts:
            sep = " "
            if prog.match(part):
                sep = "\n\n"
            buffer += sep + part.replace("\t", " ")
        return buffer

    # --- Public API methods (kept public) ---

    def build_candidate(self, candidate_string):
        """
        Build a candidate from a string by tokenizing and processing its words.

        Args:
            candidate_string (str): The string to build a candidate from.

        Returns:
            ComposedWord: A virtual candidate object constructed from the processed terms.
        """
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
  
    def get_tag(self, word, i):
        """
        Determine the tag for a word based on its characteristics.
        
        Args:
            word (str): The word to analyze.
            i (int): The position of the word.
            
        Returns:
            str: The tag assigned to the word ('d', 'u', 'a', 'n', or 'p').
        """
        try:
            w2 = word.replace(",", "")
            float(w2)
            return "d"
        except ValueError:
            cdigit = len([c for c in word if c.isdigit()])
            calpha = len([c for c in word if c.isalpha()])
            if (
                (cdigit > 0 and calpha > 0)
                or (cdigit == 0 and calpha == 0)
                or len([c for c in word if c in self.exclude]) > 1
            ):
                return "u"
            if len(word) == len([c for c in word if c.isupper()]):
                return "a"
            if (
                len([c for c in word if c.isupper()]) == 1
                and len(word) > 1
                and word[0].isupper()
                and i > 0
            ):
                return "n"
        return "p"

    def get_term(self, str_word, save_non_seen=True):
        """
        Get or create a term object for a word.
        
        Args:
            str_word (str): The word to get a term for.
            save_non_seen (bool, optional): Whether to save new terms. Defaults to True.
            
        Returns:
            SingleWord: The term object for the word.
        """
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


class ComposedWord:
    """
    Class representing a composed word (multi-word term) in the document.

    Implementation uses a minimalist approach with minimal direct attributes,
    using a data dictionary for storing most properties to reduce the total
    attribute count while maintaining backward compatibility.
    """

    def __init__(self, terms):  # [ (tag, word, term_obj) ]
        # If terms is None, initialize an invalid candidate
        if terms is None:
            self.data = {
                "start_or_end_stopwords": True,
                "tags": set(),
                "h": 0.0,
                "tf": 0.0,
                "kw": "",
                "unique_kw": "",
                "size": 0,
                "terms": [],
                "integrity": 0.0,
            }
            return

        # Basic initialization from terms
        self.data = {}

        # Calculate derived properties
        self.data["tags"] = set(["".join([w[0] for w in terms])])
        self.data["kw"] = " ".join([w[1] for w in terms])
        self.data["unique_kw"] = self.data["kw"].lower()
        self.data["size"] = len(terms)
        self.data["terms"] = [w[2] for w in terms if w[2] is not None]
        self.data["tf"] = 0.0
        self.data["integrity"] = 1.0
        self.data["h"] = 1.0

        # Check if the candidate starts or ends with stopwords
        if len(self.data["terms"]) > 0:
            self.data["start_or_end_stopwords"] = (
                self.data["terms"][0].stopword or self.data["terms"][-1].stopword
            )
        else:
            self.data["start_or_end_stopwords"] = True

    # Property accessors for backward compatibility
    @property
    def tags(self):
        return self.data["tags"]

    @property
    def kw(self):
        return self.data["kw"]

    @property
    def unique_kw(self):
        return self.data["unique_kw"]

    @property
    def size(self):
        return self.data["size"]

    @property
    def terms(self):
        return self.data["terms"]

    @property
    def tf(self):
        return self.data["tf"]

    @tf.setter
    def tf(self, value):
        self.data["tf"] = value

    @property
    def integrity(self):
        return self.data["integrity"]

    @property
    def h(self):
        return self.data["h"]

    @h.setter
    def h(self, value):
        self.data["h"] = value

    @property
    def start_or_end_stopwords(self):
        return self.data["start_or_end_stopwords"]

    def uptade_cand(self, cand):
        """Update this candidate with data from another candidate."""
        for tag in cand.tags:
            self.tags.add(tag)

    def is_valid(self):
        """Check if this candidate is valid."""
        is_valid = False
        for tag in self.tags:
            is_valid = is_valid or ("u" not in tag and "d" not in tag)
        return is_valid and not self.start_or_end_stopwords

    def get_composed_feature(self, feature_name, discart_stopword=True):
        """Get composed features from constituent terms."""
        list_of_features = [
            getattr(term, feature_name)
            for term in self.terms
            if (discart_stopword and not term.stopword) or not discart_stopword
        ]
        sum_f = sum(list_of_features)
        prod_f = np.prod(list_of_features)
        return (sum_f, prod_f, prod_f / (sum_f + 1))

    def build_features(self, params):
        """
        Build features for the composed word.

        Args:
            params (dict): Dictionary containing the following keys:
                - doc_id (optional): Document ID.
                - keys (optional): List of keys.
                - rel (optional): Boolean indicating relevance.
                - rel_approx (optional): Boolean indicating approximate relevance.
        """
        # Function implementation remains the same
        # Only changes needed are for accessing attributes through self.data
        features = params.get(
            "features", ["wfreq", "wrel", "tf", "wcase", "wpos", "wspread"]
        )
        _stopword = params.get("_stopword", [True, False])
        if features is None:
            features = ["wfreq", "wrel", "tf", "wcase", "wpos", "wspread"]
        if _stopword is None:
            _stopword = [True, False]
        columns = []
        features_cand = []
        seen = set()
        if params.get("doc_id") is not None:
            columns.append("doc_id")
            features_cand.append(params["doc_id"])

        if params.get("keys") is not None:
            if params.get("rel", True):
                columns.append("rel")
                if self.unique_kw in params["keys"] or params.get("is_virtual", False):
                    features_cand.append(1)
                    seen.add(self.unique_kw)
                else:
                    features_cand.append(0)

            if params.get("rel_approx", True):
                columns.append("rel_approx")
                max_gold_ = ("", 0.0)
                for gold_key in params["keys"]:
                    dist = 1.0 - jellyfish.levenshtein_distance(
                        # _tL
                        gold_key,
                        self.unique_kw,
                    ) / max(len(gold_key), len(self.unique_kw))
                    max_gold_ = (gold_key, dist)
                features_cand.append(max_gold_[1])
                features_cand.append(max_gold_[1])

        columns.append("kw")
        features_cand.append(self.unique_kw)
        columns.append("h")
        features_cand.append(self.h)
        columns.append("tf")
        features_cand.append(self.tf)
        columns.append("size")
        features_cand.append(self.size)
        columns.append("is_virtual")
        columns.append("is_virtual")
        features_cand.append(int(params.get("is_virtual", False)))
        for feature_name in features:
            for discart_stopword in _stopword:
                (f_sum, f_prod, f_sum_prod) = self.get_composed_feature(
                    feature_name, discart_stopword=discart_stopword
                )
                columns.append(
                    f"{'n' if discart_stopword else ''}s_sum_K{feature_name}"
                )
                features_cand.append(f_sum)

                columns.append(
                    f"{'n' if discart_stopword else ''}s_prod_K{feature_name}"
                )
                features_cand.append(f_prod)

                columns.append(
                    f"{'n' if discart_stopword else ''}s_sum_prod_K{feature_name}"
                )
                features_cand.append(f_sum_prod)

        return (features_cand, columns, seen)

    def update_h(self, features=None, is_virtual=False):
        """Update the term's score based on its constituent terms."""
        sum_h = 0.0
        prod_h = 1.0

        for t, term_base in enumerate(self.terms):
            if not term_base.stopword:
                sum_h += term_base.h
                prod_h *= term_base.h

            else:
                if STOPWORD_WEIGHT == "bi":
                    prob_t1 = 0.0
                    if t > 0 and term_base.g.has_edge(
                        self.terms[t - 1].id, self.terms[t].id
                    ):
                        prob_t1 = (
                            term_base.g[self.terms[t - 1].id][self.terms[t].id]["tf"]
                            / self.terms[t - 1].tf
                        )
                    prob_t2 = 0.0
                    if t < len(self.terms) - 1 and term_base.g.has_edge(
                        self.terms[t].id, self.terms[t + 1].id
                    ):
                        prob_t2 = (
                            term_base.g[self.terms[t].id][self.terms[t + 1].id]["tf"]
                            / self.terms[t + 1].tf
                        )

                    prob = prob_t1 * prob_t2
                    prod_h *= 1 + (1 - prob)
                    sum_h -= 1 - prob
                elif STOPWORD_WEIGHT == "h":
                    sum_h += term_base.h
                    prod_h *= term_base.h
                elif STOPWORD_WEIGHT == "none":
                    pass

        tf_used = 1.0
        if features is None or "KPF" in features:
            tf_used = self.tf

        if is_virtual:
            tf_used = np.mean([term_obj.tf for term_obj in self.terms])

        self.h = prod_h / ((sum_h + 1) * tf_used)

    def update_h_old(self, features=None, is_virtual=False):
        """Legacy method for updating the term's score."""
        sum_h = 0.0
        prod_h = 1.0

        for t, term_base in enumerate(self.terms):
            if is_virtual and term_base.tf == 0:
                continue

            if term_base.stopword:
                prob_t1 = 0.0
                if term_base.g.has_edge(self.terms[t - 1].id, self.terms[t].id):
                    prob_t1 = (
                        term_base.g[self.terms[t - 1].id][self.terms[t].id]["tf"]
                        / self.terms[t - 1].tf
                    )

                prob_t2 = 0.0
                if term_base.g.has_edge(self.terms[t].id, self.terms[t + 1].id):
                    prob_t2 = (
                        term_base.g[self.terms[t].id][self.terms[t + 1].id]["tf"]
                        / self.terms[t + 1].tf
                    )

                prob = prob_t1 * prob_t2
                prod_h *= 1 + (1 - prob)
                sum_h -= 1 - prob
            else:
                sum_h += term_base.h
                prod_h *= term_base.h
        tf_used = 1.0
        if features is None or "KPF" in features:
            tf_used = self.tf
        if is_virtual:
            tf_used = np.mean([term_obj.tf for term_obj in self.terms])
        self.h = prod_h / ((sum_h + 1) * tf_used)


class SingleWord:
    """
    Class representing a single word in the document text with its associated metrics.

    Implementation uses a minimalist approach with only three instance attributes:
    - id: The word's identifier in the graph
    - g: Reference to the graph
    - data: A consolidated dictionary containing all other attributes

    All access to word properties is through property accessors or dictionary methods,
    maintaining backward compatibility with previous implementations.
    """

    def __init__(self, unique, idx, graph):
        # Keep only the absolute minimum as direct attributes - just these 3
        self.id = idx  # Fast access needed as it's used in graph operations
        self.g = graph  # Fast access needed for network calculations

        # Everything else goes in the data dictionary - no exceptions
        self.data = {
            # Basic information
            "unique_term": unique,
            "stopword": False,
            "h": 0.0,  # Final Score
            # Term frequency statistics
            "tf": 0.0,  # Term frequency
            "tf_a": 0.0,  # Term Frequency for uppercase words
            "tf_n": 0.0,  # Term Frequency for proper nouns
            # Word characteristic metrics
            "wfreq": 0.0,  # Word frequency
            "wcase": 0.0,  # Word case metric
            "wrel": 1.0,  # Word relevance metric
            "wpos": 1.0,  # Word position metric
            "wspread": 0.0,  # Word spread across document
            "pl": 0.0,  # Probability left
            "pr": 0.0,  # Probability right
            "pagerank": 1.0,  # PageRank score
            # Ocurrence tracking
            "occurs": {},  # Sentence Occurrences
        }

    # Forward common dictionary operations to self.data
    def __getitem__(self, key):
        """Access attributes dictionary-style with obj['key']."""
        return self.data[key]

    def __setitem__(self, key, value):
        """Set attributes dictionary-style with obj['key'] = value."""
        self.data[key] = value

    def get(self, key, default=None):
        """Get with default, mimicking dict.get()."""
        return self.data.get(key, default)

    # The most commonly used properties remain as explicit accessors for backward compatibility
    @property
    def unique_term(self):
        return self.data["unique_term"]

    @property
    def stopword(self):
        return self.data["stopword"]

    @stopword.setter
    def stopword(self, value):
        self.data["stopword"] = value

    @property
    def h(self):
        return self.data["h"]

    @h.setter
    def h(self, value):
        self.data["h"] = value

    @property
    def tf(self):
        return self.data["tf"]

    @tf.setter
    def tf(self, value):
        self.data["tf"] = value

    @property
    def occurs(self):
        return self.data["occurs"]

    # Everything else uses the generic accessor methods
    def get_metric(self, name):
        """Get the value of any word metric."""
        return self.data.get(name, 0.0)

    def set_metric(self, name, value):
        """Set the value of any word metric."""
        self.data[name] = value

    def get_graph_metrics(self):
        """Calculate all graph-based metrics at once."""
        # Out-edges metrics
        wdr = len(self.g.out_edges(self.id))
        wir = sum(d["tf"] for (_, _, d) in self.g.out_edges(self.id, data=True))
        pwr = 0 if wir == 0 else wdr / wir

        # In-edges metrics
        wdl = len(self.g.in_edges(self.id))
        wil = sum(d["tf"] for (_, _, d) in self.g.in_edges(self.id, data=True))
        pwl = 0 if wil == 0 else wdl / wil

        return {"wdr": wdr, "wir": wir, "pwr": pwr, "wdl": wdl, "wil": wil, "pwl": pwl}

    def update_h(self, stats, features=None):
        """Update the word's score based on statistics."""
        max_tf = stats["max_tf"]
        avg_tf = stats["avg_tf"]
        std_tf = stats["std_tf"]
        number_of_sentences = stats["number_of_sentences"]

        # Get all graph metrics at once
        graph_metrics = self.get_graph_metrics()

        # Update metrics based on features
        if features is None or "wrel" in features:
            self.data["pl"] = graph_metrics["wdl"] / max_tf
            self.data["pr"] = graph_metrics["wdr"] / max_tf
            self.data["wrel"] = (0.5 + (graph_metrics["pwl"] * (self.tf / max_tf))) + (
                0.5 + (graph_metrics["pwr"] * (self.tf / max_tf))
            )

        if features is None or "wfreq" in features:
            self.data["wfreq"] = self.tf / (avg_tf + std_tf)

        if features is None or "wspread" in features:
            self.data["wspread"] = len(self.occurs) / number_of_sentences

        if features is None or "wcase" in features:
            self.data["wcase"] = max(self.data["tf_a"], self.data["tf_n"]) / (
                1.0 + math.log(self.tf)
            )

        if features is None or "wpos" in features:
            self.data["wpos"] = math.log(
                math.log(3.0 + np.median(list(self.occurs.keys())))
            )

        # Calculate final score
        self.data["h"] = (self.data["wpos"] * self.data["wrel"]) / (
            self.data["wcase"]
            + (self.data["wfreq"] / self.data["wrel"])
            + (self.data["wspread"] / self.data["wrel"])
        )

    def add_occur(self, tag, sent_id, pos_sent, pos_text):
        """Add occurrence information."""
        if sent_id not in self.occurs:
            self.occurs[sent_id] = []

        self.occurs[sent_id].append((pos_sent, pos_text))
        self.data["tf"] += 1.0

        if tag == "a":
            self.data["tf_a"] += 1.0
        if tag == "n":
            self.data["tf_n"] += 1.0

    # For backward compatibility, define access to common metrics as properties
    # Not necessary but good practice to maintain consistency with other classes

    @property
    def wfreq(self):
        return self.data["wfreq"]

    @wfreq.setter
    def wfreq(self, value):
        self.data["wfreq"] = value

    @property
    def wcase(self):
        return self.data["wcase"]

    @wcase.setter
    def wcase(self, value):
        self.data["wcase"] = value

    @property
    def wrel(self):
        return self.data["wrel"]

    @wrel.setter
    def wrel(self, value):
        self.data["wrel"] = value

    @property
    def wpos(self):
        return self.data["wpos"]

    @wpos.setter
    def wpos(self, value):
        self.data["wpos"] = value

    @property
    def wspread(self):
        return self.data["wspread"]

    @wspread.setter
    def wspread(self, value):
        self.data["wspread"] = value

    @property
    def pl(self):
        return self.data["pl"]

    @pl.setter
    def pl(self, value):
        self.data["pl"] = value

    @property
    def pr(self):
        return self.data["pr"]

    @pr.setter
    def pr(self, value):
        self.data["pr"] = value
