# TDGL Setup
from programs.post.plot import plot_device, plot_epsilon, plot_magnetic_field, plot_vector_potential
from programs.base.make import set_parameters, make_setup
from programs.utils import *

#------------------------------------------------------------------------------------------------------------------------

# TDGL Setup
class TDGLSetup:
    '''
    Device, Epsilon, Magnetic Field, and Vector Potential.
    '''

    def __init__(self, folder=None):
        '''
        Initialize paths and attributes.

        Input:
        - folder (str, optional): Input Folder Path
        '''

        # Primary
        self.folder = (folder or os.path.join('.', 'input', 'Default'))
        clean(self.folder)

        # Secondary
        self.parameters           = None    
        self.device               = None
        self.epsilon              = None
        self.magnetic_field       = None    
        self.vector_potential     = None
        self.fig_device           = None
        self.fig_epsilon          = None
        self.fig_magnetic_field   = None
        self.fig_vector_potential = None

    @benchmark
    def set_parameters(self, file):
        '''Read SuperCondTrans/TDGL/programs/base/make.py/set_parameters documentation.'''
        self.parameters = set_parameters(file)
        return None

    @benchmark
    def make_setup(self):
        '''Read SuperCondTrans/TDGL/programs/base/make.py/make_setup documentation.'''
        self.device, self.epsilon, self.magnetic_field, self.vector_potential = make_setup(self.folder, self.parameters)
        return None

    @benchmark
    def plot_device(self):
        '''Read SuperCondTrans/TDGL/programs/post/plot.py/plot_device documentation.'''
        self.fig_device = plot_device(self.folder, self.device)
        return None

    @benchmark
    def plot_epsilon(self):
        '''Read SuperCondTrans/TDGL/programs/post/plot.py/plot_epsilon documentation.'''
        self.fig_epsilon = plot_epsilon(self.folder, self.device, self.epsilon)
        return None

    @benchmark
    def plot_magnetic_field(self):
        '''Read SuperCondTrans/TDGL/programs/post/plot.py/plot_magnetic_field documentation.''' 
        self.fig_magnetic_field = plot_magnetic_field(self.folder, self.device, self.magnetic_field)
        return None

    @benchmark
    def plot_vector_potential(self):
        '''Read SuperCondTrans/TDGL/programs/post/plot.py/plot_vector_potential documentation.'''       
        self.fig_vector_potential = plot_vector_potential(self.folder, self.device, self.vector_potential)
        return None