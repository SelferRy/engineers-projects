import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.values_tools import model
from utils.tools_for_min_val import NameToX


def LstToStr(lst:list, sep=", ") -> str:
    """
    Transform list to string by separator
    
    Parameters:
    ----------
    lst -- list which want transform.
    sep -- separator by transform.
    
    Result:
    ------
    a -- string with list's elements.
    """
    l = len(lst)
    a = lst.copy() # .tolist()
    for i in range(l):
        a[i] = sep.join(lst[i])
    return a


def name_val(frames_name, max_vals, **loc_variables):
    """
    Get DataFrame with all parameters with need to see after all overload's compute.

    Parameters
    ----------
    sections_name   -- list with name's sections like: ["1", "2", "3", ...]
    max_vals      -- float or list with max values for the interval(-s).
                     If 1 interval then max_vals is float.
    loc_variables -- dict. Keys of every element of the dict in names of sections.
                     Notation for only values:
                        cases           -- marker of the finction wich is max on the length/sections (e.g.: "neg_Y1").
                        X_max_list -- values of length for max_vals. type: float.
    
    Returns
    ------
    df -- pd.DataFrame. Contains "Names", "Values", "X", "Cases".
        Names  -- list of lists of str or list of few/many np.array([...], dtype = str).
        Values -- list of floats. Max value for every interval.
        X -- list of floats. Max values of length with max values of function-values.
        Cases  -- list of markers of functions which have max function-values on the X/sections (e.g.: ["neg_Y1", ...]).
    """
#     print("WORK")
#     print(sections_name)
    X_max_list = loc_variables["X_max_list"]
    cases = loc_variables["cases"]
    
    df = pd.DataFrame({"Names": LstToStr([*frames_name.values()]),
                       "Values": [*max_vals.values()],
                       "X": [*X_max_list.values()],
                       "Cases": [*cases.values()]})
    return df


def list_values(**values): #list_frames:list,
    """
    Get tuple with all arguments. Without order: (cases == name of function with max,
                                                 max/min values, max's/min's length,
                                                 figures for all this cases.
                                                 names of frames)

    Parameters
    ----------
    overloads -- dict. Keys:
                 functions -- dict:
                              general: {"name_case": function_for_case}
                              example: {"neg_turb": neg_turb,
                                        "neg_down": neg_down}
                 name -- list or np.array with list(-s) or array(-s).
                         Inner list(-s) or array(-s) has(-ve) >= 2 elements, type str.
                         example: 1. [["2", "3"]]
                                  2. [np.array(["2", "3"], dtype = "U2"), ["4", "5"]]
                                  3. [np.array(["2", "3"], dtype = str)]
                 frames -- np.array.shape = (num_frames, 2):
                                  [:, 0] : names of frames without treatment. dtype == object.
                                  [:, 1] : length for this frames.

    Returns
    -------
    Type every elements are dict.
    Keys for every dict are names of sections with max_val (example: "0", ..., "24а", ...).
    Values are different. Notation for only one value of one element of the dict:
        cases           -- marker of the function which has max function-values on the X/sections (example: "neg_Y1").
        max_vals        -- max's values of function-values in interval. type: float.
        X_max_list -- values of length for max_vals. type: float.
        sections_name   -- names of sections. type: str or np.array([...], dtype = str).
        figs            -- plt.figure object.
        case_min        -- marker of the min function on the X/sections (example: "pos_Y1").
        min_val         -- min's values of values in interval. type: float.
        X_min      -- values of X for min_vals. type: float.
    """
    sections = values["sections"]
    if "neg_Y1" in values["functions"]:
        neg_Y1 = values["functions"]["neg_Y1"]
    if "pos_Y1" in values["functions"]:
        pos_Y1 = values["functions"]["pos_Y1"]
    if "neg_Y3" in values["functions"]:
        neg_Y3 = values["functions"]["neg_Y3"]

    list_sections = values["name"].copy()
    cases = {}
    max_vals = {}
    x_max_list = {}
    axs = {}
    figs = {}
    section_name = {}
    case_min = {}
    min_val = {}
    x_min = {}
    for i, section in enumerate(list_sections):
        section_name[f"{i}"] = section
        cases[str(i)], max_vals[str(i)], \
        x_max_list[str(i)], axs[str(i)], \
        figs[str(i)], case_min[str(i)], min_val[str(i)], \
        x_min[str(i)] = model(
            functions = {"pos_Y1": pos_Y1,
                         "neg_Y1": neg_Y1,
                         "neg_Y3": neg_Y3},
            name=section, sections=sections)
    return cases, max_vals, x_max_list, section_name, figs, case_min, min_val, x_min


# ===================== Save all figs =====================
def multipleSaveFigs(**figs_dict):
    """
    Save figures from dict figs_dict.

    Parameters
    ----------
    figs_dict -- dict of figures.
                 keys   -- names of frames. type: str.
                 values -- plt.figure object.

    Returns
    -------
    None
    """
    for key, fig in figs_dict.items():
        fig.savefig(f"images/fig_{key}.png", dpi=100)
        

# ================ For one by name ================
def only_section(function, sections, *args):
    """
    Simplified function for check overload (float) of one or few frame.

    Parameters
    ----------
    function -- function object.
    sections -- input data from ".xlsx" converted to numpy.
              type: np.array; shape = (number_frames, 2).
              Every line of the array is (name : length).
    args -- list with names of frames.
            Note: name the variable will modify in next versions.

    Returns
    -------
    lst - list contains: [list_frame_names, list_overloads_val].
          e.g.: [["2", "10", "40"], [-6.547, -5.421, -4.75]].
          if it would a dict of overloads: {"2": -6.547, "10": -5.421, "40": -4.75}.
          Note: in next versions change it to dict-version.
    """
    lst = []
    for arg in args:
#         print(type(arg))
        lst.extend((arg, function(NameToX(arg, sections)).tolist()))
    return lst

def all_sections_plot(X, save=False, **functions):
    """
    Give figure on all length.
    
    Parameters:
    ----------
    L_all     -- length from nose to end airplane. Float.
    save      -- switcher. Choose save or not the figure.
    functions -- dict with function objects.

    Returns:
    -------
    fig -- figure of all overloads.
    """
    pos_Y1 = functions["pos_Y1"]
    neg_Y1 = functions["neg_Y1"]
    pos_Y2 = functions["pos_Y2"]
    neg_Y2 = functions["neg_Y2"]
    neg_Y3 = functions["neg_Y3"]
    pY2 = lambda x: pos_Y2(x) if type(x) == int or type(x) == float else len(x)*[pos_Y2(x)]
    nY2 = lambda x: neg_Y2(x) if type(x) == int or type(x) == float else len(x)*[neg_Y2(x)]


    X = np.linspace(0, X)
    plt.plot(X, pos_Y1(X))
    plt.plot(X, neg_Y1(X))
    plt.plot(X, neg_Y3(X))
    plt.plot(X, pY2(X))
    plt.plot(X, nY2(X))
    
    plt.grid(which="both")
    plt.legend(["$pos$ $val_{Y1}$", "$neg$ $val_{Y1}$", "$neg$ $val_{Y3}$",
                "$pos$ $val_{Y2}$", "$neg$ $val_{Y2}$"],
               fontsize=12, bbox_to_anchor=(1.05, 1)
              )
    
    plt.title("Distribution",
              fontdict = {"fontsize": 16})
    fig = plt.gcf()
    plt.close()
    if save:
        fig.savefig("images/Vals_dist.png", dpi=250, bbox_inches="tight")
    return fig