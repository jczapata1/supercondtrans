# Load
from scipy.interpolate import LinearNDInterpolator
from programs.utils import *
import tdgl

#------------------------------------------------------------------------------

# Load Setup
def load_setup(path):
    '''
    Load parameters, device, epsilon, magnetic field, and vector potential.

    Input:
    -                           path (str): Input Folder Path

    Output:
    - parameters ((str, dict), dict[?, ?]): Parameters
    -                 device (tdgl.Device): TDGL Device
    -       ε (float, numpy.ndarray[?, 1]): Epsilon
    -      Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field
    -                  Axy_func (callable): xy-Vector Potential

    Used by:
    - tdgl_simulation.TDGLSimulation.load_setup
    '''

    # Paths
    path1 = os.path.join(path, 'Device.h5') 
    path2 = os.path.join(path, 'Setup.h5')

    # Load
    parameters = load_parameters(path2)
    device     = load_device(path1)
    ε          = load_epsilon(path2)
    Bz         = load_magnetic_field(path2)
    Axy_func   = load_vector_potential(path2, device)

    return parameters, device, ε, Bz, Axy_func

#------------------------------------------------------------------------------

# Load Parameters
def load_parameters(path):
    '''
    Load simulation parameters.

    Input:
    -                           path (str): Input File Path

    Output:
    - parameters ((str, dict), dict[?, ?]): Parameters

    Used by:
    - base.load.load_setup
    '''

    # Load
    with h5py.File(path, 'r') as file:
        parameters = {}

        for group in file['Parameters']:
            parameters[group] = {}

            for key in file[f'Parameters/{group}']:
                parameters[group][key] = file[f'Parameters/{group}/{key}'][()]

    return parameters

#------------------------------------------------------------------------------

# Load Device
def load_device(path):
    '''
    Load the TDGL Device profile.

    Input:
    -           path (str): Input File Path

    Output:
    - device (tdgl.Device): TDGL Device

    Used by:
    - base.load.load_setup
    '''

    # Load
    device = tdgl.Device.from_hdf5(path)

    return device

#------------------------------------------------------------------------------

# Load Epsilon
def load_epsilon(path):
    '''
    Load the epsilon profile.

    Input:
    -                     path (str): Input File Path

    Output:
    - ε (float, numpy.ndarray[?, 1]): Epsilon

    Used by:
    - base.load.load_setup
    '''

    # Load
    with h5py.File(path, 'r') as file:
        ε = file['Profiles/ε'][()]

    return ε

#------------------------------------------------------------------------------

# Load Magnetic Field
def load_magnetic_field(path):
    '''
    Load the z-magnetic field profile.

    Input:
    -                      path (str): Input File Path

    Output:
    - Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field

    Used by:
    - base.load.load_setup
    '''

    # Load
    with h5py.File(path, 'r') as file:
        Bz = file['Profiles/Bz'][:]

    return Bz

#------------------------------------------------------------------------------

# Load Vector Potential
def load_vector_potential(path, device):
    '''
    Load the xy-vector potential profile.

    Input:
    -           path (str): Input File Path
    - device (tdgl.Device): TDGL Device

    Output:
    -  Axy_func (callable): xy-Vector Potential

    Used by:
    - base.load.load_setup
    '''

    # Load
    with h5py.File(path, 'r') as file:
        Axy = file['Profiles/Axy'][:]

    # Data
    points = device.points
    Ax_int = LinearNDInterpolator(points, Axy[:, 0])
    Ay_int = LinearNDInterpolator(points, Axy[:, 1])

    # Vector Potential
    def Axy_func(x, y, z=None):
        pts = np.column_stack([x.ravel(), y.ravel()])
        Axy = np.stack([Ax_int(pts), Ay_int(pts)], axis=-1)
        return Axy
        
    return Axy_func