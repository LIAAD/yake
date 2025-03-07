import numpy as np
from yake.Levenshtein import Levenshtein

STOPWORD_WEIGHT = "bi"


class ComposedWord:
    """Represents a composed word (n-gram) in the text."""

    def __init__(self, terms):
        """Initialize a composed word.

        Args:
            terms: List of (tag, word, term_obj) tuples
        """
        if terms is None:
            self.start_or_end_stopwords = True
            self.tags = set()
            return

        self.tags = set(["".join(w[0] for w in terms)])
        self.kw = " ".join(w[1] for w in terms)
        self.unique_kw = self.kw.lower()
        self.size = len(terms)
        self.terms = [w[2] for w in terms if w[2] is not None]
        self.tf = 0.0
        self.integrity = 1.0
        self.H = 1.0
        self.start_or_end_stopwords = self.terms[0].stopword or self.terms[-1].stopword

    def update_cand(self, cand):
        """Update candidate with new tags.

        Args:
            cand: Candidate to update from
        """
        self.tags.update(cand.tags)

    def is_valid(self):
        """Check if candidate is valid.

        Returns:
            True if valid, False otherwise
        """
        return (
            any("u" not in tag and "d" not in tag for tag in self.tags)
            and not self.start_or_end_stopwords
        )

    def get_composed_feature(self, feature_name, discard_stopword=True):
        """Get composed feature values for the n-gram.

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
        list_of_features = [
            getattr(term, feature_name)
            for term in self.terms
            if not discard_stopword or not term.stopword
        ]

        sum_f = sum(list_of_features)
        prod_f = np.prod(list_of_features)
        return (sum_f, prod_f, prod_f / (sum_f + 1))

    def build_features(
        self,
        doc_id=None,
        keys=None,
        rel=True,
        rel_approx=True,
        is_virtual=False,
        features=None,
        _stopword=None,
    ):
        """Build features for the composed word.

        Args:
            Various feature extraction parameters

        Returns:
            Tuple of features, columns, and set of seen keywords
        """
        if features is None:
            features = ["WFreq", "WRel", "tf", "WCase", "WPos", "WSpread"]
        if _stopword is None:
            _stopword = [True, False]

        columns = []
        seen = set()
        features_cand = []

        if doc_id is not None:
            columns.append("doc_id")
            features_cand.append(doc_id)

        if keys is not None:
            if rel:
                columns.append("rel")
                if self.unique_kw in keys or is_virtual:
                    features_cand.append(1)
                    seen.add(self.unique_kw)
                else:
                    features_cand.append(0)

            if rel_approx:
                columns.append("rel_approx")
                max_gold_ = ("", 0.0)
                for gold_key in keys:
                    dist = 1.0 - Levenshtein(gold_key, self.unique_kw) / max(
                        len(gold_key), len(self.unique_kw)
                    )
                    if max_gold_[1] < dist:
                        max_gold_ = (gold_key, dist)
                features_cand.append(max_gold_[1])

        # Add basic features
        columns.append("kw")
        features_cand.append(self.unique_kw)
        columns.append("h")
        features_cand.append(self.H)
        columns.append("tf")
        features_cand.append(self.tf)
        columns.append("size")
        features_cand.append(self.size)
        columns.append("isVirtual")
        features_cand.append(int(is_virtual))

        # Add composite features
        for feature_name in features:
            for discard_stopword in _stopword:
                prefix = "n" if discard_stopword else ""
                f_sum, f_prod, f_sum_prod = self.get_composed_feature(
                    feature_name, discard_stopword=discard_stopword
                )

                columns.append(f"{prefix}s_sum_K{feature_name}")
                features_cand.append(f_sum)

                columns.append(f"{prefix}s_prod_K{feature_name}")
                features_cand.append(f_prod)

                columns.append(f"{prefix}s_sum_prod_K{feature_name}")
                features_cand.append(f_sum_prod)

        return (features_cand, columns, seen)

    def update_h(self, features=None, is_virtual=False):
        """Update the H score for the composed word.

        Args:
            features: Features to use
            is_virtual: Whether this is a virtual candidate
        """
        sum_h = 0.0
        prod_h = 1.0

        for t, term_base in enumerate(self.terms):
            if not term_base.stopword:
                sum_h += term_base.H
                prod_h *= term_base.H
            else:
                if STOPWORD_WEIGHT == "bi":
                    prob_t1 = prob_t2 = 0.0

                    # Check if terms exist at t-1 and t
                    if t > 0 and term_base.G.has_edge(
                        self.terms[t - 1].id, term_base.id
                    ):
                        prob_t1 = (
                            term_base.G[self.terms[t - 1].id][term_base.id]["TF"]
                            / self.terms[t - 1].tf
                        )

                    # Check if terms exist at t and t+1
                    if t < len(self.terms) - 1 and term_base.G.has_edge(
                        term_base.id, self.terms[t + 1].id
                    ):
                        prob_t2 = (
                            term_base.G[term_base.id][self.terms[t + 1].id]["TF"]
                            / self.terms[t + 1].tf
                        )

                    prob = prob_t1 * prob_t2
                    prod_h *= 1 + (1 - prob)
                    sum_h -= 1 - prob
                elif STOPWORD_WEIGHT == "h":
                    sum_h += term_base.H
                    prod_h *= term_base.H
                # If STOPWORD_WEIGHT is 'none', do nothing

        tf_used = 1.0
        if features is None or "KPF" in features:
            tf_used = self.tf

        if is_virtual:
            tf_used = np.mean([term_obj.tf for term_obj in self.terms])

        self.H = prod_h / ((sum_h + 1) * tf_used)
