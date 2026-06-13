# Animation
from programs.post.plot import plot_psi, plot_phase, plot_vorticity, plot_scalar_potential, plot_normal_current, plot_super_current, plot_current_voltage
from programs.utils import *
from PIL import Image

#---------------------------------------------------------------------------------------------------------------------------------------------------------

# Snapshots
def snapshots(path, n, plot, device, solution):
    '''
    Save simulation snapshots of physical observables.

    Input:
    -               path (str): Output Folder Path
    -                  n (int): Number Of Snapshots
    -       plot (str or list): Observables to Snapshots
    -     device (tdgl.Device): TDGL Device
    - solution (TDGL.Solution): TDGL Solution

    Output:
    - None
    - Snapshots Files
    - Snapshots Folders

    Used by:
    - tdgl_animation.TDGLAnimation.snapshots
    '''

    # Validate
    valid            = ['Psi', 'Phase', 'Vorticity', 'Normal_Current', 'Super_Current', 'Scalar_Potential']
    selected_folders = valid if (plot == 'All') else ([plot] if isinstance(plot, str) else list(plot))
    invalid          = [subfolder for subfolder in selected_folders if subfolder not in valid]
    if (invalid): 
        raise ValueError(f'Invalid!. Valid Options: {valid}.')

    # Make Folders
    folder  = os.path.join(path, 'Snapshots')
    folders = {}
    for subfolder in selected_folders:
        folders[subfolder] = os.path.join(folder, subfolder)
        os.makedirs(folders[subfolder], exist_ok=True)

    # Time
    t_min, t_max = solution.data_range
    time         = np.linspace(t_min, t_max, n, dtype=int)

    # Snapshots
    for (i, ti) in enumerate(time):

        # Current Time
        solution.solve_step = ti

        # Physical Observables
        psi              = np.abs(solution.tdgl_data.psi)
        phase            = np.angle(solution.tdgl_data.psi)
        vorticity        = solution.vorticity.magnitude
        normal_current   = np.linalg.norm(solution.normal_current_density.magnitude, axis=1)
        super_current    = np.linalg.norm(solution.supercurrent_density.magnitude, axis=1)
        scalar_potential = device.V0().to('mV').magnitude  * solution.tdgl_data.mu

        # Plot
        if ('Psi' in selected_folders): 
            plot_psi(folders['Psi'], device, psi, show=False, filename=f'{i:04d}')
        if ('Phase' in selected_folders): 
            plot_phase(folders['Phase'], device, phase, show=False, filename=f'{i:04d}')
        if ('Vorticity' in selected_folders): 
            plot_vorticity(folders['Vorticity'], device, vorticity, show=False, filename=f'{i:04d}')
        if ('Normal_Current' in selected_folders): 
            plot_normal_current(folders['Normal_Current'], device, normal_current, show=False, filename=f'{i:04d}')
        if ('Super_Current' in selected_folders): 
            plot_super_current(folders['Super_Current'], device, super_current, show=False, filename=f'{i:04d}')
        if ('Scalar_Potential' in selected_folders): 
            plot_scalar_potential(folders['Scalar_Potential'], device, scalar_potential, show=False, filename=f'{i:04d}')

    return None

#---------------------------------------------------------------------------------------------------------------------------------------------------------

# Animate
def animation(path, n):
    '''
    Make simulation GIF of physical observables.

    Input:
    - path (str): Output Folder Path
    -    n (int): Number Of Snapshots

    Output:
    - None
    - Gif Files

    Used by:
    - tdgl_animation.TDGLAnimation.animation
    '''

    # Folders
    folder     = os.path.join(path, 'Snapshots')
    subfolders = sorted([subfolder for subfolder in os.listdir(folder) if os.path.isdir(os.path.join(folder, subfolder))])

    # Animate
    for subfolder in subfolders:
        frames = [Image.open(os.path.join(folder, subfolder, f'{i:04d}.{img_fmt}')) for i in range(n)]
        frames[0].save(os.path.join(path, f'{subfolder}.gif'), save_all=True, append_images=frames[1:], duration=200, loop=0)

    # Delete
    shutil.rmtree(folder)

    return None