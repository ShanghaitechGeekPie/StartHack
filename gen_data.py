import h5py
import pandas as pd
import numpy as np


def readH5(filename):
    dataframes = []
    f = h5py.File(filename, 'r')
    def visitandsave(name):
        ele = f[name]
        if isinstance(ele, h5py.Dataset):
            dataframes.append(pd.DataFrame(np.array(ele)))
    f.visit(visitandsave)
    return dataframes




