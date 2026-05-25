# Initialize
from programs.base.magnetic_field import uniform, plateau, domains
from programs.base.vector_potential import vector_potential
from scipy.interpolate import LinearNDInterpolator
from tdgl.geometry import box
from programs.utils import *
import logging
import tdgl
import re

# Logging
logging.getLogger('tdgl').setLevel(logging.ERROR)

#---------------------------------------------------------------------------------------------------------------------------------------------

# Read Parameters
def read_parameters(path):
    '''
    Read parameters from a input file.

    Input:
    -                        path (str): Input Path

    Output:
    - parameters ((str, ?), dict[?, ?]): Parameters

    Used by:
    - tdgl_device.TDGLDevice.read_parameters
    - tdgl_fields.TDGLFields.read_parameters
    - tdgl_simulation.TDGLSimulation.read_parameters
    - base.physics.set_current
    '''

    # Parameters
    parameters = {}

    # Constants
    parameters['π']  = π
    parameters['φ0'] = φ0

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
    del parameters['φ0']
    del parameters['scaling_func']

    return parameters

#---------------------------------------------------------------------------------------------------------------------------------------------

# Make Device
def make_device(path, parameters):
    '''
    Compute the device profile.   

    Input:
    -                        path (str): Output Folder Path
    - parameters ((str, ?), dict[?, ?]): Parameters

    Output:
    -              device (tdgl.Device): TDGL Device

    Used by:
    - tdgl_device.TDGLDevice.make_device
    '''

    # Parameters
    ξ   = parameters['ξ']
    λ   = parameters['λ']
    u0  = parameters['u0']
    γ   = parameters['γ']
    σ   = parameters['σ']
    Lx  = parameters['Lx']
    Ly  = parameters['Ly']
    Lz  = parameters['Lz']
    NPP = parameters['NPP']

    # Geometry and Boundaries
    layer  = tdgl.Layer(coherence_length=ξ, london_lambda=λ, thickness=Lz, u=u0, gamma=γ, conductivity=σ)
    film   = tdgl.Polygon('film', points=box(Lx, Ly))
    source = tdgl.Polygon('source', points=box(ξ, Ly)).translate(dx=-Lx/2)
    drain  = tdgl.Polygon('drain', points=box(ξ, Ly)).translate(dx=+Lx/2)

    # Probe Points
    line         = np.linspace(-Ly/3, Ly/3, NPP)
    probe_points = [(-Lx/3, yi) for yi in line] + [(Lx/3, yi) for yi in line]

    # Device and Mesh
    device = tdgl.Device('rectangular_film', layer=layer, film=film, terminals=[source, drain], probe_points=probe_points, length_units='um')
    device.make_mesh(max_edge_length=ξ/2)

    # Save
    device.to_hdf5(os.path.join(path, 'Device.h5'))

    return device

#---------------------------------------------------------------------------------------------------------------------------------------------

# Make Magnetic Field
def make_magnetic_field(path, profile, parameters, device):
    '''
    Compute the magnetic field profile.

    Input:
    -                        path (str): Output Folder Path
    -                     profile (str): Profile
    - parameters ((str, ?), dict[?, ?]): Parameters
    -              device (tdgl.Device): TDGL Device

    Output:
    -   Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field

    Used by:
    - tdgl_fields.TDGLFields.make_magnetic_field
    '''

    # Mesh
    X, Y = device.points[:, 0], device.points[:, 1]

    if (profile == 'Uniform'):
        Bz = uniform(X, Y, parameters)
    elif (profile == 'Plateau'):
        Bz = plateau(X, Y, parameters)
    elif (profile == 'Domains'):
        Bz = domains(X, Y, parameters)
    else:
        raise ValueError("Invalid Profile!. Use 'Uniform', 'Plateau', or 'Domains'.")

    # Save    
    to_hdf5(os.path.join(path, 'Magnetic_Field.h5'), Bz=Bz)

    return Bz

#---------------------------------------------------------------------------------------------------------------------------------------------

# Make Vector Potential
def make_vector_potential(folder, gauge, device, Bz):
    '''
    Compute the vector potential profile.

    Input:
    -                              folder (str): Output Folder Path
    -                               gauge (str): Gauge
    -                      device (tdgl.Device): TDGL Device
    -           Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field

    Output:
    - Axy ((float, float), numpy.ndarray[?, 2]): xy-Vector Potential

    Used by:
    - tdgl_fields.TDGLFields.make_vector_potential
    '''

    # Mesh
    points = device.points

    # Magnetic Field
    Bz_int  = LinearNDInterpolator(points, Bz)
    Bz_func = lambda x, y: Bz_int(np.column_stack([x.ravel(), y.ravel()])).reshape(x.shape)

    # Vector Potential
    Axy_func = vector_potential(Bz_func, points, gauge)
    Axy      = Axy_func(points[:, 0], points[:, 1])

    # Save
    to_hdf5(os.path.join(folder, 'Vector_Potential.h5'), Ax=Axy[:, 0], Ay=Axy[:, 1])

    return Axy