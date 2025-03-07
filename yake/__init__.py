# -*- coding: utf-8 -*-

"""Top-level package for yake."""

__author__ = """Arian Pasquali"""
__email__ = "arianpasquali@gmail.com"
__version__ = "0.5.0"

# flake8: noqa: F401
from yake.yake import KeywordExtractor
from yake.datacore import DataCore
from yake.ngrams import ComposedWord
from yake.terms import SingleWord
from yake.features import calculate_term_features
from yake.utils import load_stopwords, pre_filter
