# Magnetic Field
from programs.utils import *

#-------------------------------------------------------------------------------

# Uniform
def uniform(x, y, parameters):
    '''
    Uniform magnetic field profile.

    Input:
    -        x (float, numpy.ndarray[?, 1]): x-Coordinates
    -        y (float  numpy.ndarray[?, 1]): y-Coordinates
    - parameters ((str, float), dict[1, 1]): Paramaters

    Output:
    -       Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field

    Used by:
    - base.make.make_magnetic_field
    '''

    # Magnetic Field
    B0 = parameters['B0']     # Amplitude
    Bz = B0 * np.ones_like(x) # z-Magnetic Field
    
    return Bz

#-------------------------------------------------------------------------------

# Domains
def domains(x, y, parameters):
    '''
    Periodic stripe domain magnetic field profile.

    Input:
    -        x (float, numpy.ndarray[?, 1]): x-Coordinates
    -        y (float  numpy.ndarray[?, 1]): y-Coordinates
    - parameters ((str, float), dict[1, 1]): Paramaters

    Output:
    -       Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field

    Used by:
    - base.make.make_magnetic_field
    - base.magnetic_field.plateau
    '''

    # Paramaters
    B0       = parameters['B0']       # Field Amplitude
    k        = parameters['k']        # Domain Periods
    Ld       = parameters['Ld']       # Domain Half-Width
    θ        = parameters['θ']        # Stripe Orientation
    φ        = parameters['φ']        # Phase Offset
    B_offset = parameters['B_offset'] # Field Offset

    # Magnetic Field
    l  = x*np.sin(θ) - y*np.cos(θ)                           # Rotation
    Bz = B0 * np.tanh(k * np.sin(2.0*π*l/Ld + φ)) + B_offset # z-Magnetic Field

    return Bz

#-------------------------------------------------------------------------------

# Plateau
def plateau(x, y, parameters):
    '''
    Plateau magnetic field profile.

    Input:
    -        x (float, numpy.ndarray[?, 1]): x-Coordinates
    -        y (float  numpy.ndarray[?, 1]): y-Coordinates
    - parameters ((str, float), dict[1, 1]): Paramaters

    Output:
    -       Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field

    Used by:
    - base.make.make_magnetic_field 
    '''

    # Magnetic Field
    δ  = 1                          # Characteristic length
    Bz = domains(x, y, parameters)  # Base Magnetic Field
    Bz = -np.tanh(y/δ) * np.abs(Bz) # z-Magnetic Field
    
    return Bz