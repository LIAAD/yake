# -*- coding: utf-8 -*-

"""YAKE: Yet Another Keyword Extractor - Main module."""

import logging
from typing import List, Tuple, Optional, Callable
from yake.Levenshtein import Levenshtein

# Import from our new modules
from yake.datacore import DataCore
from yake.utils import load_stopwords

logger = logging.getLogger(__name__)


class KeywordExtractor:
    """Extracts keywords from text using the YAKE algorithm."""

    def __init__(
        self,
        lan: str = "en",
        n: int = 3,
        dedup_lim: float = 0.9,
        dedup_func: str = "seqm",
        window_size: int = 1,
        top: int = 20,
        features: Optional[List[str]] = None,
        stopwords: Optional[List[str]] = None,
    ):
        """Initialize the keyword extractor.

        Args:
            lan: Language for stopwords selection
            n: Maximum n-gram size to consider
            dedup_lim: Deduplication threshold
            dedup_func: Deduplication function ('seqm', 'jaro', 'leve')
            window_size: Window size for feature extraction
            top: Maximum number of keywords to extract
            features: Features to use for keyword extraction
            stopwords: Custom stopwords list
        """
        self.lan = lan
        self.n = n
        self.top = top
        self.dedup_lim = dedup_lim
        self.features = features
        self.window_size = window_size

        # Load stopwords
        self.stopword_set = load_stopwords(lan, stopwords)

        # Set deduplication function
        self.dedup_function = self._select_dedup_function(dedup_func)

    def _select_dedup_function(self, dedup_func: str) -> Callable[[str, str], float]:
        """Select the appropriate deduplication function.

        Args:
            dedup_func: Name of deduplication function

        Returns:
            Callable that computes similarity between strings
        """
        if dedup_func.lower() in ("jaro_winkler", "jaro"):
            return self.jaro
        elif dedup_func.lower() in ("sequencematcher", "seqm"):
            return self.seqm
        else:
            return self.levs

    def jaro(self, cand1: str, cand2: str) -> float:
        """Calculate Jaro-Winkler similarity between candidates.

        Args:
            cand1: First candidate
            cand2: Second candidate

        Returns:
            Similarity score between 0 and 1
        """
        import jellyfish

        return jellyfish.jaro_winkler(cand1, cand2)

    def levs(self, cand1: str, cand2: str) -> float:
        """Calculate Levenshtein similarity between candidates.

        Args:
            cand1: First candidate
            cand2: Second candidate

        Returns:
            Similarity score between 0 and 1
        """
        distance = Levenshtein.distance(cand1, cand2)
        return 1.0 - distance / max(len(cand1), len(cand2))

    def seqm(self, cand1: str, cand2: str) -> float:
        """Calculate Sequence Matcher similarity between candidates.

        Args:
            cand1: First candidate
            cand2: Second candidate

        Returns:
            Similarity score between 0 and 1
        """
        return Levenshtein.ratio(cand1, cand2)

    def extract_keywords(self, text: Optional[str]) -> List[Tuple[str, float]]:
        """Extract keywords from the given text.
        
        This function implements the complete YAKE keyword extraction pipeline:
        
        1. Preprocesses the input text by normalizing whitespace
        2. Builds a data representation using DataCore, which:
           - Tokenizes the text into sentences and words
           - Identifies candidate n-grams (1 to n words)
           - Creates a graph of term co-occurrences
        3. Extracts statistical features for single terms and n-grams
           - For single terms: frequency, position, case, etc.
           - For n-grams: combines features from constituent terms
        4. Filters candidates based on validity criteria (e.g., no stopwords at boundaries)
        5. Sorts candidates by their importance score (H), where lower is better
        6. Performs deduplication to remove similar candidates based on string similarity
        7. Returns the top k keywords with their scores
        
        The algorithm favors keywords that are statistically important but not common
        stopwords, with scores reflecting their estimated relevance to the document.
        Lower scores indicate more important keywords.

        Args:
            text: Input text

        Returns:
            List of (keyword, score) tuples sorted by score (lower is better)
        """
        if not text:
            return []

        try:
            # Preprocess text
            text = text.replace("\n\t", " ")

            # Build data representation
            dc = DataCore(
                text=text,
                stopword_set=self.stopword_set,
                windowsSize=self.window_size,
                n=self.n,
            )

            # Extract features
            dc.build_single_terms_features(features=self.features)
            dc.build_mult_terms_features(features=self.features)

            # Filter and sort candidates
            valid_candidates = [cc for cc in dc.candidates.values() if cc.is_valid()]
            sorted_candidates = sorted(valid_candidates, key=lambda c: c.H)

            # Skip deduplication if threshold is high enough
            if self.dedup_lim >= 1.0:
                return [(cand.unique_kw, cand.H) for cand in sorted_candidates][
                    : self.top
                ]

            # Deduplicate candidates
            result_set = []
            for cand in sorted_candidates:
                should_add = True
                for _, existing_cand in result_set:
                    similarity = self.dedup_function(
                        cand.unique_kw, existing_cand.unique_kw
                    )
                    if similarity > self.dedup_lim:
                        should_add = False
                        break

                if should_add:
                    result_set.append((cand.H, cand))

                if len(result_set) == self.top:
                    break

            return [(cand.unique_kw, h) for (h, cand) in result_set]

        except Exception as e:
            logger.warning(
                f"Exception: {e} generated by the following text: '{text[:100]}...'"
            )
            return []
