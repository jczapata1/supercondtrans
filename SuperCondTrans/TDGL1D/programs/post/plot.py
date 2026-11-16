# Plot
from programs.utils import *

#-----------------------------------------------------------------------------------------------------------

# Plot
def plot(path, grid, psi, vortex, show=True, filename='Psi_Squared_Vortex'):
    '''
    Plot the squared order parameter magnitude and vortex-like potential profiles.

    Input:
    -                          path (str): Output Folder Path
    -   grid (float, numpy.ndarray[?, 1]): Grid
    -    psi (float, numpy.ndarray[?, 1]): Order Parameter Magnitude
    - vortex (float, numpy.ndarray[?, 1]): Normalized Potential
    -                         show (bool): Show Plot
    -                      filename (str): Output Filename

    Output:
    -      fig (matplotlib.figure.Figure): Psi Squared-Vortex Figure

    Used by:
    - tdgl1d_simulation.TDGL1DSimulation.plot
    - post.animation.snapshots

    Last Updated:
    - 16/11/2026
    '''

    # Mesh
    y  = grid
    Ly = grid.max()

    # Profile
    Ψ2 = psi**2
    V0 = np.max(np.abs(vortex))
    V  = (vortex / V0) if V0 > 0 else vortex

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    ax.plot(y, Ψ2, color='black', lw=lw_, label='$|\\psi|^2$')
    ax.plot(y, V, color='red', lw=lw_, label='Vortex')
    ax.set_xlabel('$y$'); ax.set_xlim(min(y), max(y))
    ax.set_xticks([-Ly, -Ly/2, 0, Ly/2, Ly], ['$-L_{y}/2$', '$-L_{y}/4$', '$0$', '$L_{y}/4$', '$L_{y}/2$'])
    ax.set_ylabel('$|\\psi(y,t)|^2$'); ax.set_ylim(-0.05, 1.05)
    ax.set_yticks([0, 1/4, 2/4, 3/4, 1], ['$0$', '$1/4$', '$1/2$', '$3/4$', '$1$'])
    ax.set_title('Psi Squared')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig