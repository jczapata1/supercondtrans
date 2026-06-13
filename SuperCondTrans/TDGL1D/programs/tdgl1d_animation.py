# TDGL1D Animation
from programs.post.animation import snapshots, animation
from programs.utils import *

#--------------------------------------------------------------------------------------------

# TDGL1D Animation
class TDGL1DAnimation:
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
        self.solution = None
        self.n        = None

    @benchmark
    def snapshots(self, n=20):
        '''Read SuperCondTrans/TDGL1D/programs/post/animation.py/snapshots documentation.'''
        self.n = n
        snapshots(self.folder, self.n, self.solution)
        return None

    @benchmark
    def animation(self):
        '''Read SuperCondTrans/TDGL1D/programs/post/animation.py/animation documentation.'''
        animation(self.folder, self.n)
        return None