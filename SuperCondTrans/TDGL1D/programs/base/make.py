# Make
from programs.utils import *
import re

#-------------------------------------------------------------------

# Read Parameters
def read_parameters(path):
    '''
    Read parameters from a input file.

    Input:
    -                        path (str): Input File Path

    Output:
    - parameters ((str, ?), dict[?, ?]): Parameters

    Used by:
    - tdgl1d_simulation.TDGL1DSimulation.read_parameters
    '''

    # Parameters
    parameters = {}

    # Constants
    parameters['π']            = π
    parameters['KB']           = KB
    parameters['ħ']            = ħ

    # Functions
    parameters['scaling_func'] = scaling_func

    # Read
    with open(path, 'r') as file:
        
        for line in file:
            match = re.match(r'^(\S+)\s*:\s*(.+)$', line)
            
            if (match):
                name             = match.group(1)
                value            = match.group(2).strip()
                parameters[name] = eval(value, {}, parameters)

    # Delete
    del parameters['π']
    del parameters['KB']
    del parameters['ħ']
    del parameters['scaling_func']

    return parameters

#-------------------------------------------------------------------

# Make Vortex
def make_vortex(parameters, t, y):
    '''
    Compute the vortex-like potential profile.

    Input:
    - parameters ((str, ?), dict[?, ?]): Parameters
    -                         t (float): Time
    -    y (float, numpy.ndarray[?, 1]): Grid

    Output:
    -    V (float, numpy.ndarray[?, 1]): Vortex-Like Potential

    Used by:
    - base.run.run
    '''

    # Parameters
    Ly   = parameters['Ly']
    V0   = parameters['V0']
    ξ    = parameters['ξ']
    v    = parameters['v']
    mode = parameters['mode']
    Nv   = parameters['Nv']
    a    = parameters['a']

    # Injection
    y_inj = -0.5 * Ly * np.sign(v)

    # Vortex 
    V  = np.zeros_like(y)
    
    if (mode == 'Single'):
        
        yc = y_inj + v*t
        r  = np.clip((y-yc) / (np.sqrt(2)*ξ), -354, 354)
        V  = V + V0 / np.cosh(r)**2

    elif (mode == 'Train'):
        
        for n in range(Nv):
            yc = y_inj - n*a*np.sign(v) + v*t
            r  = np.clip((y-yc) / (np.sqrt(2)*ξ), -354, 354)
            V  = V + V0 / np.cosh(r)**2

    else:
        raise ValueError("Invalid Mode!. Use 'Single' or 'Train'.")

    return V