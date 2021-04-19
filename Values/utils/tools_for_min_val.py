# Abstract

from .XandName import *
# import numpy as np
# import matplotlib.pyplot as plt
# from .tools_3a import NameToL


def find_min(X, function):
    """
    Give min index and value of array ny.
    
    Parameters:
    ----------
    X -- integer or array. For example: length.
    function -- scipy.interpolate.interp1d function. Define earlier.
    
    Result:
    ------
    min_ind -- index of minimum function-value.
    min_val -- the minimum function-value.
    X_min -- For example: "length's min" == length (x-axis) where is min(value).
    
    Note: domain(X | pos or neg_Y1) is frame[0:-17, 1]
          domain(X | pos or neg_Y3) is frame[0:-12, 1]
    """
    n = np.abs(function(X))
    min_ind = np.argmin(n)
    min_val = np.amin(n)
    if type(X) != float: # or int
        X_min = X[min_ind]
    else:
        X_min = X
    return min_ind, min_val, X_min


def min_values(function, _print=True, **parameters):
    """
    Get information about min overload.
    
    Parameters:
    ----------
    function -- function for linear interpolation.
    parameters -- dict with parameters for interpolation.
    
    Result:
    ------
    min_ind -- index of minimum function-value.
    min_val -- the min function-value.
    X_min -- X-value where is the min function-value.
    
    Note: domain(X | pos or neg_Y1) is sections[0:-17, 1]
          domain(X | pos or neg_Y3) is sections[0:-12, 1]
    """
    sections = parameters["sections"]
    if "X" in [*parameters]:
        X = parameters["X"]
    else:
        name = parameters["name"]
        X = NameToX(name, sections=sections)
    try:
        min_ind, min_val, X_min = find_min(X, function=function)
    except ValueError:
        raise ValueError("""Function's is not domain on the length. 
        Try change L's or name(-s)'s array.
        For turb-case length's domain is: 0 .. -17 [in index sections-array].
        For down-case length's domain is: 0 .. -12 [in index sections-array]. """)
        
    if _print:
        print("min_ind = ", min_ind)
        print("min_val =", min_val)
        print("X_min =", X_min)
    return min_ind, min_val, X_min


def min_filter(**values):
    """
    Get whole parameters and fig for plot.
    
    Parameters:
    ----------
    values -- dict:
        functions -- keys are case's names, 
                     values are functions of linear interpolation for min-values's case.
        X or name -- X's array or names of sections (len(array) > 1)
        frames -- input data of length's distances for frames.
        
    Result:
    ------
    key_min -- key of the minimum value.
    min_val -- the minimum value.
    X_min -- X's value with the min_val.
    f_min -- function linear interpolation of case of minimum values.
    """
    markers = [0] * len(values["functions"])
    f = markers.copy()
    for i, func in enumerate(values["functions"].items()):
        values[func[0]] = min_values(function=func[1], _print=False, **values)
        markers[i] = [*[func[0]]]      # get list of dict-keys like ["neg_turb", "neg_down"]
        f[i] = func[1]                 # get list of used functions for ny
        
    ind = {}
    val = {}
    Xs = {}
    for i in range(len(markers)):
        ind[str(*markers[i])] = values[str(*markers[i])][0]
        val[str(*markers[i])] = values[str(*markers[i])][1]
        Xs [str(*markers[i])] = values[str(*markers[i])][2]
    min_val = np.amin(([*val.values()]))
    i = [*val.values()].index(min_val)  # get index with min value
    key_min = [*val][i]    # if it wrong then need undefault-sort for [*dict.values()] and etc. 
    X_min = Xs[key_min]
    f_min = f[i] 
    return key_min, min_val, X_min, f_min
