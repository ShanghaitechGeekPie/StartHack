import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter


def KalmanFilter(array, sigma=10):
    # Not Kalman Filter, lol.
    # return gaussian_filter(array, sigma)
    return array


def sgn(v):
    if v > 0:
        return 1
    return -1


acc_LH = pd.read_pickle('data/vertical_exported/acc_RH')

acc_adjust = 1865

acc_fps_begin = 1865
# acc_fps_end = 1865 + 83 * 50
acc_fps_end = 1865 + 85 * 50

g = 9.81

p = (0.0, 0.0, 0.0)
v = (0.0, 0.0, 0.0)

# acc_mod = (0.0,0.0,0.0)
# acc_LH['AP'][0:1000].plot()
acc_LH['AP'] = KalmanFilter(acc_LH['AP'])
acc_LH['UR'] = KalmanFilter(acc_LH['UR'])
acc_LH['DP'] = KalmanFilter(acc_LH['DP'])

# acc_LH['AP'].plot()
# acc_LH['UR'].plot()
# acc_LH['DP'].plot()

acc_LH = g * acc_LH
# acc_LH = acc_LH

acc_mod = (0, 0, 0)

x = []
y = []
z = []

for i in range(acc_fps_begin + 1, acc_fps_end):
    current_tick = i
    last_tick = i - 1
    dt = acc_LH['timestamp'][current_tick] - acc_LH['timestamp'][last_tick]
    current_tick_data = (acc_LH['AP'][current_tick] - acc_mod[0], acc_LH['UR'][current_tick] - acc_mod[1],
                         acc_LH['DP'][current_tick] - acc_mod[2])
    last_tick_data = (
        acc_LH['AP'][last_tick] - acc_mod[0], acc_LH['UR'][last_tick] - acc_mod[1],
        acc_LH['DP'][last_tick] - acc_mod[2])
    dv = ((current_tick_data[0] + last_tick_data[0]) * dt, (current_tick_data[1] + last_tick_data[1]) * dt,
          (current_tick_data[2] + last_tick_data[2]) * dt)
    v = (0.5*v[0] + dv[0], 0.5*v[1] + dv[1], 0.5*v[2] + dv[2])
    # v = (sgn(v[0]) * np.sqrt(abs(v[0])) + dv[0], sgn(v[1]) * np.sqrt(abs(v[1])) + dv[1], sgn(v[2]) * np.sqrt(abs(v[2])) + dv[2])
    p = (p[0] + v[0] * dt, p[1] + v[1] * dt, p[2] + v[2] * dt)
    print((i - acc_adjust) / 50, v)
    # print((i - acc_adjust)/50,p)
    x.append(p[0])
    y.append(p[1])
    z.append(p[2])

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot(x, z, y, label='parametric curve')
ax.legend()
