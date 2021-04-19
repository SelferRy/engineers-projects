# Abstract

import numpy as np
import pandas as pd
# from utils.tools_min import *
# ================ Frames data ===================
sections = pd.ExcelFile("sections_data.xlsx").parse('sections').to_numpy()

class container_sections:
    """
    Slicing DataFrame like input template (e.g.: "sections_data.xlsx").
    For treatment in functions like list_overloads (give all needed: *cases_max, max_vals, X_max,
                                                                      cases_min, min_vals, X_min,
                                                                      figs, sections_names.
                                                    Note: without order and with some re-name variables
                                                          for simplify reading).

    """
    # ================ Start from 9's section ================
    names_sections = sections[9:, 0].astype(str)
    
    # from left-side
    s0_1 = sections[0:2, 0].astype(str)
    s1_2 = sections[1:3, 0].astype(str)
    s5_7 = sections[5:8, 0].astype(str)
    s9_16 = names_sections[0:8]
    s13_14 = names_sections[4:6]
    s14_15 = names_sections[5:7]
    s15_16 = s9_16[-2:]
    s17_19 = names_sections[8:11]
    s24e_24j = names_sections[21:23]
    s24k_24l = names_sections[24:26]
    s32_35 = names_sections[29:33]
    s36_40 = names_sections[33:38]
    s43_44 = names_sections[40:42]
    s67e_70 = names_sections[67:71]
    s73_74 = names_sections[73:75]
    s81_84 = names_sections[81:85]
    s86_90 = names_sections[86:91]
    s97_99 = names_sections[97:100]
    
    # from top
    s9_10 = names_sections[0:2]
    s21_22 = names_sections[12:14]
    s24_24a = names_sections[15:17]
    s32_33 = names_sections[29:31]
    s36_40 = names_sections[33:38]
    s41_42 = names_sections[38:40]
    s43_44 = names_sections[40:42]
    s46_47 = names_sections[43:45]
    s48_49 = names_sections[45:47]
    s56_57 = names_sections[53:55]
    s70_71 = names_sections[70:72]
    s76_77 = names_sections[76:78]
    s83_84 = names_sections[83:85]
    s84_85 = names_sections[84:86]
    s85_86 = names_sections[85:87]
    s88_89 = names_sections[88:90]
    s91_92 = names_sections[91:93]
    s95_96 = names_sections[95:97]
    s97_98 = names_sections[97:99]
    sLast = names_sections[-2:]
    
    # from spec
    s46_49 = names_sections[43:47]
    s86_87 = names_sections[86:88]
    s12_13 = names_sections[3:5]
    
    s8_9 = sections[8:10, 0].astype(str)
    s10_11 = names_sections[1:3]   # print(f10_11)
    s11_12 = names_sections[2:4]   # print(f11_12)
    s17_18 = names_sections[8:10]   # print(f17_18)
    s77_79 = names_sections[77:80]   # print(f77_79)
    s86_88 = names_sections[86:89]   # print(f86_88)
    s79_80 = names_sections[79:81]   # print(f79_80)
    s24_24a = names_sections[15:17]   # print(f24_24a)
    s98_99 = names_sections[98:100]   # print(f98_99)
    
    list_sections = [s0_1, s1_2, s5_7,
                   s9_10, s9_16, s12_13, s13_14,
                   s14_15, s15_16, 
                  s17_19, s24e_24j, s24k_24l,
                  s32_35, s36_40, s43_44, 
                  s67e_70, s73_74, s81_84,
                  s86_90, s21_22,
                  s24_24a, s32_33, s36_40,
                  s41_42, s43_44, s46_47, s46_49,
                  s48_49, s56_57, s70_71, s76_77,
                  s83_84, s84_85, s85_86, s86_87, 
                  s88_89, s91_92,
                  s95_96, s97_99, s97_98, sLast,
                  s8_9, s10_11, s11_12,
                  s17_18, s77_79,
                  s86_88, s79_80, s24_24a, s98_99]
