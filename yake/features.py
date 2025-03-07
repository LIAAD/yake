import numpy as np
import math

# Constants
STOPWORD_WEIGHT = "bi"


def calculate_term_features(
    term, max_tf, avg_tf, std_tf, number_of_sentences, features=None
):
    """Calculate features for a single term.

    This function computes various statistical features for a term that are used to 
    determine its importance as a potential keyword. The features include term relevance,
    frequency, spread across the document, case information, and position. These features
    are combined to calculate an overall importance score (H).

    Args:
        term: SingleWord object containing term information and statistics
        max_tf: Maximum term frequency in the document
        avg_tf: Average term frequency across all terms
        std_tf: Standard deviation of term frequency
        number_of_sentences: Total number of sentences in document
        features: List of features to calculate or None for all

    Returns:
        Dictionary of calculated features which may include:
        - WRel: Term relevance based on connection to other terms
        - WFreq: Normalized term frequency
        - WSpread: Term spread across document sentences
        - WCase: Case feature capturing capitalization patterns
        - WPos: Position feature based on median occurrence position
        - H: Overall importance score combining all features
        - Additional intermediate values like PL and PR (left/right probabilities)
    """
    result = {}

    # Calculate WRel feature (term relevance)
    if features is None or "WRel" in features:
        # Calculate left and right probabilities
        WDL = len(term.G.in_edges(term.id))
        WDR = len(term.G.out_edges(term.id))

        WIL = sum(d["TF"] for _, _, d in term.G.in_edges(term.id, data=True))
        WIR = sum(d["TF"] for _, _, d in term.G.out_edges(term.id, data=True))

        PWL = 0 if WIL == 0 else WDL / WIL
        PWR = 0 if WIR == 0 else WDR / WIR

        # Calculate probabilities
        PL = WDL / max_tf
        PR = WDR / max_tf

        # Calculate relevance
        WRel = (0.5 + (PWL * (term.tf / max_tf))) + (0.5 + (PWR * (term.tf / max_tf)))

        result["PL"] = PL
        result["PR"] = PR
        result["WRel"] = WRel

    # Calculate term frequency feature
    if features is None or "WFreq" in features:
        WFreq = term.tf / (avg_tf + std_tf)
        result["WFreq"] = WFreq

    # Calculate term spread feature
    if features is None or "WSpread" in features:
        WSpread = len(term.occurs) / number_of_sentences
        result["WSpread"] = WSpread

    # Calculate case feature (all caps/proper nouns)
    if features is None or "WCase" in features:
        WCase = max(term.tf_a, term.tf_n) / (1.0 + math.log(term.tf))
        result["WCase"] = WCase

    # Calculate position feature
    if features is None or "WPos" in features:
        WPos = math.log(math.log(3.0 + np.median(list(term.occurs.keys()))))
        result["WPos"] = WPos

    # Calculate H score if we have all required features
    required_features = {"WPos", "WRel", "WCase", "WFreq", "WSpread"}
    if all(f in result for f in required_features):
        H = (result["WPos"] * result["WRel"]) / (
            result["WCase"]
            + (result["WFreq"] / result["WRel"])
            + (result["WSpread"] / result["WRel"])
        )
        result["H"] = H

    return result


