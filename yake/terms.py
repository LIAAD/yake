import numpy as np
import math


class SingleWord:
    """Represents a single word in the text."""

    def __init__(self, unique_term, idx, graph):
        """Initialize a single word.

        Args:
            unique_term: Unique term string
            idx: Term ID
            graph: NetworkX graph
        """
        self.unique_term = unique_term
        self.id = idx
        self.tf = 0.0
        self.WFreq = 0.0
        self.WCase = 0.0
        self.tf_a = 0.0  # All caps count
        self.tf_n = 0.0  # Proper noun count
        self.WRel = 1.0
        self.PL = 0.0
        self.PR = 0.0
        self.occurs = {}
        self.WPos = 1.0
        self.WSpread = 0.0
        self.H = 0.0
        self.stopword = False
        self.G = graph
        self.pagerank = 1.0

    def update_h(self, max_tf, avg_tf, std_tf, number_of_sentences, features=None):
        """Update the importance score (H) for a single word based on multiple features.
        
        This function calculates and updates various statistical features that determine
        the word's importance as a potential keyword. It combines term relevance, frequency,
        spread across the document, case information, and position to compute an overall
        importance score (H). A lower H score indicates a more important term.
        
        The features calculated include:
        - WRel: Term relevance based on connection to other terms in the graph
        - WFreq: Normalized term frequency relative to document statistics
        - WSpread: Term distribution across document sentences
        - WCase: Case feature capturing capitalization patterns (all caps, proper nouns)
        - WPos: Position feature based on median occurrence position in the text
        
        These features are then combined using a formula that balances their contributions
        to produce the final H score.

        Args:
            max_tf: Maximum term frequency in the document
            avg_tf: Average term frequency across all terms
            std_tf: Standard deviation of term frequency
            number_of_sentences: Total number of sentences in document
            features: List of specific features to calculate or None to calculate all
        """
        if features is None or "WRel" in features:
            self.PL = self.WDL / max_tf
            self.PR = self.WDR / max_tf
            self.WRel = (0.5 + (self.PWL * (self.tf / max_tf))) + (
                0.5 + (self.PWR * (self.tf / max_tf))
            )

        if features is None or "WFreq" in features:
            self.WFreq = self.tf / (avg_tf + std_tf)

        if features is None or "WSpread" in features:
            self.WSpread = len(self.occurs) / number_of_sentences

        if features is None or "WCase" in features:
            self.WCase = max(self.tf_a, self.tf_n) / (1.0 + math.log(self.tf))

        if features is None or "WPos" in features:
            self.WPos = math.log(math.log(3.0 + np.median(list(self.occurs.keys()))))

        self.H = (self.WPos * self.WRel) / (
            self.WCase + (self.WFreq / self.WRel) + (self.WSpread / self.WRel)
        )

    @property
    def WDR(self):
        """Get number of outgoing edges."""
        return len(self.G.out_edges(self.id))

    @property
    def WIR(self):
        """Get sum of weights of outgoing edges."""
        return sum(d["TF"] for _, _, d in self.G.out_edges(self.id, data=True))

    @property
    def PWR(self):
        """Get probability of right connections."""
        wir = self.WIR
        return 0 if wir == 0 else self.WDR / wir

    @property
    def WDL(self):
        """Get number of incoming edges."""
        return len(self.G.in_edges(self.id))

    @property
    def WIL(self):
        """Get sum of weights of incoming edges."""
        return sum(d["TF"] for _, _, d in self.G.in_edges(self.id, data=True))

    @property
    def PWL(self):
        """Get probability of left connections."""
        wil = self.WIL
        return 0 if wil == 0 else self.WDL / wil

    def add_occur(self, tag, sent_id, pos_sent, pos_text):
        """Add occurrence of term in text.

        Args:
            tag: Term tag
            sent_id: Sentence ID
            pos_sent: Position in sentence
            pos_text: Position in text
        """
        if sent_id not in self.occurs:
            self.occurs[sent_id] = []

        self.occurs[sent_id].append((pos_sent, pos_text))
        self.tf += 1.0

        if tag == "a":
            self.tf_a += 1.0
        if tag == "n":
            self.tf_n += 1.0
