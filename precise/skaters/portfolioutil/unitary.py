import numpy as np
from precise.skaters.covarianceutil.covfunctions import try_invert
from precise.skaters.portfolioutil.portfunctions import portfolio_variance
from typing import List
from itertools import zip_longest
from precise.skaters.locationutil.vectorfunctions import normalize

# Long-short min-var portfolios where the only constraint is sum(w)=1


def prc_unit_port(pre=None, cov=None):
    """ Signed min var portfolio summing to unity """
    if pre is not None:
        return unitary_from_pre(pre=pre)
    else:
        return weak_from_cov(cov=cov)


def unitary_from_pre(pre):
    """ Signed min var portfolio summing to unity """
    # No optimization required
    n_dim = np.shape(pre)[1]
    wones = np.ones(shape=(n_dim, 1))
    return normalize(np.squeeze(np.matmul(pre, wones)))


def weak_from_cov(cov):
    pre = try_invert(cov)
    return unitary_from_pre(pre=pre)


def unitary_portfolio_variance(cov=None, pre=None):
    """
        Variance of the unit min-var portfolio
        (Used in some hierarchical methods to allocate capital)
    """
    w = prc_unit_port(pre=pre, cov=cov)
    return portfolio_variance(cov=cov,w=w)


def prc_unit_alloc(covs:List, pres:List)->[float]:
    """ Allocate capital between portfolios using either cov or pre matrices
    :param covs:  List of covariance matrices
    :param pres:  List of precision matrices
    :return: Capital allocation vector
    """
    return normalize([ 1/unitary_portfolio_variance(cov=cov, pre=pre) for cov, pre in zip_longest(covs, pres, fillvalue=None) ])




