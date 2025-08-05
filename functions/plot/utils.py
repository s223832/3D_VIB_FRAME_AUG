import matplotlib.pyplot as plt
import numpy as np

def plotSettings(fig=None): 
    plt.rc('lines', markersize=4)       # Set default marker size for lines
    plt.rc('lines', linewidth=1)        # Set default line width
    plt.rc('font', size=10)             # Controls default text sizes
    plt.rc('font', family="Times New Roman")      # Set default font family   
    plt.rc('axes', titlesize=10)        # Fontsize of the axes title
    plt.rc('axes', labelsize=10)        # Fontsize of the x, y and z labels
    plt.rc('xtick', labelsize=10)       # Fontsize of the tick labels
    plt.rc('ytick', labelsize=10)       # Fontsize of the tick labels
    plt.rc('legend', fontsize=10)       # Legend fontsize
    plt.rc('figure', titlesize=10)      # Fontsize of the figure title
    return fig

def plotStructure(X,C,fig,**plotkwargs):
    # Create a new 3D axis
    ax = fig.add_subplot(111, projection='3d')

    # Plots the undeformed structure
    nne = np.size(C, 0)           # Number of elements
    for i in range(nne):
        xx = X[C[i, 0:2] - 1, 0]
        yy = X[C[i, 0:2] - 1, 1]
        zz = X[C[i, 0:2] - 1, 2]
        ax.plot(xx, yy, zz, **plotkwargs)

    # Set axis limits to avoid zooming issues
    x_min, x_max = np.min(X[:, 0]), np.max(X[:, 0])
    y_min, y_max = np.min(X[:, 1]), np.max(X[:, 1])
    z_min, z_max = np.min(X[:, 2]), np.max(X[:, 2])
    
    ax.set_xlim([x_min - 0.1, x_max + 0.1])
    ax.set_ylim([y_min - 0.1, y_max + 0.1])
    ax.set_zlim([z_min - 0.1, z_max + 0.1])

    # Set equal aspect ratio (helps with zooming issues)
    ax.set_box_aspect([1, 1, 1])    # Ensures equal scaling
    return ax                       # Returns the axis object for further modifications

def plotNodes(X, ax, bound, spring_support=None):
    # Count the number of supports for each node
    support_counts = np.zeros(X.shape[0], dtype=int)

    if np.any(bound):
        for node in bound[:, 0]:
            support_counts[int(node) - 1] += 1

    if spring_support is not None and np.any(spring_support):
        for node in spring_support[:, 0]:
            support_counts[int(node) - 1] += 1

    # Define colors based on the number of supports
    colors = np.array(['b', 'r', 'g', 'orange'])
    labels = ['0 Supports', '1 Support', '2 Supports', '3 Supports']

    # Plot each node with the corresponding color
    for i, (x, y, z) in enumerate(X):
        color = colors[min(support_counts[i], 3)]
        ax.scatter(x, y, z, c=color, marker='o', linewidth=1.5, edgecolor='white')

    # Create legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=8, label=label) 
               for color, label in zip(colors, labels)]
    ax.legend(handles=handles, title='Node Supports')

    return ax

def plotNodeNumbering(X,ax,dsup,**textkwargs):
    # vector with node numbers
    s = np.arange(1,np.size(X,0)+1)

    xoffset = 0-dsup*1.7
    yoffset = 0-dsup*1.7
    zoffset = 0-dsup*2.0

    for i,key in enumerate(s):
        x = X[i,0] + xoffset
        y = X[i,1] + yoffset
        z = X[i,2] + zoffset
        ax.text(x,y,z, str(key), color = 'blue', horizontalalignment='center', verticalalignment='center',**textkwargs)
    return ax

