# Plot
from programs.utils import *

#--------------------------------------------------------------------------------------------------------------------------------------------------------

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
    - tdgl_device.TDGLDevice.plot_device

    Last Updated:
    - 07/11/2026
    '''

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    device.plot(mesh=True, legend=False, ax=ax)
    ax.set_xlabel('$x$ [$\\mu$m]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [$\\mu$m]'); ax.set_yticks([])
    ax.set_title('Mesh')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#--------------------------------------------------------------------------------------------------------------------------------------------------------

# Plot Epsilon
def plot_epsilon(path, device, epsilon, show=True, filename='Epsilon'):
    '''
    Plot the epsilon profile.

    Input:
    -                           path (str): Output Folder Path
    -                 device (tdgl.Device): TDGL Device
    - epsilon (float, numpy.ndarray[?, 1]): Epsilon
    -                          show (bool): Show Plot
    -                       filename (str): Output Filename

    Output:
    -       fig (matplotlib.figure.Figure): Epsilon Figure

    Used by:
    - tdgl_setup.TDGLSetup.plot_epsilon

    Last Updated:
    - 06/11/2026
    '''

    # Mesh
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Profile
    ε = epsilon

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, ε, triangles=tri, cmap=cmap_eps, vmin=0, vmax=2)
    fig.colorbar(im, ax=ax, label='$\\varepsilon(x,y)$', pad=0.02, shrink=0.6, ticks=[0, 1, 2])
    ax.set_xlabel('$x$ [$\\mu$m]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [$\\mu$m]'); ax.set_yticks([])
    ax.set_title('Epsilon')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#--------------------------------------------------------------------------------------------------------------------------------------------------------

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

    Last Updated:
    - 07/11/2026
    '''

    # Mesh
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Profile
    Bz_max = np.max(np.abs(magnetic_field))
    Bz     = (magnetic_field / Bz_max) if Bz_max > 0 else magnetic_field    

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, Bz, triangles=tri, cmap=cmap_magfield, vmin=-1, vmax=1)
    fig.colorbar(im, ax=ax, label='$B_{z}(x,y)/B_{Max}$', pad=0.02, shrink=0.6, ticks=[-1, 0, 1])
    ax.set_xlabel('$x$ [$\\mu$m]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [$\\mu$m]'); ax.set_yticks([])
    ax.set_title(f'Magnetic Field - $B_{{Max}}={Bz_max:0.1f}$ mT')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#--------------------------------------------------------------------------------------------------------------------------------------------------------

# Plot Vector Potential
def plot_vector_potential(path, device, vector_potential, show=True, filename='Vector_Potential'):
    '''
    Plot the xy-vector potential amplitude profile.

    Input:
    -                                             path (str): Output Folder Path
    -                                   device (tdgl.Device): TDGL Device
    - vector_potential ((float, float), numpy.ndarray[?, 2]): xy-Vector Potential
    -                                            show (bool): Show Plot
    -                                         filename (str): Output Filename

    Output:
    -                         fig (matplotlib.figure.Figure): Vector Potential Figure

    Used by:
    - tdgl_setup.TDGLSetup.plot_vector_potential

    Last Updated:
    - 07/11/2026
    '''

    # Mesh
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Profile
    A     = np.linalg.norm(vector_potential, axis=1)
    A_max = np.max(A)
    A_amp = (A / A_max) if A_max > 0 else A

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, A_amp, triangles=tri, cmap=cmap_vecpot, vmin=0, vmax=1)
    fig.colorbar(im, ax=ax, label='$|\\vec{A}(x,y)|/A_{Max}$', pad=0.02, shrink=0.6, ticks=[0, 1])
    ax.set_xlabel('$x$ [$\\mu$m]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [$\\mu$m]'); ax.set_yticks([])
    ax.set_title(f'Vector Potential - $A_{{Max}}={A_max:0.1f}$ mT$\\cdot\\mu$m')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#--------------------------------------------------------------------------------------------------------------------------------------------------------

