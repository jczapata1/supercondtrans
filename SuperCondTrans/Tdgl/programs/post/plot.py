# Plot
from programs.utils import *

#-------------------------------------------------------------------------------------------------------------

# Plot Device
def plot_device(path, device, show=True, filename='Device'):
    '''
    Plot the device mesh profile.

    Input:
    -                     path (str): Output Folder Path
    -           device (tdgl.Device): TDGL Device
    -                    show (bool): Show Plot
    -                 filename (str): Output Filename

    Output:
    - fig (matplotlib.figure.Figure): Device Figure

    Used by:
    - tdgl_setup.TDGLSetup.plot_device
    '''

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    device.plot(mesh=True, legend=False, ax=ax)
    ax.set_xlabel('$x$ [μm]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [μm]'); ax.set_yticks([])
    ax.set_title('Mesh')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#-------------------------------------------------------------------------------------------------------------

# Plot Epsilon
def plot_epsilon(path, device, epsilon, show=True, filename='Epsilon'):
    '''
    Plot the epsilon profile.

    Input:
    -                           path (str): Output Folder Path
    -                 device (tdgl.Device): TDGL Device
    - epsilon (float, numpy.ndarray[?, 1]): Epsilon Profile
    -                          show (bool): Show Plot
    -                       filename (str): Output Filename

    Output:
    -       fig (matplotlib.figure.Figure): Epsilon Figure

    Used by:
    - tdgl_setup.TDGLSetup.plot_epsilon
    '''

    # Data
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, epsilon, triangles=tri, cmap=cmap_eps, vmin=0, vmax=2)
    fig.colorbar(im, ax=ax, label='$\\varepsilon(x,y)$', pad=0.02, shrink=0.6, ticks=[0, 1, 2])
    ax.set_xlabel('$x$ [μm]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [μm]'); ax.set_yticks([])
    ax.set_title('Epsilon')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#-------------------------------------------------------------------------------------------------------------

# Plot Magnetic Field
def plot_magnetic_field(path, device, magnetic_field, show=True, filename='Magnetic_Field'):
    '''
    Plot the z-magnetic field profile.

    Input:
    -                                  path (str): Output Folder Path
    -                        device (tdgl.Device): TDGL Device
    - magnetic_field (float, numpy.ndarray[?, 1]): z-Magnetic Field
    -                                 show (bool): Show Plot
    -                              filename (str): Output Filename

    Output:
    -              fig (matplotlib.figure.Figure): Magnetic Field Figure

    Used by:
    - tdgl_setup.TDGLSetup.plot_magnetic_field
    '''

    # Data
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, magnetic_field, triangles=tri, cmap=cmap_magfield, vmin=-1, vmax=1)
    fig.colorbar(im, ax=ax, label='$B_{z}(x,y)/B_{max}$', pad=0.02, shrink=0.6, ticks=[-1, 0, 1])
    ax.set_xlabel('$x$ [μm]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [μm]'); ax.set_yticks([])
    ax.set_title('Magnetic Field')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#-------------------------------------------------------------------------------------------------------------

# Plot Vector Potential
def plot_vector_potential(path, device, vector_potential, show=True, filename='Vector_Potential'):
    '''
    Plot the xy-vector potential amplitude profile.

    Input:
    -                                    path (str): Output Folder Path
    -                          device (tdgl.Device): TDGL Device
    - vector_potential (float, numpy.ndarray[?, 1]): xy-Vector Potential Amplitude
    -                                   show (bool): Show Plot
    -                                filename (str): Output Filename

    Output:
    -                fig (matplotlib.figure.Figure): Vector Potential Figure

    Used by:
    - tdgl_setup.TDGLSetup.plot_vector_potential
    '''

    # Data
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, vector_potential, triangles=tri, cmap=cmap_vecpot, vmin=0, vmax=1)
    fig.colorbar(im, ax=ax, label='$|\\vec{A}(x,y)|/A_{max}$', pad=0.02, shrink=0.6, ticks=[0, 1])
    ax.set_xlabel('$x$ [μm]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [μm]'); ax.set_yticks([])
    ax.set_title('Vector Potential')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#-------------------------------------------------------------------------------------------------------------

# Plot Psi
def plot_psi(path, device, psi, show=True, filename='Psi'):
    '''
    Plot the order parameter magnitude profile.

    Input:
    -                       path (str): Output Folder Path
    -             device (tdgl.Device): TDGL Device
    - psi (float, numpy.ndarray[?, 1]): Order Parameter Magnitude
    -                      show (bool): Show Plot
    -                   filename (str): Output Filename

    Output:
    -   fig (matplotlib.figure.Figure): Order Parameter Magnitude Figure

    Used by:
    - tdgl_simulation.TDGLSimulation.plot_psi
    - post.animation.snapshots
    '''

    # Data
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, psi, triangles=tri, cmap=cmap_psi, vmin=0, vmax=1)
    fig.colorbar(im, ax=ax, label='$|\\psi(x,y,t)|$', pad=0.02, shrink=0.6, ticks=[0, 1])
    ax.set_xlabel('$x$ [μm]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [μm]'); ax.set_yticks([])
    ax.set_title('Psi')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#-------------------------------------------------------------------------------------------------------------

