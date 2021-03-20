import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

acc_LH = pd.read_pickle('data/vertical_exported/acc_LH')

acc_fps_begin = 1865 + 10 * 50
acc_fps_end = 1865 + 83 * 50


def get_time(t):
    return (t - 1865) / 50


fps = 30
scan_size = 2 * fps
acc_abs_max = set()
for i in range(acc_fps_begin, acc_fps_end - scan_size, scan_size // 2):
    s = acc_LH[i:i + scan_size]['  ']
    result = (s.max(), s.min(), i + np.argmax(s), i + np.argmin(s))
    acc_abs_max.add(result)
acc_abs_max_list = list(acc_abs_max)
acc_abs_max_list = sorted(acc_abs_max_list, key=lambda e: -abs(e[0] - e[1]))
for i in range(10):
    print(acc_abs_max_list[i])
    print(get_time(acc_abs_max_list[i][2]), get_time(acc_abs_max_list[i][3]))
