import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd


def getVideo(filename, keyName):
    fps = 30
    acc_fps = 50

    acc_fps_begin = 1865

    acc_lh = pd.read_pickle(filename)  # 'data/vertical_exported/acc_LH')

    endFrame = acc_fps_begin + 90 * fps

    save_count = endFrame - acc_fps_begin

    def getFrameCount():
        for i in range(int(acc_fps_begin / acc_fps * fps), int(acc_lh.shape[0] / acc_fps * fps)):
            yield i

    def init():
        ax.set_ylim(-3, 1.8)
        ax.set_xlim(0, 1)
        del xdata[:]
        del ydata[:]
        line.set_data(xdata, ydata)
        return line,

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.grid()
    xdata, ydata = [], []

    def run(frameCount):
        global xdata, ydata
        second = frameCount / fps
        accframeCount = int(second * acc_fps)
        # update the data
        print(second - acc_fps_begin / acc_fps)
        ydata = np.array(acc_lh[max(accframeCount - acc_fps, 0):accframeCount][keyName])
        xdata = np.linspace(0, 1, acc_fps)[0:len(ydata)]
        line.set_data(xdata, ydata)

        return line,

    ani = animation.FuncAnimation(fig, run, getFrameCount, interval=1000 / fps, init_func=init, save_count=save_count)
    # plt.show()
    ani.save(filename.replace('/', '_') + '_' + keyName + '.mp4', writer='ffmpeg', fps=fps, dpi=300)


filenames = ['data/vertical_exported/acc_LH', 'data/vertical_exported/acc_RH']
keys = ['AP', 'UR', 'DP']

for fn in filenames:
    for k in keys:
        getVideo(fn, k)
