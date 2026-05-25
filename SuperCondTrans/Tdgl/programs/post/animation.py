# Animation
from programs.post.plot import plot_psi, plot_phase, plot_vorticity, plot_scalar_potential
from programs.utils import *
from PIL import Image

#----------------------------------------------------------------------------------------------------------------------------------------------------

# Snapshots
def snapshots(path, n, plot, device, solution):
    '''
    Save simulation snapshots of physical observables.

    Input:
    -               path (str): Output Folder Path
    -                  n (int): Number Of Snapshots
    -       plot (str or list): Observables to Snapshots
    -     device (tdgl.Device): TDGL Device
    - solution (tdgl.Solution): TDGL Solution

    Output:
    - None
    - Snapshots Files
    - Snapshots Folders

    Used by:
    - tdgl_animation.TDGLAnimation.snapshots
    '''

    # Validate
    valid            = ['Psi', 'Phase', 'Vorticity', 'Scalar_Potential']
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

    # Global Normalization
    ω_max = 1.0
    μ_max = 1.0
    for ti in time:
        solution.solve_step = ti
        
        if ('Vorticity' in selected_folders): 
            ω_max = max(ω_max, np.max(np.abs(solution.vorticity.magnitude)))
        if ('Scalar_Potential' in selected_folders): 
            μ_max = max(μ_max, np.max(np.abs(solution.tdgl_data.mu)))

    # Plots
    plotters = {
        'Psi': lambda folder, i: plot_psi(folder, device, np.abs(solution.tdgl_data.psi), show=False, filename=f'{i:03d}'),
        'Phase': lambda folder, i: plot_phase(folder, device, np.angle(solution.tdgl_data.psi), show=False, filename=f'{i:03d}'),
        'Vorticity': lambda folder, i: plot_vorticity(folder, device, solution.vorticity.magnitude / ω_max, show=False, filename=f'{i:03d}'),
        'Scalar_Potential': lambda folder, i: plot_scalar_potential(folder, device, solution.tdgl_data.mu / μ_max, show=False, filename=f'{i:03d}'),
    }

    # Snapshots
    for (i, ti) in enumerate(time):
        solution.solve_step = ti

        for subfolder in selected_folders:
            plotters[subfolder](folders[subfolder], i)

    return None

#----------------------------------------------------------------------------------------------------------------------------------------------------

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
        frames    = [Image.open(os.path.join(folder, subfolder, f'{i:03d}.{img_fmt}')) for i in range(n)]
        frames[0].save(os.path.join(path, f'{subfolder}.gif'), save_all=True, append_images=frames[1:], duration=250, loop=0)

    return None