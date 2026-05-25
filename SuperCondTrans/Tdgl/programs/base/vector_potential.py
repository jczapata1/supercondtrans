# Vector Potential
from scipy.interpolate import RegularGridInterpolator
from scipy.integrate import cumulative_trapezoid
import numpy as np

#------------------------------------------------------------------------------------------------------------------------

# Vector Potential
def vector_potential(Bz_func, points, gauge):
    '''
    2D vector potential A(x,y) from a magnetic field Bz(x,y).

        Gauges:
        -                              'Landau-y' →  Ay = 0, Ax(x,y) = -∫_{y0}^{y} Bz(x,y') dy', y0 = midpoint
        -                              'Landau-x' →  Ax = 0, Ay(x,y) =  ∫_{x0}^{x} Bz(x',y) dx', x0 = midpoint
        -                               'Rotated' → Ay' = 0, Ax'(x',y') = -∫_{y0'}^{y'} Bz(x',y'') dy'', y0' = midpoint,
                                                      θ = arctan(⟨|∂Bz/∂y|⟩/⟨|∂Bz/∂x|⟩), Ax = cos(θ)Ax', Ay = sin(θ)Ax'

        Gauge Selection:
        -                              Bz = Bz(y) → 'Landau-y' (Uniform, Plateau, and Domains θ=0)
        -                              Bz = Bz(x) → 'Landau-x' (Domains θ=π/2)
        -                            Bz = Bz(x,y) → 'Rotated'  (θ Arbitrary)

    Input:
    -                           Bz_func (callable): z-Magnetic Field
    - points ((float, float), numpy.ndarray[?, 2]): Mesh Points
    -                                  gauge (str): Gauge

    Output:
    -                          Axy_func (callable): xy-Vector Potential

    Used by:
    - base.initialize.make_vector_potential
    '''

    # Auxiliary Grid
    Nx           = 2560
    Ny           = 512
    x_min, x_max = points[:, 0].min(), points[:, 0].max()
    y_min, y_max = points[:, 1].min(), points[:, 1].max()
    x            = np.linspace(x_min, x_max, Nx)
    y            = np.linspace(y_min, y_max, Ny)
    X, Y         = np.meshgrid(x, y, indexing='ij')
    Bz           = Bz_func(X, Y)

    # Compute Vector Potential
    if (gauge == 'Landau-y'):

        # Integration
        Ax = -cumulative_trapezoid(Bz, y, axis=1, initial=0)
        Ax = Ax - Ax[:, Ny//2:Ny//2+1]
        Ay = np.zeros_like(Bz)

    elif (gauge == 'Landau-x'):

        # Integration
        Ay = cumulative_trapezoid(Bz, x, axis=0, initial=0)
        Ay = Ay - Ay[Nx//2:Nx//2+1, :]
        Ax = np.zeros_like(Bz)
        
    elif (gauge == 'Rotated'):

        # Rotate
        dBz_dx = np.gradient(Bz, x, axis=0)
        dBz_dy = np.gradient(Bz, y, axis=1)
        θ      = np.arctan2(np.mean(np.abs(dBz_dy)), np.mean(np.abs(dBz_dx)))
        X_r    =  np.cos(θ) * X + np.sin(θ) * Y
        Y_r    = -np.sin(θ) * X + np.cos(θ) * Y
        Bz_r   = Bz_func(X_r, Y_r)

        # Integration
        Ax_r = -cumulative_trapezoid(Bz_r, y, axis=1, initial=0)
        Ax_r = Ax_r - Ax_r[:, Ny//2:Ny//2+1]
        Ay_r = np.zeros_like(Ax_r)

        # Rotate Back
        Ax = np.cos(θ) * Ax_r
        Ay = np.sin(θ) * Ax_r

    else:
        raise ValueError(f"Unknown Gauge!. Use 'Landau-y', 'Landau-x', or 'Rotated'.")

    # Interpolators
    Ax_int = RegularGridInterpolator((x, y), Ax, method='linear', bounds_error=True, fill_value=None)
    Ay_int = RegularGridInterpolator((x, y), Ay, method='linear', bounds_error=True, fill_value=None)

    # Vector Potential
    def Axy_func(x, y, z=None):
        pts = np.column_stack([x, y])
        Axy = np.stack([Ax_int(pts), Ay_int(pts)], axis=-1)
        return Axy

    return Axy_func