# Positions
from programs.utils import *

#------------------------------------------------------------------

# Random Positions
def random(Lx, Ly, N, rng):
    '''
    Generate random site positions.

    Input:
    -                     Lx (float): x-Length
    -                     Ly (float): y-Length
    -                        N (int): Number of Sites
    -          rng (numpy.Generator): Random Number Generator

    Output:
    - X (float, numpy.ndarray[N, 1]): x-Coordinates 
    - Y (float, numpy.ndarray[N, 1]): y-Coordinates

    Used by:
    - base.make.make_epsilon
    '''

    # Positions
    x    = rng.uniform(-Lx/2, Lx/2, N)
    y    = rng.uniform(-Ly/2, Ly/2, N)
    X, Y = x.reshape(-1, 1), y.reshape(-1, 1)

    return X, Y

#------------------------------------------------------------------

# Square Positions
def square(Lx, Ly, N):
    '''
    Generate square lattice site positions.

    Input:
    -                     Lx (float): x-Length
    -                     Ly (float): y-Length
    -                        N (int): Number of Sites

    Output:
    - X (float, numpy.ndarray[?, 1]): x-Coordinates 
    - Y (float, numpy.ndarray[?, 1]): y-Coordinates
    
    Used by:
    - base.make.make_epsilon
    '''

    # Parameters
    a  = np.sqrt(Lx*Ly/N)    # Lattice Constant
    Nx = max(1, round(Lx/a)) # x-Sites
    Ny = max(1, round(Ly/a)) # y-Sites
    N  = Nx * Ny             # Number of Sites

    # Mesh
    x    = np.linspace(-Lx/2 + Lx/(2*Nx), Lx/2 - Lx/(2*Nx), Nx)
    y    = np.linspace(-Ly/2 + Ly/(2*Ny), Ly/2 - Ly/(2*Ny), Ny)
    X, Y = np.meshgrid(x, y)
    X, Y = X.ravel().reshape(-1, 1), Y.ravel().reshape(-1, 1)

    return X, Y

#------------------------------------------------------------------

# Hexagonal Positions
def hexagonal(Lx, Ly, N):
    '''
    Generate hexagonal lattice site positions.

    Input:
    -                     Lx (float): x-Length
    -                     Ly (float): y-Length
    -                        N (int): Number of Sites

    Output:
    - X (float, numpy.ndarray[?, 1]): x-Coordinates 
    - Y (float, numpy.ndarray[?, 1]): y-Coordinates

    Used by:
    - base.make.make_epsilon
    '''

    # Parameters
    a  = np.sqrt((2*Lx*Ly) / (N*np.sqrt(3)))    # Lattice Constant
    Nx = max(1, round(Lx/a))                    # x-Sites
    Ny = max(1, round((2*Ly) / (a*np.sqrt(3)))) # y-Sites
    N  = Nx * Ny                                # Number of Sites

    # Mesh
    x    = np.linspace(-Lx/2, Lx/2, Nx)
    y    = np.linspace(-Ly/2, Ly/2, Ny)
    X, Y = np.meshgrid(x, y)
    X, Y = X.ravel().reshape(-1, 1), Y.ravel().reshape(-1, 1)

    return X, Y