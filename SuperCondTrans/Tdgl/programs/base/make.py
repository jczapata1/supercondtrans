# Make
from programs.base.magnetic_field import uniform, plateau, domains
from programs.base.positions import random, square, hexagonal
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
    -                        path (str): Input File Path

    Output:
    - parameters ((str, ?), dict[?, ?]): Parameters

    Used by:
    - base.make.set_parameters
    - base.transport.set_current
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

# Set Parameters
def set_parameters(path):
    '''
    Assemble general, epsilon, and magnetic field parameters.

    Input:
    -                           path (str): Input File Path

    Output:
    - parameters ((str, dict), dict[?, ?]): Parameters

    Used by:
    - tdgl_setup.TDGLSetup.set_parameters
    '''

    # Parameters
    general    = read_parameters(path)
    path1      = os.path.join('.', 'input', 'Epsilon', f"{general['disorder']}.in")
    path2      = os.path.join('.', 'input', 'Fields',  f"{general['profile']}.in")
    parameters = {'General': general, 'Epsilon': read_parameters(path1), 'Magnetic_Field': read_parameters(path2)}

    return parameters

#---------------------------------------------------------------------------------------------------------------------------------------------

# Make Setup
def make_setup(path, parameters):
    '''
    Compute device, epsilon, magnetic field, and vector potential.

    Input:
    -                           path (str): Output Folder Path
    - parameters ((str, dict), dict[?, ?]): Parameters

    Output:
    -                 device (tdgl.Device): TDGL Device
    -       ε (float, numpy.ndarray[?, 1]): Epsilon Profile
    -      Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field
    -     Axy (float, numpy.ndarray[?, 2]): xy-Vector Potential
    - Device.h5
    - Setup.h5

    Used by:
    - tdgl_setup.TDGLSetup.make_setup
    '''

    # Parameters
    parameters['Epsilon']['Lx']             = parameters['General']['Lx']
    parameters['Epsilon']['Ly']             = parameters['General']['Ly']
    parameters['Epsilon']['dist']           = parameters['General']['dist']
    parameters['Magnetic_Field']['profile'] = parameters['General']['profile']
    parameters['Magnetic_Field']['gauge']   = parameters['General']['gauge']

    # Make
    device = make_device(path, parameters['General'])
    ε      = make_epsilon(path, parameters['Epsilon'], device)
    Bz     = make_magnetic_field(path, parameters['Magnetic_Field'], device)
    Axy    = make_vector_potential(path, parameters['Magnetic_Field'], device, Bz)

    # Save
    device.to_hdf5(os.path.join(path, 'Device.h5'))
    
    with h5py.File(os.path.join(path, 'Setup.h5'), 'w') as file:

        # Profiles
        group = file.create_group('Profiles')
        group.create_dataset('ε',   data=ε)
        group.create_dataset('Bz',  data=Bz)
        group.create_dataset('Axy', data=Axy)

        # Parameters
        group = file.create_group('Parameters')
        for (name, params) in parameters.items():
            subgroup = group.create_group(name)
            
            for (key, value) in params.items():
                subgroup.create_dataset(key, data=value)

    return device, ε, Bz, Axy

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
    - base.make.make_setup
    '''

    # Parameters
    ξ   = parameters['ξ']
    λ   = parameters['λ']
    u   = parameters['u']
    γ   = parameters['γ']
    σ   = parameters['σ']
    Lx  = parameters['Lx']
    Ly  = parameters['Ly']
    Lz  = parameters['Lz']
    NPP = parameters['NPP']

    # Geometry and Boundaries
    layer  = tdgl.Layer(coherence_length=ξ, london_lambda=λ, thickness=Lz, u=u, gamma=γ, conductivity=σ)
    film   = tdgl.Polygon('film', points=box(Lx, Ly))
    source = tdgl.Polygon('source', points=box(ξ, Ly)).translate(dx=-Lx/2)
    drain  = tdgl.Polygon('drain', points=box(ξ, Ly)).translate(dx=+Lx/2)

    # Probe Points
    line         = np.linspace(-Ly/3, Ly/3, NPP)
    probe_points = [(-Lx/3, yi) for yi in line] + [(Lx/3, yi) for yi in line]

    # Device and Mesh
    device = tdgl.Device('rectangular_film', layer=layer, film=film, terminals=[source, drain], probe_points=probe_points, length_units='um')
    device.make_mesh(max_edge_length=ξ/2)

    return device

#---------------------------------------------------------------------------------------------------------------------------------------------

# Make Epsilon
def make_epsilon(path, parameters, device):
    '''
    Compute the epsilon profile.

    Input:
    -                        path (str): Output Folder Path
    - parameters ((str, ?), dict[?, ?]): Parameters
    -              device (tdgl.Device): TDGL Device

    Output:
    -    ε (float, numpy.ndarray[?, 1]): Epsilon Profile

    Used by:
    - base.make.make_setup
    '''

    # Parameters
    Lx   = parameters['Lx']
    Ly   = parameters['Ly']
    dist = parameters['dist']
    N    = parameters['N']
    R    = parameters['R']
    σR   = parameters['σR']
    ε0   = parameters['ε0']
    σε   = parameters['σε']
    seed = parameters['seed']   

    # Mesh
    points = device.points
    X, Y   = points[:, 0], points[:, 1]

    # No Pinning
    if (N == 0): return 1

    # Random State
    rng = np.random.default_rng(seed)

    # Positions
    if (dist == 'Random'):
        Xp, Yp = random(Lx, Ly, N, rng)
    elif (dist == 'Square'):
        Xp, Yp = square(Lx, Ly, N)
    elif (dist == 'Hexagonal'):
        Xp, Yp = hexagonal(Lx, Ly, N)
    else:
        raise ValueError("Invalid Distribution!. Use 'Random', 'Square', or 'Hexagonal'.")

    # Disorder
    r = rng.lognormal(np.log(R), σR, Xp.shape)
    ε = rng.normal(ε0, σε, Xp.shape)
    ε = np.clip(ε, -1.0, max(ε0, 1.0))

    # Epsilon
    d     = np.sqrt((Xp - X)**2 + (Yp - Y)**2)
    gauss = (ε - 1) * np.exp(-(d**2 / (2*r**2)))
    ε     = np.clip(1 + gauss.sum(axis=0), -1.0, max(float(ε0), 1.0))

    return ε

#---------------------------------------------------------------------------------------------------------------------------------------------
     
# Make Magnetic Field
def make_magnetic_field(path, parameters, device):
    '''
    Compute the magnetic field profile.

    Input:
    -                        path (str): Output Folder Path
    - parameters ((str, ?), dict[?, ?]): Parameters
    -              device (tdgl.Device): TDGL Device

    Output:
    -   Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field

    Used by:
    - base.make.make_setup
    '''

    # Parameters
    profile = parameters['profile']

    # Mesh
    points = device.points
    X, Y   = points[:, 0], points[:, 1]

    # Magnetic Field
    if (profile == 'Uniform'):
        Bz = uniform(X, Y, parameters)
    elif (profile == 'Plateau'):
        Bz = plateau(X, Y, parameters)
    elif (profile == 'Domains'):
        Bz = domains(X, Y, parameters)
    else:
        raise ValueError("Invalid Profile!. Use 'Uniform', 'Plateau', or 'Domains'.")

    return Bz
    
#---------------------------------------------------------------------------------------------------------------------------------------------

# Make Vector Potential
def make_vector_potential(folder, parameters, device, Bz):
    '''
    Compute the vector potential profile.

    Input:
    -                              folder (str): Output Folder Path
    -         parameters ((str, ?), dict[?, ?]): Parameters
    -                      device (tdgl.Device): TDGL Device
    -           Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field

    Output:
    - Axy ((float, float), numpy.ndarray[?, 2]): xy-Vector Potential

    Used by:
    - base.make.make_setup
    '''

    # Mesh
    points = device.points
    X, Y   = points[:, 0], points[:, 1]

    # Magnetic Field
    Bz_int  = LinearNDInterpolator(points, Bz)
    Bz_func = lambda x, y: Bz_int(np.column_stack([x.ravel(), y.ravel()])).reshape(x.shape)

    # Vector Potential
    gauge    = parameters['gauge']
    Axy_func = vector_potential(Bz_func, points, gauge)
    Axy      = Axy_func(X, Y)

    return Axy