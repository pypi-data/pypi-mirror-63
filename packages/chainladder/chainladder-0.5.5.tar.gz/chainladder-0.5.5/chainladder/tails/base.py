# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import copy
import numpy as np
from chainladder.utils.cupy import cp
from sklearn.base import BaseEstimator, TransformerMixin
from chainladder.development import DevelopmentBase, Development
from chainladder.core import EstimatorIO


class TailBase(BaseEstimator, TransformerMixin, EstimatorIO):
    ''' Base class for all tail methods.  Tail objects are equivalent
        to development objects with an additional set of tail statistics'''
    def fit(self, X, y=None, sample_weight=None):
        obj = copy.copy(X)
        xp = cp.get_array_module(obj.values)
        if 'ldf_'not in obj:
            obj = Development().fit_transform(obj)
        self._ave_period = {'Y': (1, 12),
                            'Q': (4, 3),
                            'M': (12, 1)}[obj.development_grain]
        ddims = np.concatenate(
            (obj.ddims, [(item+1)*self._ave_period[1] + obj.ddims[-1]
                         for item in range(self._ave_period[0])], [9999]), 0)
        self.ldf_ = copy.copy(obj.ldf_)
        tail = xp.ones(self.ldf_.shape)[..., -1:]
        tail = xp.repeat(tail, self._ave_period[0]+1, -1)
        self.ldf_.values = xp.concatenate((self.ldf_.values, tail), -1)
        self.ldf_.ddims = np.array(['{}-{}'.format(ddims[i], ddims[i+1])
                                    for i in range(len(ddims)-1)])
        self.ldf_.valuation = self.ldf_._valuation_triangle()
        self.sigma_ = copy.copy(getattr(obj, 'sigma_', obj.cdf_*0))
        self.std_err_ = copy.copy(getattr(obj, 'std_err_', obj.cdf_*0))
        zeros = tail[..., -1:]*0
        self.sigma_.values = xp.concatenate(
            (self.sigma_.values, zeros), -1)
        self.std_err_.values = xp.concatenate(
            (self.std_err_.values, zeros), -1)
        self.sigma_.ddims = self.std_err_.ddims = \
            np.concatenate(
                (obj.ldf_.ddims,
                 np.array(['{}-9999'.format(int(obj.ddims[-1]))])))
        val_array = self.sigma_._valuation_triangle(self.sigma_.ddims)
        self.sigma_.valuation = self.std_err_.valuation = val_array
        self.cdf_ = DevelopmentBase._get_cdf(self)
        self.cdf_._set_slicers()
        self.ldf_._set_slicers()
        self.sigma_._set_slicers()
        self.std_err_._set_slicers()
        return self

    def transform(self, X):
        X_new = copy.deepcopy(X)
        xp = cp.get_array_module(X.values)
        X_new.std_err_.values = xp.concatenate(
            (X_new.std_err_.values,
             self.std_err_.values[..., -1:]), -1)
        X_new.cdf_.values = xp.concatenate(
            (X_new.cdf_.values,
             self.cdf_.values[..., -self._ave_period[0]-1:]*0+1), -1)
        X_new.cdf_.values = X_new.cdf_.values * \
            self.cdf_.values[..., -self._ave_period[0]-1:-self._ave_period[0]]
        X_new.cdf_.values[..., -1] = self.cdf_.values[..., -1]
        X_new.ldf_.values = xp.concatenate(
            (X_new.ldf_.values,
             self.ldf_.values[..., -self._ave_period[0]-1:]), -1)
        X_new.sigma_.values = xp.concatenate(
            (X_new.sigma_.values, self.sigma_.values[..., -1:]), -1)
        X_new.cdf_.ddims = X_new.ldf_.ddims = self.ldf_.ddims
        X_new.sigma_.ddims = X_new.std_err_.ddims = self.sigma_.ddims
        X_new.cdf_.valuation = X_new.ldf_.valuation = self.ldf_.valuation
        X_new.sigma_.valuation = \
            X_new.std_err_.valuation = self.sigma_.valuation
        X_new.sigma_._set_slicers()
        X_new.ldf_._set_slicers()
        X_new.cdf_._set_slicers()
        X_new.std_err_._set_slicers()
        return X_new

    def fit_transform(self, X, y=None, sample_weight=None):
        """ Equivalent to fit(X).transform(X)

        Parameters
        ----------
        X : Triangle-like
            Set of LDFs based on the model.
        y : Ignored
        sample_weight : Ignored

        Returns
        -------
            X_new : New triangle with transformed attributes.
        """
        self.fit(X)
        if 'std_err_' not in X:
            X = Development().fit_transform(X)
        return self.transform(X)

    def _get_tail_prediction(self, tail_ldf):
        xp = cp.get_array_module(tail_ldf)
        accum_point = self.ldf_.shape[-1] - 1
        ave = 1 + tail_ldf[..., :accum_point]
        all = xp.expand_dims(xp.prod(1 + tail_ldf[..., accum_point:], -1), -1)
        tail = xp.concatenate((ave, all), -1)
        return tail
