# TDGL Animation
from programs.base.load import load_device, load_solution
from programs.post.animation import snapshots, animation
from programs.utils import *

#-----------------------------------------------------------------------------------------

# TDGL Animation
class TDGLAnimation:
    '''
    Animation.
    '''

    def __init__(self, folder=None):
        '''
        Initialize paths and attributes.

        Input:
        - folder (str, optional): Output Folder Path
        '''

        # Primary
        self.folder = (folder or os.path.join('.', 'output', 'Default'))

        # Secondary
        self.device   = None
        self.solution = None
        self.n        = None

    @benchmark
    def load_device(self, file):
        '''Read SuperCondTrans/Tdgl/programs/base/load.py/load_device documentation.'''
        self.device = load_device(file)
        return None
        
    @benchmark
    def load_solution(self, file):
        '''Read SuperCondTrans/Tdgl/programs/base/load.py/load_solution documentation.'''
        self.solution = load_solution(file)
        return None

    @benchmark
    def snapshots(self, n=20, plot='All'):
        '''Read SuperCondTrans/Tdgl/programs/post/animation.py/snapshots documentation.'''
        self.n = n
        snapshots(self.folder, self.n, plot, self.device, self.solution)
        return None

    @benchmark
    def animation(self):
        '''Read SuperCondTrans/Tdgl/programs/post/animation.py/animation documentation.'''
        animation(self.folder, self.n)
        return None
        
    @benchmark
    def compress(self):
        '''Read SuperCondTrans/libs/utils.py/compress documentation.'''
        compress(os.path.join(self.folder, 'Snapshots'))
        return None

    @benchmark
    def clean(self):
        '''Read SuperCondTrans/libs/utils.py/clean documentation.'''
        clean(self.folder)
        return None