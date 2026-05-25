# Run
from programs.base.physics import get_voltage
from programs.utils import *
import tdgl

#------------------------------------------------------------------------------------------------------------------------------------------------------------

# Point
def point(path, simulation, parameters, device, Axy, current, seed_solution):
    '''
    Run the TDGL solve in Static/Dynamic mode.

    Input:
    -                        path (str): Output Folder Path
    -                  simulation (str): Simulation Mode
    - parameters ((str, ?), dict[?, ?]): Parameters
    -              device (tdgl.Device): TDGL Device
    -                    Axy (callable): xy-Vector Potential
    -                   current (float): Transport Current
    -     seed_solution (tdgl.Solution): Seed Solution

    Output:
    -          solution (tdgl.Solution): TDGL Solution
    -                   voltage (float): Voltage
    
    Used by:
    - base.run.sweep
    - tdgl_simulation.TDGLSimulation.point
    '''

    # Parameters
    solve_time = parameters['solve_time']
    save_every = parameters['save_every']
    skip_time  = parameters['skip_time'] if ((seed_solution is None) and (simulation != 'Static')) else 0
    dt_init    = parameters['dt_init']
    dt_max     = parameters['dt_max']
    screening  = parameters['screening']
    gpu        = parameters['gpu']
    I          = current

    # Solve
    options  = tdgl.SolverOptions(solve_time=solve_time, save_every=save_every, skip_time=skip_time, dt_init=dt_init, dt_max=dt_max,
                                  output_file=os.path.join(path, 'Solution.h5'), field_units='mT', current_units='uA', include_screening=screening, gpu=gpu)
    solution = tdgl.solve(device, options, applied_vector_potential=Axy, terminal_currents={'source':I, 'drain':-I}, seed_solution=seed_solution)
    voltage  = get_voltage(solution)

    return solution, voltage

#------------------------------------------------------------------------------------------------------------------------------------------------------------

# Sweep
def sweep(path, simulation, parameters, device, Axy, currents, seed):
    '''
    Run the TDGL solve in Sweep mode.

    Input:
    -                            path (str): Output Folder Path
    -                      simulation (str): Simulation Mode
    -     parameters ((str, ?), dict[?, ?]): Parameters
    -                  device (tdgl.Device): TDGL Device
    -                        Axy (callable): xy-Vector Potential
    -        currents (numpy.ndarray[?, 1]): Transport Currents
    -                           seed (bool): Seed Solutions

    Output:
    - solutions (tdgl.Solution, list[?, 1]): TDGL Solutions
    -        voltages (numpy.ndarray[?, 1]): Voltages

    Used by:
    - tdgl_simulation.TDGLSimulation.sweep
    '''

    # Solutions and Voltages
    seed_solution = None
    solutions     = []
    voltages      = np.zeros_like(currents)

    # Sweep
    for (i, current) in enumerate(currents):

        # Make Folder
        folder = os.path.join(path, 'Data', f'{i}')
        os.makedirs(folder, exist_ok=True)

        # Solve
        solution, voltages[i] = point(folder, simulation, parameters, device, Axy, current, seed_solution)
        solutions.append(solution)
        if (seed == True): 
            seed_solution = solution

    return solutions, voltages