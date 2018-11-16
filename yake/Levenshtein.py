import numpy as np

class Levenshtein(object):

    @staticmethod
    def __ratio(distance, str_length):
        return 1 - float(distance) / float(str_length)

    @staticmethod
    def ratio(seq1, seq2):
        str_distance = Levenshtein.distance(seq1,seq2)
        str_length = max(len(seq1),len(seq2))
        return Levenshtein.__ratio(str_distance,str_length)

    @staticmethod
    def distance(seq1, seq2):  
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros ((size_x, size_y))
        for x in range(size_x):
            matrix [x, 0] = x
        for y in range(size_y):
            matrix [0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x-1] == seq2[y-1]:
                    matrix [x,y] = min(
                        matrix[x-1, y] + 1,
                        matrix[x-1, y-1],
                        matrix[x, y-1] + 1
                    )
                else:
                    matrix [x,y] = min(
                        matrix[x-1,y] + 1,
                        matrix[x-1,y-1] + 1,
                        matrix[x,y-1] + 1
                    )
        return (matrix[size_x - 1, size_y - 1])