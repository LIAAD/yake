from typing import Sequence
import numpy as np


class Levenshtein:
    """Implements the Levenshtein distance and similarity ratio."""

    @staticmethod
    def ratio(seq1: Sequence, seq2: Sequence) -> float:
        """Calculate the similarity ratio between two sequences.

        This function computes a normalized similarity measure between two sequences
        based on their Levenshtein distance. The ratio is calculated as 1 minus the
        Levenshtein distance divided by the length of the longer sequence. A ratio of 1.0
        indicates identical sequences, while a ratio closer to 0.0 indicates more dissimilar
        sequences.

        Args:
            seq1: First sequence to compare
            seq2: Second sequence to compare

        Returns:
            Similarity ratio between 0.0 and 1.0, where:
            - 1.0 means the sequences are identical
            - 0.0 means the sequences are completely different
            - Values in between represent partial similarity
        """
        distance = Levenshtein.distance(seq1, seq2)
        length = max(len(seq1), len(seq2))

        # Avoid division by zero
        if length == 0:
            return 1.0

        return 1.0 - float(distance) / float(length)

    @staticmethod
    def distance(seq1: Sequence, seq2: Sequence) -> int:
        """Calculate the Levenshtein distance between two sequences.

        This function computes the minimum number of single-character edits (insertions,
        deletions, or substitutions) required to change one sequence into another. It uses
        a dynamic programming approach with a matrix to track the minimum edit distance
        at each step of the comparison.

        Args:
            seq1: First sequence to compare
            seq2: Second sequence to compare

        Returns:
            Edit distance as an integer representing the minimum number of operations
            needed to transform seq1 into seq2. A distance of 0 means the sequences
            are identical.
        """
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1

        # Initialize the distance matrix
        matrix = np.zeros((size_x, size_y), dtype=int)

        # Initialize first row and column
        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y

        # Fill the matrix
        for x in range(1, size_x):
            for y in range(1, size_y):
                cost = 0 if seq1[x - 1] == seq2[y - 1] else 1
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,  # deletion
                    matrix[x, y - 1] + 1,  # insertion
                    matrix[x - 1, y - 1] + cost,  # substitution
                )

        return int(matrix[size_x - 1, size_y - 1])
