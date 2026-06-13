# Animation
from programs.post.plot import plot
from programs.utils import *
from PIL import Image

#-----------------------------------------------------------------------------------------------------------------------

# Snapshots
def snapshots(path, n, solution):
    '''
    Save simulation snapshots of physical observables.

    Input:
    -                 path (str): Output Folder Path
    -                    n (int): Number Of Snapshots
    - solution (TDGL1D.Solution): TDGL1D Solution

    Output:
    - None
    - Snapshots Files
    - Snapshots Folder

    Used by:
    - tdgl1d_animation.TDGL1DAnimation.snapshots
    '''

    # Make Folder
    folder = os.path.join(path, 'Snapshots')
    os.makedirs(folder, exist_ok=True)

    # Time
    t_min, t_max = solution.data_range
    time         = np.linspace(t_min, t_max, n, dtype=int)

    # Snapshots
    for (i, ti) in enumerate(time):

        # Current Time
        solution.solve_step = ti

        # Plot
        plot(folder, solution.grid, solution.psi[ti], solution.vortex[ti], show=False, filename=f'{i:04d}')

    return None

#-----------------------------------------------------------------------------------------------------------------------

# Animation
def animation(path, n):
    '''
    Make simulation GIF of physical observables.

    Input:
    - path (str): Output Folder Path
    -    n (int): Number Of Snapshots

    Output:
    - None
    - GIF File

    Used by:
    - tdgl1d_animation.TDGL1DAnimation.animation
    '''

    # Folder
    folder = os.path.join(path, 'Snapshots')

    # Animate
    frames = [Image.open(os.path.join(folder, f'{i:04d}.{img_fmt}')) for i in range(n)]
    frames[0].save(os.path.join(path, 'Psi_Vortex.gif'), save_all=True, append_images=frames[1:], duration=200, loop=0)

    # Delete
    shutil.rmtree(folder)

    return None