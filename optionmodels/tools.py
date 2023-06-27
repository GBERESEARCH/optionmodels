"""
Mathematical tools - Cholesky decomposition, combinatorics

"""
from functools import reduce
import operator as op
import numpy as np
# pylint: disable=invalid-name

class Tools():
    """
    Mathematical tools - Cholesky decomposition, combinatorics

    """

    @staticmethod
    def cholesky_decomposition(matrix: np.ndarray) -> np.ndarray:
        """
        Cholesky Decomposition.
        Return M in M * M.T = matrix where matrix is a symmetric positive
        definite correlation matrix

        Parameters
        ----------
        matrix : Array
            Correlation matrix.

        Returns
        -------
        M : Array
            Matrix decomposition.

        """

        # Number of columns in input correlation matrix R
        n = len(matrix[0])

        a = np.zeros((n + 1, n + 1))
        M = np.zeros((n + 1, n + 1))

        for i in range(n + 1):
            for j in range(n + 1):
                a[i, j] = matrix[i, j]
                M[i, j] = 0

        for i in range(n + 1):
            for j in range(n + 1):
                U = a[i, j]
            for h in range(1, i):
                U = U - M[i, h] * M[j, h]
            if j == 1:
                M[i, i] = np.sqrt(U)
            else:
                M[j, i] = U / M[i, i]

        return M


    @staticmethod
    def n_choose_r(n: int, r: int) -> int:
        """
        Binomial Coefficients. n choose r
        Number of ways to choose an (unordered) subset of r elements
        from a fixed
        set of n elements.

        Parameters
        ----------
        n : Int
            Set of elements.
        r : Int
            Subset of elements.

        Returns
        -------
        Int
            Binomial coefficient.

        """

        # Due to symmetry of the binomial coefficient, set r to
        # optimise calculation
        r = min(r, n-r)

        # Numerator is the descending product from n to n+1-r
        numer = reduce(op.mul, range(n, n-r, -1), 1)

        # Denominator is the product from 1 to r
        denom = reduce(op.mul, range(1, r+1), 1)

        # Binomial coefficient is calculated by dividing these two.
        return numer // denom  # or / in Python 2