def calculate_composed_features(composed_word, features=None, is_virtual=False):
    """Calculate features for composed words (n-grams).

    This function computes features for multi-word expressions (n-grams) by combining
    the features of individual terms. It handles stopwords differently based on the
    STOPWORD_WEIGHT configuration. The function calculates an overall importance score (H)
    that considers the relationships between terms in the n-gram.

    Args:
        composed_word: ComposedWord object containing the n-gram information
        features: List of features to calculate or None for all
        is_virtual: Whether this is a virtual candidate (not directly observed in text)

    Returns:
        Dictionary with calculated features including:
        - H: Overall importance score for the n-gram
        - prod_h: Product of H scores of component terms
        - sum_h: Sum of H scores of component terms
        - tf_used: Term frequency used in calculations
    """
    result = {}

    # Initialize summation and product for H score
    sum_h = 0.0
    prod_h = 1.0

    # Process each term in the composed word
    for t, term_base in enumerate(composed_word.terms):
        if not term_base.stopword:
            # For non-stopwords, simply add/multiply H scores
            sum_h += term_base.H
            prod_h *= term_base.H
        else:
            # For stopwords, weight by connection probability
            if STOPWORD_WEIGHT == "bi":
                prob_t1 = prob_t2 = 0.0

                # Check if terms exist at t-1 and t
                if t > 0 and term_base.G.has_edge(
                    composed_word.terms[t - 1].id, term_base.id
                ):
                    prob_t1 = (
                        term_base.G[composed_word.terms[t - 1].id][term_base.id]["TF"]
                        / composed_word.terms[t - 1].tf
                    )

                # Check if terms exist at t and t+1
                if t < len(composed_word.terms) - 1 and term_base.G.has_edge(
                    term_base.id, composed_word.terms[t + 1].id
                ):
                    prob_t2 = (
                        term_base.G[term_base.id][composed_word.terms[t + 1].id]["TF"]
                        / composed_word.terms[t + 1].tf
                    )

                prob = prob_t1 * prob_t2
                prod_h *= 1 + (1 - prob)
                sum_h -= 1 - prob
            elif STOPWORD_WEIGHT == "h":
                # Alternative: include stopword's H value
                sum_h += term_base.H
                prod_h *= term_base.H
            # If STOPWORD_WEIGHT is 'none', do nothing

    # Determine term frequency to use
    tf_used = 1.0
    if features is None or "KPF" in features:
        tf_used = composed_word.tf

    # For virtual candidates, use mean term frequency
    if is_virtual:
        tf_used = np.mean([term_obj.tf for term_obj in composed_word.terms])

    # Calculate final H score
    H = prod_h / ((sum_h + 1) * tf_used)
    result["H"] = H

    # Add derived features
    result["prod_h"] = prod_h
    result["sum_h"] = sum_h
    result["tf_used"] = tf_used

    return result


def get_composed_feature(composed_word, feature_name, discard_stopword=True):
    """Calculate combined metrics for a feature across all terms in a composed word.

    This function aggregates a specific feature across all terms in a multi-word expression.
    It computes the sum, product, and ratio of the feature values, optionally excluding
    stopwords from the calculation.

    Args:
        composed_word: ComposedWord object containing the n-gram information
        feature_name: Name of the feature to compose (must be an attribute of the term objects)
        discard_stopword: Whether to exclude stopwords from calculation (True by default)

    Returns:
        Tuple of (sum, product, ratio) for the feature where:
        - sum: Sum of the feature values across all relevant terms
        - product: Product of the feature values across all relevant terms
        - ratio: Product divided by (sum + 1), a measure of feature consistency
    """
    list_of_features = [
        getattr(term, feature_name)
        for term in composed_word.terms
        if not discard_stopword or not term.stopword
    ]

    if not list_of_features:
        return (0, 0, 0)

    sum_f = sum(list_of_features)
    prod_f = np.prod(list_of_features)

    # Calculate ratio, avoiding division by zero
    ratio = prod_f / (sum_f + 1)

    return (sum_f, prod_f, ratio)


def apply_features_to_term(term, features):
    """Apply calculated features to a SingleWord object.

    This function takes a dictionary of calculated features and sets them as attributes
    on the provided term object, making the features accessible directly from the term.

    Args:
        term: SingleWord object to update with feature values
        features: Dictionary of features from calculate_term_features
    """
    for feature_name, value in features.items():
        setattr(term, feature_name, value)


def apply_features_to_composed_word(composed_word, features):
    """Apply calculated features to a ComposedWord object.

    This function takes a dictionary of calculated features and sets the main H score
    as an attribute on the provided composed word object. Unlike apply_features_to_term,
    this function only sets the H score, not all features.

    Args:
        composed_word: ComposedWord object to update with feature values
        features: Dictionary of features from calculate_composed_features
    """
    for feature_name, value in features.items():
        if feature_name == "H":  # Only set the main H score
            composed_word.H = value
