"""ComposedWord class for representing multi-word terms."""

import numpy as np
import jellyfish
from .utils import STOPWORD_WEIGHT

class ComposedWord:
    """Representation of a multi-word term in the document."""

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
        """Build features for machine learning or evaluation."""
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
