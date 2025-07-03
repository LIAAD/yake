"""
Multi-word term representation module for YAKE keyword extraction.

This module contains the ComposedWord class which represents multi-word terms
(potential keyword phrases) in a document. It handles the aggregation of features
from individual terms, scoring of candidate phrases, and validation to determine
which phrases make good keyword candidates.
"""

import numpy as np
import jellyfish
from .utils import STOPWORD_WEIGHT


class ComposedWord:
    """
    Representation of a multi-word term in the document.

    This class stores and aggregates information about multi-word keyword candidates,
    calculating combined scores from the properties of their constituent terms.
    It tracks statistics like term frequency, integrity, and provides methods to
    validate whether a phrase is likely to be a good keyword.

    Attributes:
        See property accessors below for available attributes.
    """

    def __init__(self, terms):
        """
        Initialize a ComposedWord object representing a multi-word term.

        Args:
            terms (list): List of tuples (tag, word, term_obj) representing
                          the individual words in this phrase. Can be None to
                          initialize an invalid candidate.
        """
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
        """Get the set of part-of-speech tag sequences for this phrase."""
        return self.data["tags"]

    @property
    def kw(self):
        """Get the original form of the keyword phrase."""
        return self.data["kw"]

    @property
    def unique_kw(self):
        """Get the normalized (lowercase) form of the keyword phrase."""
        return self.data["unique_kw"]

    @property
    def size(self):
        """Get the number of words in this phrase."""
        return self.data["size"]

    @property
    def terms(self):
        """Get the list of SingleWord objects for each constituent term."""
        return self.data["terms"]

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
    def integrity(self):
        """Get the integrity score indicating phrase coherence."""
        return self.data["integrity"]

    @property
    def h(self):
        """Get the final relevance score of this phrase (lower is better)."""
        return self.data["h"]

    @h.setter
    def h(self, value):
        """
        Set the final relevance score of this phrase.

        Args:
            value (float): The new score value
        """
        self.data["h"] = value

    @property
    def start_or_end_stopwords(self):
        """Get whether this phrase starts or ends with stopwords."""
        return self.data["start_or_end_stopwords"]

    def uptade_cand(self, cand):
        """
        Update this candidate with data from another candidate.

        Merges tag information from another candidate representing
        the same keyword phrase.

        Args:
            cand (ComposedWord): Another instance of the same keyword to merge with
        """
        # Add all tags from the other candidate to this one's tags
        for tag in cand.tags:
            self.tags.add(tag)

    def is_valid(self):
        """
        Check if this candidate is a valid keyword phrase.

        A valid keyword phrase doesn't contain unusual characters or digits,
        and doesn't start or end with stopwords.

        Returns:
            bool: True if this is a valid keyword candidate, False otherwise
        """
        is_valid = False
        # Check that at least one tag sequence has no unusual characters or digits
        for tag in self.tags:
            is_valid = is_valid or ("u" not in tag and "d" not in tag)

        # A valid keyword cannot start or end with a stopword
        return is_valid and not self.start_or_end_stopwords

    def get_composed_feature(self, feature_name, discart_stopword=True):
        """
               Get composed feature values for the n-gram.

        This function aggregates a specific feature across all terms in the n-gram.
        It computes the sum, product, and ratio of the feature values, optionally
        excluding stopwords from the calculation.

        Args:
            feature_name: Name of feature to get (must be an attribute of the term objects)
            discard_stopword: Whether to exclude stopwords from calculation (True by default)

        Returns:
            Tuple of (sum, product, ratio) for the feature where:
            - sum: Sum of the feature values across all relevant terms
            - product: Product of the feature values across all relevant terms
            - ratio: Product divided by (sum + 1), a measure of feature consistency

        """
        # Get feature values from each term, filtering stopwords if requested
        list_of_features = [
            getattr(term, feature_name)
            for term in self.terms
            if (discart_stopword and not term.stopword) or not discart_stopword
        ]

        # Calculate aggregate statistics
        sum_f = sum(list_of_features)
        prod_f = np.prod(list_of_features)

        # Return the three aggregated values
        return (sum_f, prod_f, prod_f / (sum_f + 1))

    def build_features(self, params):
        """
        Build features for machine learning or evaluation.

        Generates feature vectors that can be used for model training,
        evaluation, or visualization of keyword properties.

        Args:
            params (dict): Parameters for feature generation including:
                - features (list): Features to include
                - _stopword (list): Whether to consider stopwords [True, False]
                - doc_id (str): Document identifier
                - keys (list): Gold standard keywords for evaluation
                - rel (bool): Whether to include relevance feature
                - rel_approx (bool): Whether to include approximate relevance
                - is_virtual (bool): Whether this is a virtual candidate

        Returns:
            tuple: (features_list, column_names, matched_gold_standards)
        """
        # Get feature configuration from parameters
        features = params.get(
            "features", ["wfreq", "wrel", "tf", "wcase", "wpos", "wspread"]
        )
        _stopword = params.get("_stopword", [True, False])

        # Use defaults if not provided
        if features is None:
            features = ["wfreq", "wrel", "tf", "wcase", "wpos", "wspread"]
        if _stopword is None:
            _stopword = [True, False]

        # Initialize feature collection
        columns = []
        features_cand = []
        seen = set()

        # Add document identifier if provided
        if params.get("doc_id") is not None:
            columns.append("doc_id")
            features_cand.append(params["doc_id"])

        # Add gold standard match features if keys are provided
        if params.get("keys") is not None:
            # Exact match feature
            if params.get("rel", True):
                columns.append("rel")
                if self.unique_kw in params["keys"] or params.get("is_virtual", False):
                    features_cand.append(1)
                    seen.add(self.unique_kw)
                else:
                    features_cand.append(0)

            # Approximate match feature using string similarity
            if params.get("rel_approx", True):
                columns.append("rel_approx")
                max_gold_ = ("", 0.0)
                for gold_key in params["keys"]:
                    # Calculate normalized Levenshtein similarity
                    dist = 1.0 - jellyfish.levenshtein_distance(
                        gold_key,
                        self.unique_kw,
                    ) / max(len(gold_key), len(self.unique_kw))
                    max_gold_ = (gold_key, dist)
                features_cand.append(max_gold_[1])
                features_cand.append(max_gold_[1])

        # Add basic candidate properties
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

        # Add all requested features with different stopword handling
        for feature_name in features:
            for discart_stopword in _stopword:
                # Calculate aggregate feature metrics
                (f_sum, f_prod, f_sum_prod) = self.get_composed_feature(
                    feature_name, discart_stopword=discart_stopword
                )

                # Add sum feature
                columns.append(
                    f"{'n' if discart_stopword else ''}s_sum_K{feature_name}"
                )
                features_cand.append(f_sum)

                # Add product feature
                columns.append(
                    f"{'n' if discart_stopword else ''}s_prod_K{feature_name}"
                )
                features_cand.append(f_prod)

                # Add sum-product feature
                columns.append(
                    f"{'n' if discart_stopword else ''}s_sum_prod_K{feature_name}"
                )
                features_cand.append(f_sum_prod)

        return (features_cand, columns, seen)

    def update_h(self, features=None, is_virtual=False):
        """
        Update the term's score based on its constituent terms.

        Calculates a combined relevance score for the multi-word term by
        aggregating scores of its constituent words, with special handling for
        stopwords to improve keyword quality.

        Args:
            features (list, optional): Specific features to use for scoring
            is_virtual (bool): Whether this is a virtual candidate not in text
        """
        sum_h = 0.0
        prod_h = 1.0
        t = 0

        # Process each term in the phrase
        while t < len(self.terms):
            term_base = self.terms[t]
            # Handle non-stopwords directly
            if not term_base.stopword:
                sum_h += term_base.h
                prod_h *= term_base.h

            # Handle stopwords according to configured weight method
            else:
                if STOPWORD_WEIGHT == "bi":
                    # BiWeight: use probabilities of adjacent term connections

                    # If multiple stopwords in a row, treat as a group
                    stop_group_start = t
                    stop_group_end = t

                    while stop_group_end + 1 < len(self.terms) and self.terms[stop_group_end + 1].stopword:
                        stop_group_end += 1

                    # Adjacent probability of first stopword to previous term
                    prob_t1 = 0.0
                    # Check connection with previous term
                    if stop_group_start > 0 and term_base.g.has_edge(
                            self.terms[stop_group_start - 1].id, self.terms[stop_group_start].id
                    ):
                        prob_t1 = (
                                term_base.g[self.terms[stop_group_start - 1].id][self.terms[stop_group_start].id]["tf"]
                                / self.terms[stop_group_start - 1].tf
                        )

                    # Adjacent probability of last stopword to next term
                    prob_t2 = 0.0
                    # Check connection with next term
                    if stop_group_end < len(self.terms) - 1 and term_base.g.has_edge(
                            self.terms[stop_group_end].id, self.terms[stop_group_end + 1].id
                    ):
                        prob_t2 = (
                                term_base.g[self.terms[stop_group_end].id][self.terms[stop_group_end + 1].id]["tf"]
                                / self.terms[stop_group_end + 1].tf
                        )

                    # Calculate combined probability and update scores
                    prob = prob_t1 * prob_t2
                    prod_h *= 1 + (1 - prob)
                    sum_h -= 1 - prob

                    t = stop_group_end
                elif STOPWORD_WEIGHT == "h":
                    # HWeight: treat stopwords like normal words
                    sum_h += term_base.h
                    prod_h *= term_base.h
                elif STOPWORD_WEIGHT == "none":
                    # None: ignore stopwords entirely
                    pass

            t += 1

        # Determine term frequency to use in scoring
        tf_used = 1.0
        if features is None or "KPF" in features:
            tf_used = self.tf

        # For virtual candidates, use mean frequency of constituent terms
        if is_virtual:
            tf_used = np.mean([term_obj.tf for term_obj in self.terms])

        # Calculate final score (lower is better)
        self.h = prod_h / ((sum_h + 1) * tf_used)

    def update_h_old(self, features=None, is_virtual=False):
        """
        Legacy method for updating the term's score.

        Preserved for backward compatibility but uses a slightly different
        approach to calculate scores.

        Args:
            features (list, optional): Specific features to use for scoring
            is_virtual (bool): Whether this is a virtual candidate not in text
        """
        sum_h = 0.0
        prod_h = 1.0

        # Process each term in the phrase
        for t, term_base in enumerate(self.terms):
            # Skip terms with zero frequency in virtual candidates
            if is_virtual and term_base.tf == 0:
                continue

            # Handle stopwords with probability-based weighting
            if term_base.stopword:
                # Calculate probability of co-occurrence with previous term
                prob_t1 = 0.0
                if term_base.g.has_edge(self.terms[t - 1].id, self.terms[t].id):
                    prob_t1 = (
                        term_base.g[self.terms[t - 1].id][self.terms[t].id]["tf"]
                        / self.terms[t - 1].tf
                    )

                # Calculate probability of co-occurrence with next term
                prob_t2 = 0.0
                if term_base.g.has_edge(self.terms[t].id, self.terms[t + 1].id):
                    prob_t2 = (
                        term_base.g[self.terms[t].id][self.terms[t + 1].id]["tf"]
                        / self.terms[t + 1].tf
                    )

                # Update scores based on combined probability
                prob = prob_t1 * prob_t2
                prod_h *= 1 + (1 - prob)
                sum_h -= 1 - prob
            else:
                # Handle normal words directly
                sum_h += term_base.h
                prod_h *= term_base.h

        # Determine term frequency to use in scoring
        tf_used = 1.0
        if features is None or "KPF" in features:
            tf_used = self.tf

        # For virtual candidates, use mean frequency of constituent terms
        if is_virtual:
            tf_used = np.mean([term_obj.tf for term_obj in self.terms])

        # Calculate final score (lower is better)
        self.h = prod_h / ((sum_h + 1) * tf_used)
