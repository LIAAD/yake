"""Module for keyword extraction from text documents."""

import os
import jellyfish
from .Levenshtein import Levenshtein
from .datarepresentation import DataCore


class KeywordExtractor:
    """Class to extract and process keywords from text."""

    def __init__(self, config):
        """Initialize the KeywordExtractor with the given parameters.

        Args:
            config (dict): Dictionary containing configuration parameters.
        """
        self.lan = config.get("lan", "en")
        self.n = config.get("n", 3)
        self.top = config.get("top", 20)
        self.dedup_lim = config.get("dedup_lim", 0.9)
        self.window_size = config.get("window_size", 1)
        self.features = config.get("features", None)
        self.stopword_set = self.load_stopwords(config.get("stopwords", None))

        dedup_func = config.get("dedup_func", "seqm").lower()
        self.dedup_function = {
            "jaro_winkler": self.jaro,
            "jaro": self.jaro,
            "sequencematcher": self.seqm,
            "seqm": self.seqm
        }.get(dedup_func, self.levs)

    def load_stopwords(self, stopwords):
        """Load stopwords from a file or use provided set."""
        if stopwords is not None:
            return set(stopwords)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        stopwords_path = os.path.join("StopwordsList", f"stopwords_{self.lan[:2].lower()}.txt")
        
        if not os.path.exists(os.path.join(dir_path, stopwords_path)):
            stopwords_path = os.path.join("StopwordsList", "stopwords_noLang.txt")

        resource_path = os.path.join(dir_path, stopwords_path)
        
        try:
            with open(resource_path, encoding="utf-8") as stop_file:
                return set(stop_file.read().lower().split("\n"))
        except UnicodeDecodeError:
            print("Warning: reading stopword list as ISO-8859-1")
            with open(resource_path, encoding="ISO-8859-1") as stop_file:
                return set(stop_file.read().lower().split("\n"))

    def jaro(self, cand1, cand2):
        """Calculate Jaro-Winkler distance between candidates."""
        return jellyfish.jaro_winkler(cand1, cand2)

    def levs(self, cand1, cand2):
        """Calculate normalized Levenshtein distance."""
        distance = Levenshtein.distance(cand1, cand2)
        return 1 - distance / max(len(cand1), len(cand2))

    def seqm(self, cand1, cand2):
        """Calculate sequence matcher ratio."""
        return Levenshtein.ratio(cand1, cand2)

    def extract_keywords(self, text):
        """Extract keywords from the given text.

        Args:
            text (str): Input text to extract keywords from

        Returns:
            list: List of tuples containing (keyword, score)
        """
        if not text:
            return []

        text = text.replace("\n", " ")
        dc = DataCore(
            text=text,
            stopword_set=self.stopword_set,
            windows_size=self.window_size,
            n=self.n,
        )

        dc.build_single_terms_features(features=self.features)
        dc.build_mult_terms_features(features=self.features)

        result_set = []
        candidates_sorted = sorted(
            [cc for cc in dc.candidates.values() if cc.is_valid()],
            key=lambda c: c.h
        )

        if self.dedup_lim >= 1.0:
            return [(cand.unique_kw, cand.h) for cand in candidates_sorted][:self.top]

        for cand in candidates_sorted:
            if all(self.dedup_function(cand.unique_kw, cand_result.unique_kw) <= self.dedup_lim
                   for _, cand_result in result_set):
                result_set.append((cand.h, cand))
                if len(result_set) == self.top:
                    break

        return [(cand.kw, h) for h, cand in result_set]
