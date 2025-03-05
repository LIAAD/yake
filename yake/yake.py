"""Module for keyword extraction from text documents."""

import os
import jellyfish
from .Levenshtein import Levenshtein
from .datarepresentation import DataCore

class KeywordExtractor:
    """Class to extract and process keywords from text."""

    def __init__(self, **kwargs):
        """Initialize the KeywordExtractor with configuration parameters."""
        self.config = {
            "lan": kwargs.get("lan", "en"),
            "n": kwargs.get("n", 3),
            "dedup_lim": kwargs.get("dedup_lim", 0.9),
            "dedup_func": kwargs.get("dedup_func", "seqm"),
            "window_size": kwargs.get("window_size", 1),
            "top": kwargs.get("top", 20),
            "features": kwargs.get("features", None),
        }

        self.stopword_set = self._load_stopwords(kwargs.get("stopwords"))
        self.dedup_function = self._get_dedup_function(self.config["dedup_func"])

    def _load_stopwords(self, stopwords):
        """Load stopwords from file or use provided set."""
        if stopwords is not None:
            return set(stopwords)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        local_path = os.path.join(
            "StopwordsList", f"stopwords_{self.config['lan'][:2].lower()}.txt"
        )

        if not os.path.exists(os.path.join(dir_path, local_path)):
            local_path = os.path.join("StopwordsList", "stopwords_noLang.txt")

        resource_path = os.path.join(dir_path, local_path)

        try:
            with open(resource_path, encoding="utf-8") as stop_file:
                return set(stop_file.read().lower().split("\n"))
        except UnicodeDecodeError:
            print("Warning: reading stopword list as ISO-8859-1")
            with open(resource_path, encoding="ISO-8859-1") as stop_file:
                return set(stop_file.read().lower().split("\n"))

    def _get_dedup_function(self, func_name):
        """Retrieve the appropriate deduplication function."""
        return {
            "jaro_winkler": self.jaro,
            "jaro": self.jaro,
            "sequencematcher": self.seqm,
            "seqm": self.seqm,
        }.get(func_name.lower(), self.levs)

    def jaro(self, cand1, cand2):
        return jellyfish.jaro_winkler(cand1, cand2)

    def levs(self, cand1, cand2):
        return 1 - Levenshtein.distance(cand1, cand2) / max(len(cand1), len(cand2))

    def seqm(self, cand1, cand2):
        return Levenshtein.ratio(cand1, cand2)

    def extract_keywords(self, text):
        """Extract keywords from text."""
        if not text:
            return []

        text = text.replace("\n", " ")
        dc = DataCore(
            text=text,
            stopword_set=self.stopword_set,
            windows_size=self.config["window_size"],
            n=self.config["n"],
        )

        dc.build_single_terms_features(features=self.config["features"])
        dc.build_mult_terms_features(features=self.config["features"])

        result_set = []
        candidates_sorted = sorted(
            [cc for cc in dc.candidates.values() if cc.is_valid()], key=lambda c: c.h
        )

        if self.config["dedup_lim"] >= 1.0:
            return [(cand.unique_kw, cand.h) for cand in candidates_sorted][: self.config["top"]]

        for cand in candidates_sorted:
            should_add = True
            for (h, cand_result) in result_set:
                if self.dedup_function(
                    cand.unique_kw, cand_result.unique_kw) > self.config["dedup_lim"]:
                    should_add = False
                    break

            if should_add:
                result_set.append((cand.h, cand))
            if len(result_set) == self.config["top"]:
                break

        return [(cand.kw, h) for (h, cand) in result_set]