# Plot Psi Squared
def plot_psi_squared(path, device, psi_squared, show=True, filename='Psi_Squared'):
    '''
    Plot the squared order parameter magnitude profile.

    Input:
    -                               path (str): Output Folder Path
    -                     device (tdgl.Device): TDGL Device
    - psi_squared (float, numpy.ndarray[?, 1]): Squared Order Parameter Magnitude
    -                              show (bool): Show Plot
    -                           filename (str): Output Filename

    Output:
    -   fig (matplotlib.figure.Figure): Squared Order Parameter Magnitude Figure

    Used by:
    - tdgl_simulation.TDGLSimulation.plot_psi_squared
    - post.animation.snapshots

    Last Updated:
    - 06/11/2026
    '''

    # Mesh
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Profile
    Ψ2 = psi_squared

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, Ψ2, triangles=tri, cmap=cmap_psi_squared, vmin=0, vmax=1)
    fig.colorbar(im, ax=ax, label='$|\\psi(x,y,t)|^2$', pad=0.02, shrink=0.6, ticks=[0, 1])
    ax.set_xlabel('$x$ [$\\mu$m]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [$\\mu$m]'); ax.set_yticks([])
    ax.set_title('Psi Squared')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#--------------------------------------------------------------------------------------------------------------------------------------------------------

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

    Last Updated:
    - 06/11/2026
    '''

    # Mesh
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Profile
    φ = phase   

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, φ, triangles=tri, cmap=cmap_phase, vmin=-π, vmax=π)
    cbar = fig.colorbar(im, ax=ax, label='$\\varphi(x,y,t)$', pad=0.02, shrink=0.6, ticks=[-π, 0, π])
    cbar.set_ticklabels(['$-\\pi$', '$0$', '$\\pi$'])
    ax.set_xlabel('$x$ [$\\mu$m]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [$\\mu$m]'); ax.set_yticks([])
    ax.set_title('Phase')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#--------------------------------------------------------------------------------------------------------------------------------------------------------

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

    Last Updated:
    - 07/11/2026
    '''

    # Mesh
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Profile
    ω_max = np.max(np.abs(vorticity))
    ω     = (vorticity / ω_max) if ω_max > 0 else vorticity

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, ω, triangles=tri, cmap=cmap_vort, vmin=-1, vmax=1)
    fig.colorbar(im, ax=ax, label='$|\\omega(x,y,t)|/\\omega_{Max}(t)$', pad=0.02, shrink=0.6, ticks=[-1, 0, 1])
    ax.set_xlabel('$x$ [$\\mu$m]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [$\\mu$m]'); ax.set_yticks([])
    ax.set_title(f'Vorticity - $\\omega_{{Max}}(t)={ω_max:0.1f}$ $\\mu$A/$\\mu$m$^{2}$')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#--------------------------------------------------------------------------------------------------------------------------------------------------------

# Plot Normal Current
def plot_normal_current(path, device, normal_current, show=True, filename='Normal_Current'):
    '''
    Plot the normal current density magnitude profile.

    Input:
    -                                  path (str): Output Folder Path
    -                        device (tdgl.Device): TDGL Device
    - normal_current (float, numpy.ndarray[?, 1]): Normal Current Density Magnitude
    -                                 show (bool): Show Plot
    -                              filename (str): Output Filename

    Output:
    -              fig (matplotlib.figure.Figure): Normal Current Density Figure

    Used by:
    - tdgl_simulation.TDGLSimulation.plot_normal_current
    - post.animation.snapshots

    Last Updated:
    - 07/11/2026
    '''

    # Mesh
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Profile
    Kn_max = np.max(normal_current)
    Kn     = (normal_current / Kn_max) if Kn_max > 0 else normal_current
    Kn_log = np.log1p(Kn)/np.log(2)

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, Kn_log, triangles=tri, cmap=cmap_current, vmin=0, vmax=1)
    fig.colorbar(im, ax=ax, label='$\\log\\left(1+\\frac{|K_{n}(x,y,t)|}{K_{n}^{Max}(t)}\\right)/\\log(2)$', pad=0.02, shrink=0.6, ticks=[0, 1])
    ax.set_xlabel('$x$ [$\\mu$m]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [$\\mu$m]'); ax.set_yticks([])
    ax.set_title(f'Normal Current Density - $K_{{n}}^{{Max}}(t)$={Kn_max:0.1f} $\\mu$A/$\\mu$m')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#--------------------------------------------------------------------------------------------------------------------------------------------------------

