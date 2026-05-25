# Physics
from programs.base.initialize import read_parameters
from programs.utils import *

#-------------------------------------------------------------------------------------------

# Set Current
def set_current(path):
    '''
    Generate linear transport current.

    Input:
    -                           path (str): Input File Path

    Output:
    - current (float, numpy.ndarray[?, 1]): Transport Current

    Used by:
    - tdgl_simulation.TDGLSimulation.set_current
    '''

    # Parameters
    parameters = read_parameters(path) # Read
    Ii         = parameters['Ii']      # Initial Transport Current
    If         = parameters['If']      # Final Transport Current
    N          = parameters['N']       # Number of Points

    # Transport Current
    current = np.linspace(Ii, If, N)

    return current

#-------------------------------------------------------------------------------------------

# Get Voltage
def get_voltage(solution):
    '''
    Get time-averaged voltage between line probes.

    Input:
    - solution (tdgl.Solution): TDGL Solution

    Output:
    -          voltage (float): Voltage

    Used by:
    - base.run.point
    '''

    # Voltage
    V0       = solution.device.V0().to('mV').magnitude                      # Scale
    N        = len(solution.device.probe_points) // 2                       # Points
    dynamics = solution.dynamics                                            # Dynamics
    time     = dynamics.time[-1] / 2                                        # Time
    voltages = [dynamics.mean_voltage(i, i+N, tmin=time) for i in range(N)] # Pair Voltages
    voltage  = V0 * np.mean(voltages)

    return voltage