# TDGL Simulation
from programs.post.plot import plot_psi, plot_phase, plot_vorticity, plot_scalar_potential, plot_current_voltage
from programs.base.transport import set_current
from programs.base.run import point, sweep
from programs.base.load import load_setup
from programs.utils import *

#-------------------------------------------------------------------------------------------------------------------

# TDGL Simulation
class TDGLSimulation:
    '''
    Simulation.
    '''

    def __init__(self, folder=None):
        '''
        Initialize paths and attributes.

        Input:
        - folder (str, optional): Output Folder Path
        '''

        # Primary
        self.folder = (folder or os.path.join('.', 'output', 'Default'))

        # Shared
        self.parameters       = None
        self.device           = None
        self.epsilon          = None
        self.magnetic_field   = None
        self.vector_potential = None
        self.current          = None
        self.simulation       = None
        
        # Point
        self.solution             = None
        self.voltage              = None
        self.psi                  = None
        self.fig_psi              = None
        self.phase                = None
        self.fig_phase            = None
        self.vorticity            = None
        self.fig_vorticity        = None
        self.scalar_potential     = None
        self.fig_scalar_potential = None

        # Sweep
        self.solutions           = None
        self.voltages            = None
        self.fig_current_voltage = None

    @benchmark
    def load_setup(self, folder):
        '''Read SuperCondTrans/Tdgl/programs/base/load.py/load_setup documentation.'''
        self.parameters, self.device, self.epsilon, self.magnetic_field, self.vector_potential = load_setup(folder)
        return None

    @benchmark
    def set_current(self, file):
        '''Read SuperCondTrans/Tdgl/programs/base/transport.py/set_current documentation.'''
        self.current = set_current(file)
        return None

    @benchmark
    def point(self, simulation, seed_solution=None):
        '''Read SuperCondTrans/Tdgl/programs/base/run.py/point documentation.'''
        self.simulation             = simulation
        self.solution, self.voltage = point(self.folder, self.simulation, self.parameters['General'], self.device, 
                                            self.epsilon, self.vector_potential, self.current[0], seed_solution)
        return None

    @benchmark
    def sweep(self, simulation, seed=False):
        '''Read SuperCondTrans/Tdgl/programs/base/run.py/sweep documentation.'''
        self.simulation               = simulation
        self.solutions, self.voltages = sweep(self.folder, self.simulation, self.parameters['General'], self.device, 
                                              self.epsilon, self.vector_potential, self.current, seed)
        return None

    @benchmark
    def plot_psi(self):
        '''Read SuperCondTrans/Tdgl/programs/post/plot.py/plot_psi documentation.'''
        self.psi     = np.abs(self.solution.tdgl_data.psi)
        self.fig_psi = plot_psi(self.folder, self.device, self.psi)
        return None

    @benchmark
    def plot_phase(self):
        '''Read SuperCondTrans/Tdgl/programs/post/plot.py/plot_phase documentation.'''
        self.phase     = np.angle(self.solution.tdgl_data.psi)
        self.fig_phase = plot_phase(self.folder, self.device, self.phase)
        return None

    @benchmark
    def plot_vorticity(self):
        '''Read SuperCondTrans/Tdgl/programs/post/plot.py/plot_vorticity documentation.'''
        self.vorticity     = self.solution.vorticity.magnitude
        ω_max              = np.max(np.abs(self.vorticity))
        ω                  = (self.vorticity / ω_max) if ω_max > 0 else self.vorticity
        self.fig_vorticity = plot_vorticity(self.folder, self.device, ω)
        return None

    @benchmark
    def plot_scalar_potential(self):
        '''Read SuperCondTrans/Tdgl/programs/post/plot.py/plot_scalar_potential documentation.'''
        self.scalar_potential     = self.solution.tdgl_data.mu
        μ_max                     = np.max(np.abs(self.scalar_potential))
        μ                         = (self.scalar_potential / μ_max) if μ_max > 0 else self.scalar_potential
        self.fig_scalar_potential = plot_scalar_potential(self.folder, self.device, μ)
        return None

    @benchmark
    def plot_current_voltage(self):
        '''Read SuperCondTrans/Tdgl/programs/post/plot.py/plot_current_voltage documentation.'''
        self.fig_current_voltage = plot_current_voltage(self.folder, self.current, self.voltages)
        return None

    @benchmark
    def compress(self):
        '''Read SuperCondTrans/libs/utils.py/compress documentation.'''
        compress(os.path.join(self.folder, 'Data'))
        return None

    @benchmark
    def clean(self):
        '''Read SuperCondTrans/libs/utils.py/clean documentation.'''
        clean(self.folder)
        return None