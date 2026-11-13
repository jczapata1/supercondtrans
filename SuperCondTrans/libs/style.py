# Style
# Last Updated: 09/11/2026
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import shutil

#--------------------------------------------------------------------------------------------------------------------

# Linewidth
lw_ = 1.3

# Fontsize
fs0_ = 5.0  # ---
fs1_ = 6.5  # Legend, Title, Ticks
fs2_ = 7.5  # Labels, Text
fs3_ = 10.0 # ---

# Markers
me_ = 1.5 # Edgewidth
ms_ = 3.0 # Size

# Opacity
alp1_ = 0.3 # Grid
alp2_ = 0.2 # Vertical/Horizontal Lines
alp3_ = 1.0 # Default
alp4_ = 0.5 # Lines

# Colors
color_NbN = 'seagreen'
color_1   = 'navy'
color_2   = 'brown'

# Colormaps
cmap_eps         = 'RdBu'
cmap_magfield    = 'copper'
cmap_vecpot      = 'copper'
cmap_psi_squared = 'jet_r'
cmap_phase       = 'afmhot'
cmap_vort        = 'RdBu_r'
cmap_current     = 'inferno'
cmap_scapot      = 'BrBG_r'

# Font
plt.rcParams['text.usetex']         = (shutil.which('latex') is not None) and (shutil.which('dvipng') is not None)
plt.rcParams['font.family']         = 'serif'
plt.rcParams['text.latex.preamble'] = r'\usepackage[T1]{fontenc}\usepackage[light, math]{iwona}\usepackage{amsmath}'
plt.rcParams['font.size']           = fs2_ 
plt.rcParams['figure.titlesize']    = fs2_
plt.rcParams['figure.labelsize']    = fs2_

# Axes
plt.rcParams['axes.titlesize'] = fs2_
plt.rcParams['axes.labelsize'] = fs2_
plt.rcParams['axes.linewidth'] = 1.0

# Ticks
plt.rcParams['xtick.labelsize']   = fs1_
plt.rcParams['ytick.labelsize']   = fs1_
plt.rcParams['xtick.bottom']      = True
plt.rcParams['xtick.top']         = True
plt.rcParams['ytick.left']        = True
plt.rcParams['ytick.right']       = True
plt.rcParams['xtick.direction']   = 'in'
plt.rcParams['ytick.direction']   = 'in'
plt.rcParams['xtick.color']       = 'black'
plt.rcParams['ytick.color']       = 'black'
plt.rcParams['xtick.labelcolor']  = 'black'
plt.rcParams['ytick.labelcolor']  = 'black'
plt.rcParams['xtick.major.size']  = 4
plt.rcParams['ytick.major.size']  = 4
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0

# Legend
plt.rcParams['legend.fontsize']      = fs1_
plt.rcParams['legend.frameon']       = True
plt.rcParams['legend.facecolor']     = 'white'
plt.rcParams['legend.edgecolor']     = 'none'
plt.rcParams['legend.framealpha']    = 1
plt.rcParams['legend.handletextpad'] = 0.4

# Grid
plt.rcParams['axes.grid']  = False
plt.rcParams['grid.alpha'] = alp1_

# Save Figure
img_fmt                            = 'jpg'
plt.rcParams['savefig.bbox']       = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.2
plt.rcParams['savefig.dpi']        = 300