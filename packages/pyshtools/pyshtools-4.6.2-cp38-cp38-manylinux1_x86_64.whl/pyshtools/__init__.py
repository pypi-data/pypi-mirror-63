"""
pyshtools
=========

pyshtools is an archive of scientific routines that can be used to
perform spherical harmonic transforms and reconstructions, rotations
of data expressed in spherical harmonics, and multitaper spectral
analyses on the sphere.

This module imports the following classes and subpackages into the
main namespace:

    SHCoeffs          : Class for spherical harmonic coefficients.
    SHGrid            : Class for global grids.
    SHWindow          : Class for localized spectral analyses.
    Slepian           : Class for Slepian functions.
    SlepianCoeffs     : Class for Slepian expansion coefficients.
    SHGravCoeffs      : Class for gravitational potential spherical harmonic
                        coefficients.
    SHGravGrid        : Class for global gridded gravitational field data.
    SHGravTensor      : Class for the gravity tensor and eigenvalues.
    SHGeoid           : Class for the geoid.
    SHMagCoeffs       : Class for magnetic potential spherical harmonic
                        coefficients.
    SHMagGrid         : Class for global gridded magnetic field data.
    SHMagTensor       : Class for the magnetic field tensor and eigenvalues.

    shclasses         : All pyshtools classes and subclasses.
    shtools           : All Python-wrapped Fortran 95 routines.
    constant          : pyshtools constants.
    legendre          : Legendre functions.
    expand            : Spherical harmonic expansion routines.
    shio              : Spherical harmonic I/O, storage, and conversion
                        routines.
    spectralanalysis  : Global and localized spectral analysis routines.
    rotate            : Spherical harmonic rotation routines.
    gravmag           : Gravity and magnetics routines.
    utils             : pyshtools utilities.

For further information, consult the web documentation at

   https://shtools.oca.eu/

and the GitHub project page at

   https://github.com/SHTOOLS/SHTOOLS
"""
__version__ = '4.6'
__author__ = 'SHTOOLS developers'


# ---- Import shtools subpackages ----
from . import shtools
from . import constant
from . import shclasses
from . import legendre
from . import expand
from . import shio
from . import spectralanalysis
from . import rotate
from . import gravmag
from . import utils

# ---- Import principal classes into pyshtools namespace
from .shclasses import SHCoeffs
from .shclasses import SHGrid
from .shclasses import SHWindow
from .shclasses import Slepian
from .shclasses import SlepianCoeffs
from .shclasses import SHGravCoeffs
from .shclasses import SHGravGrid
from .shclasses import SHGravTensor
from .shclasses import SHGeoid
from .shclasses import SHMagCoeffs
from .shclasses import SHMagGrid
from .shclasses import SHMagTensor

# ---- Define __all__ for use with: from pyshtools import * ----
__all__ = ['constant', 'shclasses', 'legendre', 'expand', 'shio', 'shtools',
           'spectralanalysis', 'rotate', 'gravmag', 'utils', 'SHCoeffs',
           'SHGrid', 'SHWindow', 'Slepian', 'SlepianCoeffs', 'SHGravCoeffs',
           'SHGravGrid', 'SHGravTensor', 'SHGeoid', 'SHMagCoeffs', 'SHMagGrid',
           'SHMagTensor']