def plotElementNumbering(X, C, ax, dsup, **textkwargs):
    # Loop over elements from Connectivity matrix
    for i in range(np.size(C, 0)):
        # Direction vectors
        dx = X[C[i, 1] - 1, 0] - X[C[i, 0] - 1, 0]
        dy = X[C[i, 1] - 1, 1] - X[C[i, 0] - 1, 1]
        dz = X[C[i, 1] - 1, 2] - X[C[i, 0] - 1, 2]
        dirvec = np.array([dx, dy, dz]) / np.sqrt(dx**2 + dy**2 + dz**2)  # Unit vector in the direction of the element
        normvec = np.cross(dirvec, [0, 0, 1])  # Normal vector in the positive direction

        # Midpoint location
        xmid = dx / 2 + X[C[i, 0] - 1, 0]
        ymid = dy / 2 + X[C[i, 0] - 1, 1]
        zmid = dz / 2 + X[C[i, 0] - 1, 2]

        # Text offset
        xoffset = normvec[0] * dsup * 2.0
        yoffset = normvec[1] * dsup * 2.0
        zoffset = normvec[2] * dsup * 2.0

        # Element number
        key = str(i + 1)  # String with element numbers

        # Plot label
        ax.text(xmid + xoffset, ymid + yoffset, zmid + zoffset, str(key),
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'),
                horizontalalignment='center', verticalalignment='center', **textkwargs)
    return ax

def getPlotAxsLim(X, scale, scalefact):
    # Get figure size in x-, y- and z- direction
    sizeX = np.max(X[:,0]) - np.min(X[:,0])
    sizeY = np.max(X[:,1]) - np.min(X[:,1])
    sizeZ = np.max(X[:,2]) - np.min(X[:,2])

    # Common plot annotation dimension
    dsup = max(abs(sizeX), abs(sizeY), abs(sizeZ)) * scale
    
    # Define x-, y- and z- axis limits
    xmin = np.min(X[:,0]) - dsup * scalefact
    xmax = np.max(X[:,0]) + dsup * scalefact
    ymin = np.min(X[:,1]) - dsup * scalefact
    ymax = np.max(X[:,1]) + dsup * scalefact
    zmin = np.min(X[:,2]) - dsup * scalefact
    zmax = np.max(X[:,2]) + dsup * scalefact
    axlim = np.array([xmin, xmax, ymin, ymax, zmin, zmax])

    return [dsup, axlim]

def set_axes_equal(ax):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    zlim = ax.get_zlim()

    x_range = xlim[1] - xlim[0]
    y_range = ylim[1] - ylim[0]
    z_range = zlim[1] - zlim[0]

    # Determine the maximum span
    max_range = max(x_range, y_range, z_range) / 2.0

    # Find the midpoints
    x_mid = (xlim[0] + xlim[1]) / 2.0
    y_mid = (ylim[0] + ylim[1]) / 2.0
    z_mid = (zlim[0] + zlim[1]) / 2.0

    # Apply new limits based on the max range
    ax.set_xlim([x_mid - max_range, x_mid + max_range])
    ax.set_ylim([y_mid - max_range, y_mid + max_range])
    ax.set_zlim([z_mid - max_range, z_mid + max_range])

def plotModeShape(Xnew, C, nne, ax, **plotkwargs):

    # Plots the deformed structure
    for i in range(nne):
        xx = Xnew[C[i, 0:2] - 1, 0]
        yy = Xnew[C[i, 0:2] - 1, 1]
        zz = Xnew[C[i, 0:2] - 1, 2]

        ax.plot(xx, yy, zz, marker='o', color='b', linestyle='-', linewidth=2) # marker='o'

    # Set axis limits to avoid zooming issues
    x_min, x_max = np.min(Xnew[:, 0]), np.max(Xnew[:, 0])
    y_min, y_max = np.min(Xnew[:, 1]), np.max(Xnew[:, 1])
    z_min, z_max = np.min(Xnew[:, 2]), np.max(Xnew[:, 2])
    
    ax.set_xlim([x_min - 0.1, x_max + 0.1])
    ax.set_ylim([y_min - 0.1, y_max + 0.1])
    ax.set_zlim([z_min - 0.1, z_max + 0.1])

    # Set equal aspect ratio (helps with zooming issues)
    ax.set_box_aspect([1, 1, 1])    # Ensures equal scaling
    return ax                       # Returns the axis object for further modifications