from precise.skaters.covarianceutil.covfunctions import try_invert, cov_distance
from precise.skaters.portfolioutil.diagonal import prc_diag_alloc, prc_diag_port
from seriate import seriate
import numpy as np
from functools import partial




def corr_seriation_portfolio_factory(port, port_kwargs:dict=None, seriator=None, cov=None, pre=None):
    """
        A utility for portfolio methods that prefer to receive assets in some "seriated" ordering
        The seriator acts on distances implied by correlations

    :param seriator:          Takes a distance matrix and returns an ordering
    :param port:              Portfolio generator
    :param port_kwargs:       Arguments to portfolio generator, other than 'cov' and/or 'pre'
    :param cov:               Original portfolio in arbitrary order
    :param pre:               Original precision matrix in arbitrary order
    :return: w                Portfolio weights in original ordering
    """
    if cov is None:
        cov = try_invert(pre)

    if seriator is None:
        seriator = seriate

    if port_kwargs is None:
        port_kwargs = {}

    # Establish ordering using seriator anc corr distances
    cov_dist = cov_distance(cov)
    ndx = seriator(cov_dist)
    inv_ndx = np.argsort(ndx)
    cov_cols = cov[:,ndx]
    cov_back = cov_cols[:,inv_ndx]
    assert np.allclose(cov,cov_back)
    ordered_cov = cov_cols[ndx,:]

    # Allocate capital to ordered assets
    ordered_w = port(cov=ordered_cov, **port_kwargs)

    # Return to original ordering
    w = ordered_w[inv_ndx]
    return w



if __name__=='__main__':
    from precise.skaters.covarianceutil.covrandom import random_band_cov
    cov = random_band_cov()
    print(np.shape(cov))
    ordered_cov = corr_seriation_portfolio_factory(cov=cov, alloc=None)
    from precise.skaters.covarianceutil.covfunctions import cov_to_corrcoef
    ordered_corrcoef = cov_to_corrcoef(ordered_cov)
    pass


