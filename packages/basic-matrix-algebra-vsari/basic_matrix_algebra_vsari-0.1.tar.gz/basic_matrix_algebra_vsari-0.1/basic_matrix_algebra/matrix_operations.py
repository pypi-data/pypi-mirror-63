
import sys
import unittest

class Matrix(object):
    """ A simple Python matrix class with basic operations """

    def __init__(self, m, n,init=True):
        if init:
            self.rows = [[0] * n for x in range(m)]
        else:
            self.rows = []

        self.m = m
        self.n = n

    @classmethod
    def _makeMatrix(cls, rows):

        m = len(rows)
        n = len(rows[0])
        mat = Matrix(m, n)
        mat.rows = rows
        return mat

    def __add__(self, other):
        """ Add a matrix to this matrix and  return the new matrix.
        Doesn't modify the current matrix """

        new = Matrix(self.m, self.n)
        for x in range(self.m):
            row = [sum(item) for item in zip(self.rows[x], other.rows[x])]
            new.rows[x] = row
        return new

    def __sub__(self, other):
        """ Add a matrix to this matrix and  return the new matrix.
        Doesn't modify the current matrix """

        new = Matrix(self.m, self.n)
        for x in range(self.m):
            row = [item[0]-item[1] for item in zip(self.rows[x], other.rows[x])]
            new.rows[x] = row
        return new

    def __mul__(self, other):
        """ Multiple a matrix with this matrix and  return the new matrix.
         Doesn't modify the current matrix """

        matm, matn = other.m, other.n

        if (self.n != matm):
            raise MatrixError("Matrices cannot be multipled!")

        other_t = other.getTranspose()
        new = Matrix(self.m, matn)

        for x in range(self.m):
            for y in range(other_t.m):
                new.rows[x][y] = sum([item[0] * item[1] for item in zip(self.rows[x], other_t.rows[y])])

        return new


    def getTranspose(self):
        """ Return a transpose of the matrix without
        modifying the matrix itself """

        m, n = self.n, self.m
        mat = Matrix(m, n)
        mat.rows = [list(item) for item in zip(*self.rows)]

        return mat

    def __eq__(self, other):
        """ Test equality """

        return (other.rows == self.rows)


    def __repr__(self):
        s = str(self.rows)
        rank = str(self.m) +" x "+ str (self.n)
        rep = "Matrix: \"%s\", rank: \"%s\"" % (s, rank)
        return rep


