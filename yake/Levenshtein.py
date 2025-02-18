"""Module providing Levenshtein distance and ratio calculations."""

import numpy as np


class Levenshtein:
    """Class for computing Levenshtein distance and similarity ratio."""

    @staticmethod
    def __ratio(distance: float, str_length: int) -> float:
        """Calculate the similarity ratio based on distance and string length.

        Args:
            distance (float): The Levenshtein distance between two strings.
            str_length (int): The length of the longer string.

        Returns:
            float: The similarity ratio.
        """
        return 1 - float(distance) / float(str_length)

    @staticmethod
    def ratio(seq1: str, seq2: str) -> float:
        """Compute the similarity ratio between two strings.

        Args:
            seq1 (str): The first string.
            seq2 (str): The second string.

        Returns:
            float: The similarity ratio.
        """
        str_distance = Levenshtein.distance(seq1, seq2)
        str_length = max(len(seq1), len(seq2))
        return Levenshtein.__ratio(str_distance, str_length)

    @staticmethod
    def distance(seq1: str, seq2: str) -> int:
        """Calculate the Levenshtein distance between two strings.

        Args:
            seq1 (str): The first string.
            seq2 (str): The second string.

        Returns:
            int: The Levenshtein distance.
        """
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))

        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x - 1] == seq2[y - 1]:
                    cost = 0
                else:
                    cost = 1

                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,     # Deletion
                    matrix[x, y - 1] + 1,     # Insertion
                    matrix[x - 1, y - 1] + cost,  # Substitution
                )

        return int(matrix[size_x - 1, size_y - 1])
