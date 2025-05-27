"""
Module providing Levenshtein distance and ratio calculations.

This module implements the Levenshtein (edit distance) algorithm for measuring
the difference between two strings. It provides both a raw distance calculation
and a normalized similarity ratio, which are useful for comparing text strings
and identifying potential matches with slight variations.
"""

import numpy as np


class Levenshtein:
    """
    Class for computing Levenshtein distance and similarity ratio.

    This class provides static methods to calculate the edit distance between
    strings (how many insertions, deletions, or substitutions are needed to
    transform one string into another) and to determine a normalized similarity
    ratio between them.

    These metrics are widely used in fuzzy string matching, spell checking,
    and approximate text similarity measurements.
    """

    @staticmethod
    def __ratio(distance: float, str_length: int) -> float:
        """
        Calculate the similarity ratio based on distance and string length.

        This method normalizes the Levenshtein distance into a similarity ratio
        between 0 and 1, where 1 represents identical strings and 0 represents
        completely different strings.

        Args:
            distance (float): The Levenshtein distance between two strings.
            str_length (int): The length of the longer string.

        Returns:
            float: The similarity ratio, where higher values indicate greater similarity.
                  The range is [0.0, 1.0] where 1.0 means identical strings.
        """
        return 1 - float(distance) / float(str_length)

    @staticmethod
    def ratio(seq1: str, seq2: str) -> float:
        """
        Compute the similarity ratio between two strings.

        This is the main method for determining string similarity. It calculates
        the Levenshtein distance and then converts it to a ratio representing
        how similar the strings are.

        Args:
            seq1 (str): The first string to compare.
            seq2 (str): The second string to compare.

        Returns:
            float: The similarity ratio between the two strings, ranging from 0.0
                  (completely different) to 1.0 (identical).
        """
        str_distance = Levenshtein.distance(seq1, seq2)
        str_length = max(len(seq1), len(seq2))
        return Levenshtein.__ratio(str_distance, str_length)

    @staticmethod
    def distance(seq1: str, seq2: str) -> int:
        """
        Calculate the Levenshtein distance between two strings.

        This method implements the core Levenshtein algorithm, which calculates
        the minimum number of single-character edits (insertions, deletions, or
        substitutions) required to change one string into another.

        The algorithm uses dynamic programming with a matrix approach to efficiently
        compute the minimum edit distance.

        Args:
            seq1 (str): The first string to compare.
            seq2 (str): The second string to compare.

        Returns:
            int: The Levenshtein distance - the minimum number of edit operations
                 required to transform seq1 into seq2.
        """
        # Create a matrix of size (len(seq1)+1) x (len(seq2)+1)
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))

        # Initialize the first row and column of the matrix
        for x in range(size_x):
            matrix[x, 0] = x  # Cost of deleting characters from seq1
        for y in range(size_y):
            matrix[0, y] = y  # Cost of inserting characters from seq2

        # Fill the matrix using dynamic programming approach
        for x in range(1, size_x):
            for y in range(1, size_y):
                # Check if the characters at current positions match
                if seq1[x - 1] == seq2[y - 1]:
                    cost = 0  # No cost for matching characters
                else:
                    cost = 1  # Cost of 1 for substitution

                # Calculate minimum cost among deletion, insertion, and substitution
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,  # Deletion (remove from seq1)
                    matrix[x, y - 1] + 1,  # Insertion (add from seq2)
                    matrix[x - 1, y - 1] + cost,  # Substitution or match
                )

        # Return the bottom-right value of the matrix as the final distance
        return int(matrix[size_x - 1, size_y - 1])
