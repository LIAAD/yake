"""Data representation module for keyword extraction!"""

from .core import DataCore
from .single_word import SingleWord
from .composed_word import ComposedWord

__all__ = ["DataCore", "SingleWord", "ComposedWord"]
