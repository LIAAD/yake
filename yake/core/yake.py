"""
Keyword extraction module for YAKE.

This module provides the KeywordExtractor class which serves as the main entry point 
for the YAKE keyword extraction algorithm. It handles configuration, stopword loading,
deduplication of similar keywords, and the entire extraction pipeline from raw text 
to ranked keywords.
"""

import os
import jellyfish
from yake.data import DataCore
from .Levenshtein import Levenshtein


class KeywordExtractor:
    """
    Main entry point for YAKE keyword extraction.
    
    This class handles the configuration, preprocessing, and extraction of keywords
    from text documents using statistical features without relying on dictionaries
    or external corpora. It integrates components for text processing, candidate
    generation, feature extraction, and keyword ranking.
    
    Attributes:
        See initialization parameters for configurable attributes.
    """

    def __init__(self, **kwargs):
        """
        Initialize the KeywordExtractor with configuration parameters.
        
        Args:
            **kwargs: Configuration parameters including:
                lan (str): Language for stopwords (default: "en")
                n (int): Maximum n-gram size (default: 3)
                dedup_lim (float): Similarity threshold for deduplication (default: 0.9)
                dedup_func (str): Deduplication function: "seqm", "jaro", or "levs" (default: "seqm")
                window_size (int): Size of word window for co-occurrence (default: 1)
                top (int): Maximum number of keywords to extract (default: 20)
                features (list): List of features to use for scoring (default: None = all features)
                stopwords (set): Custom set of stopwords (default: None = use language-specific)
        """
        # Initialize configuration dictionary with default values
        self.config = {
            "lan": kwargs.get("lan", "en"),
            "n": kwargs.get("n", 3),
            "dedup_lim": kwargs.get("dedup_lim", 0.9),
            "dedup_func": kwargs.get("dedup_func", "seqm"),
            "window_size": kwargs.get("window_size", 1),
            "top": kwargs.get("top", 20),
            "features": kwargs.get("features", None),
        }

        # Load appropriate stopwords and deduplication function
        self.stopword_set = self._load_stopwords(kwargs.get("stopwords"))
        self.dedup_function = self._get_dedup_function(self.config["dedup_func"])

    def _load_stopwords(self, stopwords):
        """
        Load stopwords from file or use provided set.
        
        This method handles the loading of language-specific stopwords from
        the appropriate resource file, falling back to a language-agnostic
        list if the specific language is not available.
        
        Args:
            stopwords (set, optional): Custom set of stopwords to use
            
        Returns:
            set: A set of stopwords for filtering non-content words
        """
        # Use provided stopwords if available
        if stopwords is not None:
            return set(stopwords)

        # Determine the path to the appropriate stopword list
        dir_path = os.path.dirname(os.path.realpath(__file__))
        local_path = os.path.join(
            "StopwordsList", f"stopwords_{self.config['lan'][:2].lower()}.txt"
        )

        # Fall back to language-agnostic list if specific language not available
        if not os.path.exists(os.path.join(dir_path, local_path)):
            local_path = os.path.join("StopwordsList", "stopwords_noLang.txt")

        resource_path = os.path.join(dir_path, local_path)

        # Attempt to read the stopword file with UTF-8 encoding
        try:
            with open(resource_path, encoding="utf-8") as stop_file:
                return set(stop_file.read().lower().split("\n"))
        except UnicodeDecodeError:
            # Fall back to ISO-8859-1 encoding if UTF-8 fails
            print("Warning: reading stopword list as ISO-8859-1")
            with open(resource_path, encoding="ISO-8859-1") as stop_file:
                return set(stop_file.read().lower().split("\n"))

    def _get_dedup_function(self, func_name):
        """
        Retrieve the appropriate deduplication function.
        
        Maps the requested string similarity function name to the corresponding
        method implementation for keyword deduplication.
        
        Args:
            func_name (str): Name of the deduplication function to use
            
        Returns:
            function: Reference to the selected string similarity function
        """
        # Map function names to their implementations
        return {
            "jaro_winkler": self.jaro,
            "jaro": self.jaro,
            "sequencematcher": self.seqm,
            "seqm": self.seqm,
        }.get(func_name.lower(), self.levs)

    def jaro(self, cand1, cand2):
        """
        Calculate Jaro similarity between two strings.
        
        A string metric measuring edit distance between two sequences,
        with higher values indicating greater similarity.
        
        Args:
            cand1 (str): First string to compare
            cand2 (str): Second string to compare
            
        Returns:
            float: Similarity score between 0.0 (different) and 1.0 (identical)
        """
        return jellyfish.jaro(cand1, cand2)

    def levs(self, cand1, cand2):
        """
        Calculate normalized Levenshtein similarity between two strings.
        
        Computes the Levenshtein distance and normalizes it by the length
        of the longer string, returning a similarity score.
        
        Args:
            cand1 (str): First string to compare
            cand2 (str): Second string to compare
            
        Returns:
            float: Similarity score between 0.0 (different) and 1.0 (identical)
        """
        return 1 - Levenshtein.distance(cand1, cand2) / max(len(cand1), len(cand2))

    def seqm(self, cand1, cand2):
        """
        Calculate sequence matcher ratio between two strings.
        
        Uses the Levenshtein ratio which measures the similarity between
        two strings based on the minimum number of operations required
        to transform one string into the other.
        
        Args:
            cand1 (str): First string to compare
            cand2 (str): Second string to compare
            
        Returns:
            float: Similarity score between 0.0 (different) and 1.0 (identical)
        """
        return Levenshtein.ratio(cand1, cand2)

    def extract_keywords(self, text):
        """
        Extract keywords from text.
        
        This method implements the complete YAKE keyword extraction pipeline:
        1. Text preprocessing
        2. Term extraction and feature computation
        3. Candidate keyword generation
        4. Scoring and deduplication
        5. Ranking and selection of top keywords
        
        Args:
            text (str): The input text to extract keywords from
            
        Returns:
            list: A list of tuples (keyword, score) sorted by score (lower is better)
        """
        # Handle empty input
        if not text:
            return []

        # Normalize text by replacing newlines with spaces
        text = text.replace("\n", " ")

        # Create a configuration dictionary for DataCore
        core_config = {
            "windows_size": self.config["window_size"],
            "n": self.config["n"],
        }

        # Initialize the data core with the text
        dc = DataCore(text=text, stopword_set=self.stopword_set, config=core_config)

        # Build features for single terms and multi-word terms
        dc.build_single_terms_features(features=self.config["features"])
        dc.build_mult_terms_features(features=self.config["features"])

        # Collect and sort all valid candidates by score (lower is better)
        result_set = []
        candidates_sorted = sorted(
            [cc for cc in dc.candidates.values() if cc.is_valid()], key=lambda c: c.h
        )

        # If deduplication is disabled, return all candidates up to the limit
        if self.config["dedup_lim"] >= 1.0:
            return [(cand.unique_kw, cand.h) for cand in candidates_sorted][
                : self.config["top"]
            ]

        # Perform deduplication by comparing candidates
        for cand in candidates_sorted:
            should_add = True
            # Check if this candidate is too similar to any already selected
            for h, cand_result in result_set:
                if (
                    self.dedup_function(cand.unique_kw, cand_result.unique_kw)
                    > self.config["dedup_lim"]
                ):
                    should_add = False
                    break

            # Add candidate if it passes deduplication
            if should_add:
                result_set.append((cand.h, cand))

            # Stop once we have enough candidates
            if len(result_set) == self.config["top"]:
                break

        # Format results as (keyword, score) tuples
        return [(cand.kw, h) for (h, cand) in result_set]
