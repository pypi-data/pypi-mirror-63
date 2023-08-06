# Any changes to the distributions library should be reinstalled with
#pip install --upgrade .

# For running unit tests, use
#gauss/usr/bin/python -m unittest test

import unittest

from basic_matrix_algebra import Matrix

class MatrixTests(unittest.TestCase):

    def testAdd(self):
        m1 = Matrix._makeMatrix([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix._makeMatrix([[7, 8, 9], [10, 11, 12]])
        m3 = m1 + m2
        self.assertTrue(m3 == Matrix._makeMatrix([[8, 10, 12], [14, 16, 18]]))

    def testSub(self):
        m1 = Matrix._makeMatrix([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix._makeMatrix([[7, 8, 9], [10, 11, 12]])
        m3 = m2 - m1
        self.assertTrue(m3 == Matrix._makeMatrix([[6, 6, 6], [6, 6, 6]]))

    def testMul(self):
        m1 = Matrix._makeMatrix([[1, 2, 3], [4, 5, 6]])
        m2 = Matrix._makeMatrix([[7, 8], [10, 11], [12, 13]])
        self.assertTrue(m1 * m2 == Matrix._makeMatrix([[63, 69], [150, 165]]))
        #self.assertTrue(m2 * m1 == Matrix._makeMatrix([[39, 54, 69], [54, 75, 96], [64, 89, 114]]))

    def testTranspose(self):
        m1 = Matrix._makeMatrix([[1, 2, 3], [4, 5, 6]])
        # Also test getTranspose
        m2 = m1.getTranspose()
        self.assertTrue(m2 == Matrix._makeMatrix([[1, 4], [2,5],[3,6]]))

if __name__ == "__main__":
    unittest.main()