import numpy as np

def intpL(PolDeg=None):
    """
    Gauss-Legendre quadrature points and weights for 1D integration

    Parameters
    ----------
    PolDeg : int
        Polynomial degree of the integration rule

    Returns
    -------
    xip : np.array
        Integration points
    wip : np.array
        Integration weights
    """

    if PolDeg <= 1:
        xip = np.array([0])
        wip = np.array([2])
    
    elif PolDeg <= 3:
        xip = np.array([-0.577350269189626, 0.577350269189626])
        wip = np.array([1, 1])

    elif PolDeg <= 5:
        xip = np.array([-0.774596669241483, 0, 0.774596669241483])
        wip = np.array([0.555555555555556, 0.888888888888889, 0.555555555555556])

    elif PolDeg <= 7:
        xip = np.array([-0.861136311594053, -0.339981043584856, 0.339981043584856, 0.861136311594053])
        wip = np.array([0.347854845137454, 0.652145154862546, 0.652145154862546, 0.347854845137454])

    elif PolDeg <= 9:
        xip = np.array([-0.906179845938664, -0.538469310105683, 0, 0.538469310105683, 0.906179845938664])
        wip = np.array([0.236926885056189, 0.478628670499366, 0.568888888888889, 0.478628670499366, 0.236926885056189])
    
    else:
        raise ValueError("PolDeg too high or note specified")
    
    return xip, wip