"""SingleWord class for representing individual terms."""

import math
import numpy as np

class SingleWord:
    """Representation of a single word term in the document."""

    def __init__(self, unique, idx, graph):

        self.id = idx  # Fast access needed as it's used in graph operations
        self.g = graph  # Fast access needed for network calculations

        self.data = {
            # Basic information
            "unique_term": unique,
            "stopword": False,
            "h": 0.0,  # Final Score
            # Term frequency statistics
            "tf": 0.0,      # Term frequency
            "tf_a": 0.0,    # Term Frequency for uppercase words
            "tf_n": 0.0,    # Term Frequency for proper nouns
            # Word characteristic metrics
            "wfreq": 0.0,   # Word frequency
            "wcase": 0.0,   # Word case metric
            "wrel": 1.0,    # Word relevance metric
            "wpos": 1.0,    # Word position metric
            "wspread": 0.0, # Word spread across document
            "pl": 0.0,      # Probability left
            "pr": 0.0,      # Probability right
            "pagerank": 1.0, # PageRank score
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
