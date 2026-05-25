# TDGL Fields
from programs.base.initialize import read_parameters, make_magnetic_field, make_vector_potential
from programs.post.plot import plot_magnetic_field, plot_vector_potential
from programs.base.load import load_device
from programs.utils import *

#----------------------------------------------------------------------------------------------------------------

# TDGL Fields
class TDGLFields:
    '''
    Magnetic Field and Vector Potential.
    '''

    def __init__(self, folder=None):
        '''
        Initialize paths and attributes.

        Input:
        - folder (str, optional): Input Folder Path
        '''

        # Primary
        self.folder = (folder or os.path.join('.', 'input', 'Default'))

        # Secondary
        self.parameters            = None
        self.device                = None
        self.profile               = None
        self.magnetic_field        = None
        self.gauge                 = None        
        self.vector_potential      = None
        self.fig_magnetic_field    = None
        self.fig_vector_potential  = None

    @benchmark
    def read_parameters(self, file):
        '''Read SuperCondTrans/Tdgl/programs/base/initialize.py/read_parameters documentation.'''
        self.parameters = read_parameters(file)
        return None

    @benchmark
    def load_device(self, file):
        '''Read SuperCondTrans/Tdgl/programs/base/load.py/load_device documentation.'''        
        self.device = load_device(file)        
        return None

    @benchmark
    def make_magnetic_field(self, profile):
        '''Read SuperCondTrans/Tdgl/programs/base/initialize.py/make_magnetic_field documentation.'''    
        self.profile        = profile
        self.magnetic_field = make_magnetic_field(self.folder, self.profile, self.parameters, self.device)
        return None

    @benchmark
    def make_vector_potential(self, gauge):
        '''Read SuperCondTrans/Tdgl/programs/base/initialize.py/make_vector_potential documentation.'''    
        self.gauge            = gauge
        self.vector_potential = make_vector_potential(self.folder, self.gauge, self.device, self.magnetic_field)
        return None

    @benchmark
    def plot_magnetic_field(self):
        '''Read SuperCondTrans/Tdgl/programs/post/plot.py/plot_magnetic_field documentation.''' 
        Bz_max                  = np.max(np.abs(self.magnetic_field))
        Bz                      = (self.magnetic_field / Bz_max) if Bz_max > 0 else self.magnetic_field
        self.fig_magnetic_field = plot_magnetic_field(self.folder, self.device, Bz)
        return None

    @benchmark
    def plot_vector_potential(self):
        '''Read SuperCondTrans/Tdgl/programs/post/plot.py/plot_vector_potential documentation.'''
        A     = np.sqrt(self.vector_potential[:, 0]**2 + self.vector_potential[:, 1]**2)
        A_max = np.max(A)
        A_amp = (A / A_max) if A_max > 0 else A
        self.fig_vector_potential = plot_vector_potential(self.folder, self.device, A_amp)
        return None

    @benchmark
    def clean(self):
        '''Read SuperCondTrans/libs/utils.py/clean documentation.'''
        clean(self.folder)
        return None