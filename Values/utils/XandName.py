# Abstract

import numpy as np


def XtoName(X, sections, index=False):
    """
    Give number of frame.
    
    Parameters:
    ----------
    L -- float or array. 
         For next functions len(L) > 1.
    frames -- array of frames:
        [0] -- frame_num
        [1] -- frame_length
    
    Result:
    ------
    frame_name -- string or string's array. 
    if index == True:
        index -- array of index
    
    Note: only for one scalar of L. Not for array.
    """
    if (type(X) == int) or (type(X) == float):
        ind = np.argwhere(X == sections[:, 1].astype("int32"))[0]
        name = sections[ind, 0][0]
    else:
        try:
            X = np.array(X, dtype="int32")
        except TypeError:
            raise TypeError("""Try to change type of data for variable X to list or np.ndarray.
            The array have to be with only float-elements.""")
        ind, name = np.zeros(X.shape), np.zeros(X.shape).astype(str)
        for i, val in enumerate(X):
            ind[i] = np.argwhere(val == sections[:, 1].astype("int32"))
            name[i] = sections[int(ind[i]), 0]
    if index:
        return name, ind 
    return name


def NameToX(names, sections, index=False): # =frames
    """
    Give number of frame.
    
    Parameters:
    ----------
    L -- float
    frames -- array of frames:
        [0] -- frame_num
        [1] -- frame_length
    
    Result:
    ------
    frame_name -- integer. Name of frames: [1:n] 
    
    Note: only for one scalar of L. Not for array.
    """
    if type(names) == str:
        ind = np.argwhere(names == sections[:, 0].astype(str))[0]
        X = sections[ind[0], 1]
#     elif type(names) == float or int:
#         try:
#             names = f"{names}"
#         except TypeError:
#             raise TypeError("Function NameToL doesn't undestand type local variable \"name\"")
#         print("WORK")
#         print(frames[:, 0].astype(str))
#         print(names, type(names))
#         ind = np.argwhere(names == frames[:, 0].astype(str))[0]
#         print(type(ind))
#         L = frames[ind[0], 1]
    else:
        try:
            names = np.array(names, dtype=str)
        except TypeError:
            raise TypeError("""Try to change type of data for variable L to list or np.ndarray.
            The array have to be with only str-elements.""")
        ind, X = np.zeros(names.shape), np.zeros(names.shape).astype("float64")
        for i, name in enumerate(names):
            ind[i] = np.argwhere(name == sections[:, 0].astype(str))[0]
            X[i] = sections[int(ind[i]), 1]
    if index:
        return X, ind
    return X
