# Load
from scipy.interpolate import LinearNDInterpolator
from programs.utils import *
import tdgl

#-----------------------------------------------------------

# Load Device
def load_device(path):
    '''
    Load the TDGL Device profile.

    Input:
    -           path (str): Input File Path

    Output:
    - device (tdgl.Device): TDGL Device

    Used by:
    - tdgl_fields.TDGLFields.load_device
    - tdgl_simulation.TDGLSimulation.load_device
    - tdgl_animation.TDGLAnimation.load_device
    '''

    # Load
    device = tdgl.Device.from_hdf5(path)

    return device

#-----------------------------------------------------------

# Load Magnetic Field
def load_magnetic_field(path):
    '''
    Load the z-magnetic field profile.

    Input:
    -                      path (str): Input File Path

    Output:
    - Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field

    Used by:
    - tdgl_simulation.TDGLSimulation.load_magnetic_field
    '''

    # Load
    Bz = from_hdf5(path).Bz

    return Bz

#-----------------------------------------------------------

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
    - tdgl_simulation.TDGLSimulation.load_vector_potential
    '''

    # Data
    A      = from_hdf5(path)
    points = device.points
    Ax_int = LinearNDInterpolator(points, A.Ax)
    Ay_int = LinearNDInterpolator(points, A.Ay)

    def Axy_func(x, y, z=None):
        pts = np.column_stack([x.ravel(), y.ravel()])
        Axy = np.stack([Ax_int(pts), Ay_int(pts)], axis=-1)
        return Axy

    return Axy_func

#-----------------------------------------------------------

# Load Solution
def load_solution(path):
    '''
    Load the TDGL Solution.

    Input:
    -               path (str): Input File Path

    Output:
    - solution (tdgl.Solution): TDGL Solution

    Used by:
    - tdgl_animation.TDGLAnimation.load_solution
    '''

    # Load
    solution = tdgl.Solution.from_hdf5(path)

    return solution