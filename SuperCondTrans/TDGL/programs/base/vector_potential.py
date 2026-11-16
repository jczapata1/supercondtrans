# Vector Potential
from scipy.interpolate import RegularGridInterpolator
from scipy.integrate import cumulative_trapezoid
import numpy as np

#------------------------------------------------------------------------------------------------------------------

# Vector Potential
def vector_potential(Bz_func, points, gauge):
    '''
    2D vector potential A(x,y) from a magnetic field Bz(x,y).

        Gauges:
        -                              'Landau-y' →     Ay = 0, Ax(x,y) = -∫_{y0}^{y} Bz(x,y') dy', y0 = midpoint
        -                              'Landau-x' →     Ax = 0, Ay(x,y) =  ∫_{x0}^{x} Bz(x',y) dx', x0 = midpoint
        -                               'Rotated' →     Ax = -sin(θ)G(u) - ∫_{y0}^{y} R(x,y') dy', Ay = cos(θ)G(u)
                                                      G(u) = ∫_{0}^{u} Bz(u') du', u = (x-x0)cos(θ) + (y-y0)sin(θ)
                                                    R(x,y) = Bz(x,y) - Bz(u), (x0,y0) = midpoint
                                                         θ = ½ arctan(2⟨∂xBz*∂yBz⟩/(⟨(∂xBz)²⟩-⟨(∂yBz)²⟩))

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
    - base.make.make_vector_potential

    Last Updated:
    - 16/11/2026
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

        # Gradient Direction
        dBz_dx = np.gradient(Bz, x, axis=0)
        dBz_dy = np.gradient(Bz, y, axis=1)
        θ      = 0.5 * np.arctan2(2.0*np.mean(dBz_dx*dBz_dy), np.mean(dBz_dx**2) - np.mean(dBz_dy**2))

        # Profile (Across Stripes)
        x0, y0 = 0.5*(x_min + x_max), 0.5*(y_min + y_max)
        u      = np.cos(θ) * (X - x0) + np.sin(θ) * (Y - y0)
        u1     = np.linspace(u.min(), u.max(), 4*max(Nx, Ny))
        Bz_u   = Bz_func(x0 + np.cos(θ)*u1, y0 + np.sin(θ)*u1)

        # Integration
        G_u = cumulative_trapezoid(Bz_u, u1, initial=0)
        G_u = G_u - np.interp(0.0, u1, G_u)
        G   = np.interp(u, u1, G_u)

        # Vector Potential (Along Stripes)
        Ax = -np.sin(θ) * G
        Ay =  np.cos(θ) * G

        # Residual Field
        R  = Bz - np.interp(u, u1, Bz_u)
        AR = -cumulative_trapezoid(R, y, axis=1, initial=0)
        Ax = Ax + AR - AR[:, Ny//2:Ny//2+1]

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