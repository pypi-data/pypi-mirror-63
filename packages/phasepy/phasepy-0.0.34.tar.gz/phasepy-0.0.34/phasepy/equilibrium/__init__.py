﻿"""
phasepy.equilibrium: phase equilibria with Python 
=======================================================


Functions
---------
bubbleTy : bubble point P, x -> T, y
bubblePy : bubble point T, x -> P, y
dewTx : dew point P, y -> T, x
dewTy : dew point T, y -> P, x
flash : istohermal isobaric two phase flash z, T, P -> x,y,beta
ell : liquid liquid equilibrium  z, T, P -> x, w, beta
ell_init : finds initial guess for ell 
multiflash : multiflash algorithm that checks stability of the phases
ellvb : heteroazetropic calculation (VLLE) for binary mixtures
ellv : heteroazetropic calculation (VLLE) for multicomponent mixtures

tpd : Michelsen tpd function
tpd_mim : finds a minimum of tpd function given a initial guess
tpd_minimas : tries to find n minimas of tpd function



"""


from __future__ import division, print_function, absolute_import

__all__ = [s for s in dir() if not s.startswith('_')]

from .bubble import bubblePy, bubbleTy
from .dew import dewPx, dewTx
from .flash import flash
from .multiflash import multiflash
from .hazt import haz, ellv
from .hazb import ellvb
from .stability import tpd_min, tpd_minimas, ell_init, gmix
from .ell import ell