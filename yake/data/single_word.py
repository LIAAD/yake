"""
Single word term representation module for YAKE keyword extraction.

This module contains the SingleWord class which represents individual terms
in a document for keyword extraction. It tracks statistical features like
term frequency, position, and relationships with other terms to calculate
a relevance score for each word.
"""

import math
import numpy as np


class SingleWord:
    """
    Representation of a single word term in the document.

    This class stores and calculates statistical features for individual terms,
    including frequency, position, spread, and relationship metrics. These features
    are used to calculate a relevance score that indicates the word's importance
    in the document.

    Attributes:
        See property accessors below for available attributes.
    """

    def __init__(self, unique, idx, graph):
        """
        Initialize a SingleWord term object.

        Args:
            unique (str): The unique normalized term this object represents
            idx (int): Unique identifier for the term in the document
            graph (networkx.DiGraph): Word co-occurrence graph from the document
        """
        self.id = idx  # Fast access needed as it's used in graph operations
        self.g = graph  # Fast access needed for network calculations

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
        """
        Access attributes dictionary-style with obj['key'].

        Args:
            key (str): The attribute key to access

        Returns:
            Any: The value associated with the key
        """
        return self.data[key]

    def __setitem__(self, key, value):
        """
        Set attributes dictionary-style with obj['key'] = value.

        Args:
            key (str): The attribute key to set
            value (Any): The value to associate with the key
        """
        self.data[key] = value

    def get(self, key, default=None):
        """
        Get with default, mimicking dict.get().

        Args:
            key (str): The attribute key to access
            default (Any, optional): The default value if key doesn't exist

        Returns:
            Any: The value associated with the key or the default value
        """
        return self.data.get(key, default)

    # The most commonly used properties remain as explicit accessors for backward compatibility
    @property
    def unique_term(self):
        """Get the unique normalized term this object represents."""
        return self.data["unique_term"]

    @property
    def stopword(self):
        """Get whether this term is a stopword."""
        return self.data["stopword"]

    @stopword.setter
    def stopword(self, value):
        """
        Set whether this term is a stopword.

        Args:
            value (bool): True if the term is a stopword, False otherwise
        """
        self.data["stopword"] = value

    @property
    def h(self):
        """Get the final relevance score of this term (lower is better)."""
        return self.data["h"]

    @h.setter
    def h(self, value):
        """
        Set the final relevance score of this term.

        Args:
            value (float): The new score value
        """
        self.data["h"] = value

    @property
    def tf(self):
        """Get the term frequency (number of occurrences) in the document."""
        return self.data["tf"]

    @tf.setter
    def tf(self, value):
        """
        Set the term frequency value.

        Args:
            value (float): The new term frequency value
        """
        self.data["tf"] = value

    @property
    def occurs(self):
        """Get the dictionary of sentence occurrences for this term."""
        return self.data["occurs"]

    # Everything else uses the generic accessor methods
    def get_metric(self, name):
        """
        Get the value of any word metric.

        Args:
            name (str): The name of the metric to retrieve

        Returns:
            float: The value of the requested metric
        """
        return self.data.get(name, 0.0)

    def set_metric(self, name, value):
        """
        Set the value of any word metric.

        Args:
            name (str): The name of the metric to set
            value (float): The new value for the metric
        """
        self.data[name] = value

    def get_graph_metrics(self):
        """
        Calculate all graph-based metrics at once.

        Analyzes the term's connections in the co-occurrence graph to compute
        various relationship metrics that measure its contextual importance.

        Returns:
            dict: Dictionary containing the calculated graph metrics:
                - wdr: Word different right (number of outgoing edges)
                - wir: Word importance right (sum of outgoing edge weights)
                - pwr: Probability weight right (wdr/wir)
                - wdl: Word different left (number of incoming edges)
                - wil: Word importance left (sum of incoming edge weights)
                - pwl: Probability weight left (wdl/wil)
        """
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
        """
        Update the word's score based on statistics.

        Calculates all the statistical features that determine the word's
        relevance score, using document-level statistics for normalization.

        Args:
            stats (dict): Document statistics including:
                - max_tf (float): Maximum term frequency in the document
                - avg_tf (float): Average term frequency
                - std_tf (float): Standard deviation of term frequency
                - number_of_sentences (int): Total number of sentences
            features (list, optional): Specific features to calculate, or None for all
        """
        max_tf = stats["max_tf"]
        avg_tf = stats["avg_tf"]
        std_tf = stats["std_tf"]
        number_of_sentences = stats["number_of_sentences"]

        # Get all graph metrics at once
        graph_metrics = self.get_graph_metrics()

        # Update metrics based on features
        if features is None or "wrel" in features:
            # Calculate relatedness metrics using graph connections
            self.data["pl"] = graph_metrics["wdl"] / max_tf
            self.data["pr"] = graph_metrics["wdr"] / max_tf
            self.data["wrel"] = (0.5 + (graph_metrics["pwl"] * (self.tf / max_tf))) + (
                0.5 + (graph_metrics["pwr"] * (self.tf / max_tf))
            )

        if features is None or "wfreq" in features:
            # Calculate frequency metric normalized by corpus statistics
            self.data["wfreq"] = self.tf / (avg_tf + std_tf)

        if features is None or "wspread" in features:
            # Calculate spread as proportion of sentences containing the term
            self.data["wspread"] = len(self.occurs) / number_of_sentences

        if features is None or "wcase" in features:
            # Calculate case feature from uppercase and proper noun occurrences
            self.data["wcase"] = max(self.data["tf_a"], self.data["tf_n"]) / (
                1.0 + math.log(self.tf)
            )

        if features is None or "wpos" in features:
            # Calculate position feature from median position of occurrences
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
        """
        Add occurrence information for this term.

        Records where in the document this term appears, tracking sentence ID,
        position within sentence, global position in text, and updates term
        frequency counters.

        Args:
            tag (str): Part-of-speech tag for this occurrence ('a' for acronym, 'n' for proper noun, etc.)
            sent_id (int): Sentence ID where the term appears
            pos_sent (int): Position within the sentence
            pos_text (int): Global position in the entire text
        """
        # Create empty list for this sentence if it's the first occurrence
        if sent_id not in self.occurs:
            self.occurs[sent_id] = []

        # Record position information for this occurrence
        self.occurs[sent_id].append((pos_sent, pos_text))
        self.data["tf"] += 1.0

        # Update special counters for acronyms and proper nouns
        if tag == "a":
            self.data["tf_a"] += 1.0
        if tag == "n":
            self.data["tf_n"] += 1.0

    # For backward compatibility, define access to common metrics as properties
    @property
    def wfreq(self):
        """Get the word frequency metric."""
        return self.data["wfreq"]

    @wfreq.setter
    def wfreq(self, value):
        """Set the word frequency metric."""
        self.data["wfreq"] = value

    @property
    def wcase(self):
        """Get the word case metric."""
        return self.data["wcase"]

    @wcase.setter
    def wcase(self, value):
        """Set the word case metric."""
        self.data["wcase"] = value

    @property
    def wrel(self):
        """Get the word relevance metric."""
        return self.data["wrel"]

    @wrel.setter
    def wrel(self, value):
        """Set the word relevance metric."""
        self.data["wrel"] = value

    @property
    def wpos(self):
        """Get the word position metric."""
        return self.data["wpos"]

    @wpos.setter
    def wpos(self, value):
        """Set the word position metric."""
        self.data["wpos"] = value

    @property
    def wspread(self):
        """Get the word spread metric."""
        return self.data["wspread"]

    @wspread.setter
    def wspread(self, value):
        """Set the word spread metric."""
        self.data["wspread"] = value

    @property
    def pl(self):
        """Get the probability left metric."""
        return self.data["pl"]

    @pl.setter
    def pl(self, value):
        """Set the probability left metric."""
        self.data["pl"] = value

    @property
    def pr(self):
        """Get the probability right metric."""
        return self.data["pr"]

    @pr.setter
    def pr(self, value):
        """Set the probability right metric."""
        self.data["pr"] = value
