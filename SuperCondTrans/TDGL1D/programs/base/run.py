# Run
from programs.base.make import make_vortex
from scipy.linalg import solve_banded
from programs.utils import *

#-----------------------------------------------------------------------------------------

# TDGL1D
class TDGL1D:

    # Solution
    class Solution:
        '''
        Solution.
        '''

        def __init__(self, grid, psi, vortex, times):
            '''
            Initialize attributes.
            '''

            self.grid       = grid
            self.psi        = psi
            self.vortex     = vortex
            self.times      = times
            self.solve_step = 0

        @property
        def data_range(self):
            return (0, len(self.psi)-1)

#-----------------------------------------------------------------------------------------

# Run
def run(path, parameters):
    '''
    Run the TDGL1D time evolution.

        Solves: 
        
            u·τGL·√(1+γ²f²)·∂f/∂t = ξ²·∂²f/∂y² + (1-f²)·f - V·f

        -          f → Order Parameter Magnitude
        -       u, γ → TDGL Relaxation Parameters
        -        τGL → Ginzburg-Landau Characteristic Time
        -          ξ → Ginzburg-Landau Coherence Length
        - ξ²·∂²f/∂y² → Order Parameter Laplacian
        -   (1-f²)·f → Ginzburg-Landau Non-Linear Term
        -          V → Vortex-Like Potential Profile

    Input:
    -                 path (str): Output Folder Path
    -          parameters (dict): Parameters

    Output:
    - solution (TDGL1D.Solution): TDGL1D Solution
    - Simulation.h5

    Used by:
    - tdgl1d_simulation.TDGL1DSimulation.run
    '''

    # Parameters
    Ly         = parameters['Ly']
    Ny         = parameters['Ny']
    u          = parameters['u']
    γ          = parameters['γ']
    ξ          = parameters['ξ']
    τGL        = parameters['τGL']
    dt         = parameters['dt']
    Nt         = parameters['Nt']
    save_every = parameters['save_every']

    # Grid
    y  = np.linspace(-Ly/2, Ly/2, Ny)
    dy = y[1] - y[0]

    # Physical Observables
    psi    = []
    vortex = []
    times  = []

    # Initial Condition
    f = np.ones(Ny)          

    # IMEX Constants
    α   = ξ**2 / dy**2
    off = -α * np.ones(Ny-1)

    # Solver
    for n in range(Nt):

        # Terms
        t   = n * dt                           # t
        V   = make_vortex(parameters, t, y)    # V
        τ   = u * τGL * np.sqrt(1 + γ**2*f**2) # u·τGL·√(1+γ²f²)
        rhs = (1 - f**2)*f - V*f               # (1-f²)·f - V·f

        # IMEX: (τ/dt - L)·fⁿ⁺¹ = τ/dt·fⁿ + rhs
        diag       = τ/dt + 2*α                             # Diagonal
        diag[0]    = τ[0]/dt + α                            # Neumann Bounday Conditions
        diag[-1]   = τ[-1]/dt + α                           # Neumann Bounday Conditions
        ab         = np.zeros((3, Ny))                      # Banded Format
        ab[0, 1:]  = off                                    # Upper Diagonal (-α)
        ab[1, :]   = diag                                   # Main Diagonal (τ/dt + 2α)
        ab[2, :-1] = off                                    # Lower Diagonal (-α)
        f          = solve_banded((1, 1), ab, τ/dt*f + rhs) # Solve (τ/dt - L)·fⁿ⁺¹ = rhs
        f          = np.maximum(f, 0.0)                     # Corrections (|ψ|≥0)

        # Save
        if (n % save_every == 0):
            
            psi.append(f.copy())
            vortex.append(V.copy())
            times.append(t)

    # Arrays
    grid   = y
    psi    = np.array(psi)
    vortex = np.array(vortex)
    times  = np.array(times)

    # Data Saving
    with h5py.File(os.path.join(path, 'Simulation.h5'), 'w') as file:
        
        file.create_dataset('grid', data=grid)
        file.create_dataset('psi', data=psi)
        file.create_dataset('vortex', data=vortex)
        file.create_dataset('times', data=times)

    # Solution
    solution = TDGL1D.Solution(grid, psi, vortex, times)

    return solution