# Plot Phase
def plot_phase(path, device, phase, show=True, filename='Phase'):
    '''
    Plot the order parameter phase profile.

    Input:
    -                         path (str): Output Folder Path
    -               device (tdgl.Device): TDGL Device
    - phase (float, numpy.ndarray[?, 1]): Order Parameter Phase
    -                        show (bool): Show Plot
    -                     filename (str): Output Filename

    Output:
    -     fig (matplotlib.figure.Figure): Order Parameter Phase Figure

    Used by:
    - tdgl_simulation.TDGLSimulation.plot_phase
    - post.animation.snapshots
    '''

    # Data
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, phase, triangles=tri, cmap=cmap_phase, vmin=-π, vmax=π)
    cbar = fig.colorbar(im, ax=ax, label='$\\varphi(x,y,t)$', pad=0.02, shrink=0.6, ticks=[-π, 0, π])
    cbar.set_ticklabels(['$-\\pi$', '$0$', '$\\pi$'])
    ax.set_xlabel('$x$ [μm]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [μm]'); ax.set_yticks([])
    ax.set_title('Phase')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#-------------------------------------------------------------------------------------------------------------

# Plot Vorticity
def plot_vorticity(path, device, vorticity, show=True, filename='Vorticity'):
    '''
    Plot the vorticity magnitude profile.

    Input:
    -                             path (str): Output Folder Path
    -                   device (tdgl.Device): TDGL Device
    - vorticity (float, numpy.ndarray[?, 1]): Vorticity Magnitude
    -                            show (bool): Show Plot
    -                         filename (str): Output Filename

    Output:
    -         fig (matplotlib.figure.Figure): Vorticity Figure

    Used by:
    - tdgl_simulation.TDGLSimulation.plot_vorticity
    - post.animation.snapshots
    '''

    # Data
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, vorticity, triangles=tri, cmap=cmap_vort, vmin=-1, vmax=1)
    fig.colorbar(im, ax=ax, label='$|\\omega(x,y,t)|/\\omega_{max}$', pad=0.02, shrink=0.6, ticks=[-1, 0, 1])
    ax.set_xlabel('$x$ [μm]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [μm]'); ax.set_yticks([])
    ax.set_title('Vorticity')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#-------------------------------------------------------------------------------------------------------------

# Plot Scalar Potential
def plot_scalar_potential(path, device, scalar_potential, show=True, filename='Scalar_Potential'):
    '''
    Plot the scalar potential profile.

    Input:
    -                                    path (str): Output Folder Path
    -                          device (tdgl.Device): TDGL Device
    - scalar_potential (float, numpy.ndarray[?, 1]): Scalar Potential
    -                                   show (bool): Show Plot
    -                                filename (str): Output Filename

    Output:
    -                fig (matplotlib.figure.Figure): Scalar Potential Figure

    Used by:
    - tdgl_simulation.TDGLSimulation.plot_scalar_potential
    - post.animation.snapshots
    '''

    # Data
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]
    Lx     = X.max() - X.min()
    Ly     = Y.max() - Y.min()
    w      = Lx / 200

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, scalar_potential, triangles=tri, cmap=cmap_scapot, vmin=-1, vmax=1)
    fig.colorbar(im, ax=ax, label='$\\mu(x,y,t)/\\mu_{max}$', pad=0.02, shrink=0.6, ticks=[-1, 0, 1])
    ax.add_patch(plt.Rectangle((-Lx/3 - w/2, -Ly/3), w, 2*Ly/3, color='black'))
    ax.add_patch(plt.Rectangle((Lx/3 - w/2, -Ly/3), w, 2*Ly/3, color='black'))
    ax.set_xlabel('$x$ [μm]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [μm]'); ax.set_yticks([])
    ax.set_title('Scalar Potential')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#-------------------------------------------------------------------------------------------------------------

# Plot Current-Voltage
def plot_current_voltage(path, currents, voltages, show=True, filename='Current_Voltage'):
    '''
    Plot the current-voltage profile.

    Input:
    -                            path (str): Output Folder Path
    - currents (float, numpy.ndarray[?, 1]): Currents
    - voltages (float, numpy.ndarray[?, 1]): Voltages
    -                           show (bool): Show Plot
    -                        filename (str): Output Filename

    Output:
    -        fig (matplotlib.figure.Figure): Current-Voltage Figure

    Used by:
    - tdgl_simulation.TDGLSimulation.plot_current_voltage
    '''

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(3, 2))

    ax.scatter(currents, voltages, color='black', s=10, marker='o', facecolors='none')
    ax.set_xlabel('Current [μA]')
    ax.set_ylabel('Voltage [mV]')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig