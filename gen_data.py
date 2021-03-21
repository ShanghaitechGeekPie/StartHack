import h5py
import pandas as pd
import numpy as np
import os
import glob


def readH5(filename, save_dir_name):
    f = h5py.File(filename, 'r')

    def visitandsave(name):
        ele = f[name]
        if isinstance(ele, h5py.Dataset):
            data = pd.DataFrame(np.array(ele))
            data.to_pickle(os.path.join(save_dir_name, name.replace('/', '_')))
            print(data.keys())

    f.visit(visitandsave)

readH5('data/overhang/bae8f52c-407e-5f89-a8e3-61fcca51ee0a.h5','data/overhang_exported')
readH5('data/overhang/bae8f52c-407e-5f89-a8e3-61fcca51ee0a_raw.h5','data/overhang_exported')

readH5('data/traverse/e897d166-1618-5bd3-ba3a-cb7577c64647.h5','data/traverse_exported')
readH5('data/traverse/e897d166-1618-5bd3-ba3a-cb7577c64647_raw.h5','data/traverse_exported')
# filelist = ['data/overhang', 'data/traverse']
# for ff in filelist:
#     for q in glob.glob(os.path.join(ff, '*.h5')):
#         print(q)
#         os.mkdir(ff + "_exported")
#         readH5(q, ff + "_exported")
