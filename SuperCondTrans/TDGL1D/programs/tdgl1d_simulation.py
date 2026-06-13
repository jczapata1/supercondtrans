# TDGL1D Simulation
from programs.base.make import read_parameters
from programs.post.plot import plot
from programs.base.run import run
from programs.utils import *

#---------------------------------------------------------------------------------------------

# TDGL1D Simulation
class TDGL1DSimulation:
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
        clean(self.folder)

        # Secondary
        self.parameters = None
        self.grid       = None
        self.solution   = None
        self.psi        = None
        self.vortex     = None
        self.fig        = None

    @benchmark
    def read_parameters(self, file):
        '''Read SuperCondTrans/TDGL1D/programs/base/make.py/read_parameters documentation.'''
        self.parameters = read_parameters(file)
        return None

    @benchmark
    def run(self):
        '''Read SuperCondTrans/TDGL1D/programs/base/run.py/run documentation.'''
        self.solution = run(self.folder, self.parameters)
        return None

    @benchmark
    def plot(self):
        '''Read SuperCondTrans/TDGL1D/programs/post/plot.py/plot documentation.'''
        self.grid   = self.solution.grid
        self.psi    = self.solution.psi[-1]
        self.vortex = self.solution.vortex[-1]
        self.fig    = plot(self.folder, self.grid, self.psi, self.vortex)
        return None