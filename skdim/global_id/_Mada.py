#
# MIT License
#
# Copyright (c) 2020 Jonathan Bac
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import warnings
import numpy as np
from scipy.spatial.distance import pdist, squareform
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_array


class Mada(BaseEstimator):

    """ A template estimator to be used as a reference implementation.
    For more information regarding how to build your own estimator, read more
    in the :ref:`User Guide <user_guide>`.
    Parameters
    ----------
    demo_param : str, default='demo_param'
        A parameter used for demonstation of how to pass and store paramters.
    """

    def __init__(self, k=20, comb="average", DM=False, local=False):
        self.k = k
        self.comb = comb
        self.DM = DM
        self.local = local

    def fit(self, X, y=None):
        """A reference implementation of a fitting function.
        Parameters
        ----------
        X : {array-like}, shape (n_samples, n_features)
            The training input samples.
        y : dummy parameter to respect the sklearn API

        Returns
        -------
        self : object
            Returns self.
        """
        X = check_array(X, accept_sparse=False)
        if len(X) == 1:
            raise ValueError("Can't fit with 1 sample")
        if X.shape[1] == 1:
            raise ValueError("Can't fit with n_features = 1")
        if not np.isfinite(X).all():
            raise ValueError("X contains inf or NaN")
        if self.k >= len(X):
            warnings.warn(
                'k larger or equal to len(X), using len(X)-1')

        self._k = len(X)-1 if self.k >= len(X) else self.k

        self.dimension_ = self._mada(X)
        self.is_fitted_ = True
        # `fit` should always return `self`
        return self

    def _mada(self, X):

        if (self.DM == False):
            distmat = squareform(pdist(X))

        else:
            distmat = X

        n = len(distmat)

        if (self.local == False and n > 10000):
            ID = np.random.choice(n, size=int(
                np.round(n/2)), replace=False)
            tmpD = distmat[ID, :]
            tmpD[tmpD == 0] = np.max(tmpD)

        else:
            tmpD = distmat
            tmpD[tmpD == 0] = np.max(tmpD)

        sortedD = np.sort(tmpD, axis=0, kind='mergesort')
        RK = sortedD[self._k-1, :]
        RK2 = sortedD[int(np.floor(self._k/2)-1), :]
        ests = np.log(2)/np.log(RK/RK2)

        if (self.local == True):
            return(ests)

        if (self.comb == "average"):
            return np.mean(ests)
        elif (self.comb == "median"):
            return np.median(ests)
