# Make
from programs.base.magnetic_field import uniform, plateau, domains
from programs.base.positions import random, square, hexagonal
from programs.base.vector_potential import vector_potential
from scipy.interpolate import LinearNDInterpolator
from programs.base.load import load_device
from tdgl.geometry import box
from programs.utils import *
import logging
import tdgl
import re

# Logging
logging.getLogger('tdgl').setLevel(logging.ERROR)

# Warnings
np.seterr(divide='ignore')

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
    - tdgl_device.TDGLDevice.set_parameters

    Last Updated:
    - 07/11/2026
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

    Last Updated:
    - 07/11/2026
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
    Load the device, then compute epsilon, magnetic field, and vector potential.

    Input:
    -                           path (str): Output Folder Path
    - parameters ((str, dict), dict[?, ?]): Parameters

    Output:
    -                 device (tdgl.Device): TDGL Device
    -       ε (float, numpy.ndarray[?, 1]): Epsilon Profile
    -      Bz (float, numpy.ndarray[?, 1]): z-Magnetic Field
    -     Axy (float, numpy.ndarray[?, 2]): xy-Vector Potential
    - Setup.h5

    Used by:
    - tdgl_setup.TDGLSetup.make_setup

    Last Updated:
    - 08/11/2026
    '''

    # Parameters
    parameters['Epsilon']['Lx']             = parameters['General']['Lx']
    parameters['Epsilon']['Ly']             = parameters['General']['Ly']
    parameters['Epsilon']['dist']           = parameters['General']['dist']
    parameters['Epsilon']['TC']             = parameters['General']['TC']
    parameters['Epsilon']['T0']             = parameters['General']['T0']
    parameters['Epsilon']['TM']             = parameters['General']['TM']
    parameters['Magnetic_Field']['profile'] = parameters['General']['profile']
    parameters['Magnetic_Field']['gauge']   = parameters['General']['gauge']

    # Make
    device = load_device(os.path.join('.', 'input', 'Device', 'Device.h5'))
    ε      = make_epsilon(path, parameters['Epsilon'], device)
    Bz     = make_magnetic_field(path, parameters['Magnetic_Field'], device)
    Axy    = make_vector_potential(path, parameters['Magnetic_Field'], device, Bz)

    # Save
    with h5py.File(os.path.join(path, 'Setup.h5'), 'w') as file:

        # Profiles
        group = file.create_group('Profiles')
        group.create_dataset('ε', data=ε)
        group.create_dataset('Bz', data=Bz)
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
    - Device.h5

    Used by:
    - tdgl_device.TDGLDevice.make_device

    Last Updated:
    - 07/11/2026
    '''

    # Parameters
    ξM  = parameters['ξM']
    λM  = parameters['λM']
    u   = parameters['u']
    γ   = parameters['γ']
    σ   = parameters['σ']
    Lx  = parameters['Lx']
    Ly  = parameters['Ly']
    Lz  = parameters['Lz']
    NPP = parameters['NPP']

    # Geometry and Boundaries
    layer  = tdgl.Layer(coherence_length=ξM, london_lambda=λM, thickness=Lz, u=u, gamma=γ, conductivity=σ)
    film   = tdgl.Polygon('film', points=box(Lx, Ly))
    source = tdgl.Polygon('source', points=box(ξM, Ly)).translate(dx=-Lx/2)
    drain  = tdgl.Polygon('drain', points=box(ξM, Ly)).translate(dx=+Lx/2)

    # Probe Points
    line         = np.linspace(-Ly/3, Ly/3, NPP)
    probe_points = [(-Lx/3, yi) for yi in line] + [(Lx/3, yi) for yi in line]

    # Device and Mesh
    device = tdgl.Device('rectangular_film', layer=layer, film=film, terminals=[source, drain], probe_points=probe_points, length_units='um')
    device.make_mesh(max_edge_length=ξM/2)

    # Save
    device.to_hdf5(os.path.join(path, 'Device.h5'))

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

    Last Updated:
    - 08/11/2026
    '''

    # Parameters
    Lx   = parameters['Lx']
    Ly   = parameters['Ly']
    dist = parameters['dist']
    TC   = parameters['TC']
    T0   = parameters['T0']
    TM   = parameters['TM']
    N    = parameters['N']
    R    = parameters['R']
    σR   = parameters['σR']
    TD   = parameters['TD']
    σTD  = parameters['σTD']
    seed = parameters['seed']

    # Mesh
    points = device.points
    X, Y   = points[:, 0], points[:, 1]

    # Critical Temperature
    Tc = np.full(X.shape, TC)

    # Defects
    if (N > 0):

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
        r   = rng.lognormal(np.log(R), σR, Xp.shape)
        TDs = rng.normal(TD, σTD, Xp.shape)
        TDs = np.clip(TDs, 0.0, None)

        # Critical Temperature
        d     = np.sqrt((Xp - X)**2 + (Yp - Y)**2)
        gauss = (TDs - TC) * np.exp(-(d**2 / (2*r**2)))
        Tc    = np.clip(TC + gauss.sum(axis=0), 0.0, None)

    # Epsilon
    ε = (1 - (T0/Tc)**2) / (1 - (TM/TC)**2)
    ε = np.clip(ε, -1.0, None)

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

    Last Updated:
    - 01/08/2026
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

    Last Updated:
    - 01/08/2026
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