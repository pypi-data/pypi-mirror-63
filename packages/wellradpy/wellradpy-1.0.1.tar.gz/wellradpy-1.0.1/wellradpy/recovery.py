# -*- coding: utf-8 -*-
"""
Created on 2019/06/26

@author: Etienne Bresciani
"""

import numpy as np # version 1.16.2
from .utils import E1, E1inv
import scipy.optimize as opt # version 1.2.1

###############################################################################
# Auxiliary functions
###############################################################################

def barrier_effect_star(rinv_star, t_star):
    return E1(rinv_star**2/t_star) - E1(rinv_star**2/(t_star-1))

def func_root_rinv_star(rinv_star_unknown, sc_star_target, t_star):
    return barrier_effect_star(rinv_star_unknown, t_star) - sc_star_target

def rinv_star(sc_star, t_star):
    """
    Calculate dimensionless radius of investigation.

    Parameters
    ----------
    sc_star: float
        Any positive real number.
    t_star: float
        Any positive real number.

    Returns
    -------
    rinv_star

    """
    # Note: Another method (e.g. Newton) could be more efficient, but bisection is simple and robust, and we expect that efficiency will not be an issue in practice
    sol = opt.root_scalar(func_root_rinv_star, args=(sc_star,t_star), method='bisect', bracket=(1e-12, 1e2), rtol=1e-5)
    return sol.root

def barrier_effect_at_tmax_star(tmax_star):
    return E1((tmax_star-1)*np.log(tmax_star/(tmax_star-1))) - \
           E1(tmax_star*np.log(tmax_star/(tmax_star-1)))

def func_root_tmax_star(tmax_star_unknown, sc_star_target):
    return barrier_effect_at_tmax_star(tmax_star_unknown) - sc_star_target

def tmax_star(sc_star):
    """
    Calculate dimensionless time at which radius of investigation is maximum.

    Parameters
    ----------
    sc_star: float
        Any positive real number.

    Returns
    -------
    tmax_star such that barrier_effect_star(rinv_star, t_star) = sc_star.

    """
    # Note: Another method (e.g. Newton) could be more efficient, but bisection is simple and robust, and we expect that efficiency will not be an issue in practice
    sol = opt.root_scalar(func_root_tmax_star, args=(sc_star), method='bisect', bracket=(1.000001,1e5), rtol=1e-5)
    return sol.root

def barrier_effect_at_tend_star(tend_star):
    return E1(1.e-10/tend_star) - E1(1.e-10/(tend_star-1))

def func_root_tend_star(tend_star_unknown, sc_star_target):
    return barrier_effect_at_tend_star(tend_star_unknown) - sc_star_target

def tend_star(sc_star):
    """
    Calculate dimensionless termination time of the recovery test.

    Parameters
    ----------
    sc_star: float
        Any positive real number.

    Returns
    -------
    tmax_star such that barrier_effect_star(rinv_star, t_star) = sc_star.

    """
    # Note: Another method (e.g. Newton) could be more efficient, but bisection is simple and robust, and we expect that efficiency will not be an issue in practice
    sol = opt.root_scalar(func_root_tend_star, args=(sc_star), method='bisect', bracket=(1.000001,1e5), rtol=1e-5)
    return sol.root

###############################################################################
# Radius of investigation functions
###############################################################################

def rinv_absdrawdiff(t, T, S, Q, sc=0.05):
    """
    Calculate radius of investigation during drawdown based on an absolute drawdown difference criterion.

    Parameters
    ----------
    t: float
        Time from beginning of pumping.
    T: float
        Transmissivity.
    S: float
        Storativity.
    Q: float
        Pumping rate.
    sc: float, optional
        Absolute drawdown difference threshold.

    Returns
    -------
    Radius of investigation.

    Notes
    -----
    Units as you wish, but must be consistent for all the parameters.

    """
    sc_star = 4*np.pi*T*sc/Q
    C = np.sqrt(E1inv(sc_star))
    return C * np.sqrt(T*t/S)
