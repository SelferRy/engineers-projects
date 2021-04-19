# Abstract

# Rename "overload_tools_3b_min_v03"
# Changes: del LtoName() and move it to XandName.py

import numpy as np
import matplotlib.pyplot as plt
from utils.tools_for_min_val import *

def find_max(X, function):
    """
    Give max index and value of array ny.
    
    Parameters:
    ----------
    X -- integer or array. For example: length.
    function -- scipy.interpolate.interp1d function. Define earlier.
    
    Result:
    ------
    max_ind_ny -- index of maximum ny(X)
    max_ny -- maximum value of ny(X)
    X_max -- "length's max" == length (x-axis) where is max(ny).
    
    Note: domain(X | pos or neg_turb) is frame[0:-17, 1]
          domain(X | pos or neg_down) is frame[0:-12, 1]
    """
    n = np.abs(function(X))
    max_ind_ny = np.argmax(n)
    max_ny = np.amax(n)
    if type(X) != float:
        X_max = X[max_ind_ny]
    else:
        X_max = X
    return max_ind_ny, max_ny, X_max

# frames = np.zeros((2,2))


def max_value(function, _print=True, **parameters):
    """
    Get information about max overload.
    
    Parameters:
    ----------
    function -- function for linear interpolation.
    parameters -- dict with parameters for interpolation.
    
    Result:
    ------
    max_ind -- index of maximum function-value.
    max_val -- the max function-value.
    X_max -- argue-value X where is the max function-value.
    
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
        max_ind, max_val, X_max = find_max(X, function=function)
    except ValueError:
        raise ValueError("""Function's is not domain on the length. 
        Try change X's or name(-s)'s array.
        For Y1-case X's domain is: 0 .. -17 [in index sections-array].
        For Y3-case X's domain is: 0 .. -12 [in index sections-array]. """)
        
    if _print:
        print("max_ind = ", max_ind)
        print("max_val =", max_val)
        print("X_max =", X_max)
    return max_ind, max_val, X_max


def max_filter(**values):
    """
    Get whole parameters and fig for plot.
    
    Parameters:
    ----------
    overloads -- dict:
        functions -- keys are case's names, 
                     values are functions of linear interpolation for max-overload's case.
        L or name -- length's array or names of frames (len(array) > 1)
        frames -- input data of length's distances for frames.
        
    Result:
    ------
    key_max -- key of the maximum value. For example: overloads.
    max_val -- the maximum value. For example: overloads.
    X_max -- X's value with the max_val. For example: length.
    f_max -- functiion linear interpolation of case of maximum overloads.
    """
    markers = [0] * len(values["functions"])
    f = markers.copy()
    for i, func in enumerate(values["functions"].items()):
        values[func[0]] = max_value(function=func[1], _print=False, **values)
        markers[i] = [*[func[0]]]      # get list of dict-keys like ["neg_turb", "neg_down"]
        f[i] = func[1]                 # get list of used functions for ny
        
    ind = {}
    val = {}
    Xs = {}
    for i in range(len(markers)):
        ind[str(*markers[i])] = values[str(*markers[i])][0]
        val[str(*markers[i])] = values[str(*markers[i])][1]
        Xs [str(*markers[i])] = values[str(*markers[i])][2]
    max_val = np.amax(([*val.values()]))
    i = [*val.values()].index(max_val)  # get index with max value
    key_max = [*val][i]    # if it wrong then need undefault-sort for [*dict.values()] and etc. 
    X_max = Xs[key_max]
    f_max = f[i] 
    return key_max, max_val, X_max, f_max


def values_plot(_print=False, **values):
    """
    Get whole parameters and fig for plot.
    
    Parameters:
    ----------
    _print -- switcher for on/off print result-values.
    values -- dict:
        functions -- keys are case's names, 
                     values are functions of linear interpolation for max-val's case. For example: overload.
        L or name -- length's array or names of frames (len(array) > 1)
        sections -- input data of X's distances for sections.
        
    Result:
    ------
    fig -- figure-object. Plot for simplify interpretation.
    """ 
    key_max, max_val, X_max, f = max_filter(**values)
    key_min, min_val, X_min, f_min = min_filter(**values)
    if _print:
        print("key_max: ", key_max)
        print("max_val =", max_val)
        print("X_max = ", X_max)


    sections = values["sections"]
    if "X" in [*values]:
        X = values["X"]
        name = XtoName(X, sections)
    else:
        name = values["name"]
        X = NameToX(name, sections)
    
    if len(X) <= 1:
            raise ValueError("""Length error! 
            Function "values_plot()" need to get array with length > 1.""")
    
    plt.plot(X, f(X), "-k")
    sign = f(X)[1]/np.abs(f(X)[1])
    max_val *= sign
    min_val *= sign
#     print("min:", min_val, "\tmax:", max_val)
    plt.plot([X_max]*2, [min_val, max_val], '--r') # min_val
#     print(np.linspace(min_val, max_val, 2))
#     plt.text(X_max, -3, "test") # f"frame_num = {str_frame_name},\nX = {frame_X}"
    plt.grid()
    if len(X) > 1:
#         interval = f"{X[0]} to {X[-1]} [мм]"
        interval = f"from sec.{name[0]} to sec.{name[-1]}"
    else:
#         interval = f"{X} [мм]"
        interval = f"sec.{name}"
    plt.legend(["Disturb. $val$ on X =" + interval,
                "$val_{max}$ on X = " + interval], fontsize=9)
    ax = plt.gca()
    fig = plt.gcf()
    plt.close()
    return ax, fig


def model(**values):
    """
    Get whole parameters and fig for plot.
    
    Parameters:
    ----------
    overloads -- dict:
        functions -- keys are case's names, 
                     values are functions of linear interpolation for max-overload's case.
        L or name -- length's array or names of frames (len(array) > 1)
        frames -- input data of length's distances for frames.
        
    Result:
    ------
    case -- str-object. Case's name.
    max_val -- maximum value of overloads in the length's array.
    length_max -- length's value with the max_val.
    fig -- figure-object. Plot for simplify interpretation.
    """
    case, max_val, X_max, _ = max_filter(**values)
    case_min, min_val, X_min, _min = max_filter(**values)  # maybe min_filter?
    if "L" in values:
        if len(values["X"]) == 1:
            return case, max_val, X_max, _
            
    if  "name" in values:
         if len(values["name"]) == 1:
            return case, max_val, X_max, _
            
    ax, fig = values_plot(**values)
    plt.close()
    
    return case, max_val, X_max, ax, fig, case_min, min_val, X_min
