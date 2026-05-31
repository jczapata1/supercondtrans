# TDGL Animation
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
    def clean(self):
        '''Read SuperCondTrans/libs/utils.py/clean documentation.'''
        clean(self.folder)
        return None