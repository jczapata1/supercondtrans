# TDGL Device
from programs.base.make import read_parameters, make_device
from programs.post.plot import plot_device
from programs.utils import *

#-------------------------------------------------------------------------------------------

# TDGL Device
class TDGLDevice:
    '''
    Device.

    Last Updated:
    - 07/11/2026
    '''

    def __init__(self, folder=None):
        '''
        Initialize paths and attributes.

        Input:
        - folder (str, optional): Input Folder Path
        '''

        # Primary
        self.folder = (folder or os.path.join('.', 'input', 'Device'))
        clean(self.folder)

        # Secondary
        self.parameters = None
        self.device     = None
        self.fig_device = None

    @benchmark
    def set_parameters(self, file):
        '''Read SuperCondTrans/TDGL/programs/base/make.py/read_parameters documentation.'''
        self.parameters = read_parameters(file)
        return None

    @benchmark
    def make_device(self):
        '''Read SuperCondTrans/TDGL/programs/base/make.py/make_device documentation.'''
        self.device = make_device(self.folder, self.parameters)
        return None

    @benchmark
    def plot_device(self):
        '''Read SuperCondTrans/TDGL/programs/post/plot.py/plot_device documentation.'''
        self.fig_device = plot_device(self.folder, self.device)
        return None