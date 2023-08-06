"""
Minimum Description Length Principle (MDLP)
"""

# Guillermo Navas-Palencia <g.navas.palencia@gmail.com>
# Copyright (C) 2020

import numpy as np

from sklearn.base import BaseEstimator
from sklearn.exceptions import NotFittedError
from sklearn.utils import check_array


_check_parameters(min_samples_split, min_samples_leaf, max_candidates,
                  dynamic_split):

    pass


class MDLP(BaseEstimator):
    def __init__(self, min_samples_split=2, min_samples_leaf=2,
                 max_candidates=64, dynamic_split="k-tile"):

        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_candidates = max_candidates
        self.dynamic_split = dynamic_split

        # auxiliary
        self._n_samples = None

        self._is_fitted = None

    def fit(self, x, y):
        _check_parameters(**self.get_params())

        return self._fit(x, y)

    @property
    def splits(self):
        pass