# Plot Supercurrent
def plot_super_current(path, device, super_current, show=True, filename='Supercurrent'):
    '''
    Plot the supercurrent density magnitude profile.

    Input:
    -                                 path (str): Output Folder Path
    -                       device (tdgl.Device): TDGL Device
    - super_current (float, numpy.ndarray[?, 1]): Supercurrent Density Magnitude
    -                                show (bool): Show Plot
    -                             filename (str): Output Filename

    Output:
    -             fig (matplotlib.figure.Figure): Supercurrent Density Figure

    Used by:
    - tdgl_simulation.TDGLSimulation.plot_super_current
    - post.animation.snapshots

    Last Updated:
    - 07/11/2026
    '''

    # Mesh
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]

    # Profile
    Ks_max = np.max(super_current)
    Ks     = (super_current / Ks_max) if Ks_max > 0 else super_current
    Ks_log = np.log1p(Ks)/np.log(2)

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, Ks_log, triangles=tri, cmap=cmap_current, vmin=0, vmax=1)
    fig.colorbar(im, ax=ax, label='$\\log\\left(1+\\frac{|K_{s}(x,y,t)|}{K_{s}^{Max}(t)}\\right)/\\log(2)$', pad=0.02, shrink=0.6, ticks=[0, 1])
    ax.set_xlabel('$x$ [$\\mu$m]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [$\\mu$m]'); ax.set_yticks([])
    ax.set_title(f'Supercurrent Density - $K_{{s}}^{{Max}}(t)$={Ks_max:0.1f} $\\mu$A/$\\mu$m')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#--------------------------------------------------------------------------------------------------------------------------------------------------------

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

    Last Updated:
    - 07/11/2026
    '''

    # Mesh
    points = device.points
    tri    = device.triangles
    X, Y   = points[:, 0], points[:, 1]
    Lx     = X.max() - X.min()
    Ly     = Y.max() - Y.min()
    w      = Lx / 200

    # Profile
    μ_max = np.max(np.abs(scalar_potential))
    μ     = (scalar_potential / μ_max) if μ_max > 0 else scalar_potential

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(9, 2))

    im = ax.tripcolor(X, Y, μ, triangles=tri, cmap=cmap_scapot, vmin=-1, vmax=1)
    fig.colorbar(im, ax=ax, label='$\\mu(x,y,t)/\\mu_{Max}(t)$', pad=0.02, shrink=0.6, ticks=[-1, 0, 1])
    ax.add_patch(plt.Rectangle((-Lx/3 - w/2, -Ly/3), w, 2*Ly/3, color='black'))
    ax.add_patch(plt.Rectangle((Lx/3 - w/2, -Ly/3), w, 2*Ly/3, color='black'))
    ax.set_xlabel('$x$ [$\\mu$m]'); ax.set_xticks([])
    ax.set_ylabel('$y$ [$\\mu$m]'); ax.set_yticks([])
    ax.set_title(f'Scalar Potential - $\\mu_{{Max}}(t)$={μ_max:0.3f} mV')
    ax.set_aspect('equal')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig

#--------------------------------------------------------------------------------------------------------------------------------------------------------

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

    Last Updated:
    - 06/11/2026
    '''

    # Figure
    fig, ax = plt.subplots(1, 1, figsize=(3, 2))

    ax.plot(currents, voltages, '-o', color='gray', linewidth=lw_, markerfacecolor='white', markeredgecolor='gray', markeredgewidth=me_, markersize=ms_)
    ax.set_xlabel('Current [$\\mu$A]')
    ax.set_ylabel('Voltage [mV]')

    # Save, Show, and Close
    fig.savefig(os.path.join(path, f'{filename}.{img_fmt}'))
    if (show == True): plt.show()
    plt.close(fig)

    return fig