import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation


def cross_entropy(a):
    return a.cumsum()


def get_hl(name):
    print(name)
    namel = 'data/{}_exported/acc_LH'.format(name)
    namer = 'data/{}_exported/acc_RH'.format(name)

    def side(name_s):
        acc_LH = pd.read_pickle(name_s)

        acc_fps_begin = 1865 + 10 * 50
        acc_fps_end = 1865 + 83 * 50

        def get_time(t):
            return (t - 1865) / 50

        fps = 50
        scan_size = 2 * fps
        acc_abs_max = set()
        for i in range(acc_fps_begin, acc_fps_end - scan_size, scan_size // 2):
            data = acc_LH[i:i + scan_size]
            s = np.sqrt(data['AP'] ** 2 + data['DP'] ** 2 + data['UR'] ** 2)
            result = (s.max(), s.min(), i + np.argmax(s), i + np.argmin(s))
            acc_abs_max.add(result)
        acc_abs_max_list = list(acc_abs_max)
        acc_abs_max_list = sorted(acc_abs_max_list, key=lambda e: -abs(e[0] - e[1]))
        for i in range(6):
            # print(acc_abs_max_list[i])
            print("{:.3}--{:.3}".format(get_time(acc_abs_max_list[i][2]), get_time(acc_abs_max_list[i][3])))

    side(namel)
    side(namer)
    print("------------------------------------------")


def get_highlight_graph(left_hand, right_hand):
    fps = 30
    acc_fps = 50

    acc_fps_begin = 1865

    acc_lh = pd.read_pickle(left_hand)  # 'data/vertical_exported/acc_LH')
    acc_rh = pd.read_pickle(right_hand)

    endFrame = acc_fps_begin + 90 * fps

    save_count = endFrame - acc_fps_begin

    def getFrameCount():
        for i in range(int(acc_fps_begin / acc_fps * fps), int(acc_lh.shape[0] / acc_fps * fps)):
            yield i

    def init():
        ax.set_ylim(0, 5)
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
        second = frameCount / fps
        accframeCount = int(second * acc_fps)
        # update the data
        print(second - acc_fps_begin / acc_fps)

        # here we gen the data

        lap = acc_lh[max(accframeCount - acc_fps, 0):accframeCount]['AP']
        lur = acc_lh[max(accframeCount - acc_fps, 0):accframeCount]['UR']
        ldp = acc_lh[max(accframeCount - acc_fps, 0):accframeCount]['DP']

        rap = acc_rh[max(accframeCount - acc_fps, 0):accframeCount]['AP']
        rur = acc_rh[max(accframeCount - acc_fps, 0):accframeCount]['UR']
        rdp = acc_rh[max(accframeCount - acc_fps, 0):accframeCount]['DP']

        l = np.sqrt(lap ** 2 + lur ** 2 + ldp ** 2)
        r = np.sqrt(rap ** 2 + rur ** 2 + rdp ** 2)

        ydata = np.array(l + r)
        # gen data end

        xdata = np.linspace(0, 1, acc_fps)[0:len(ydata)]
        line.set_data(xdata, ydata)

        return line,

    ani = animation.FuncAnimation(fig, run, getFrameCount, interval=1000 / fps, init_func=init, save_count=save_count)
    #plt.show()
    ani.save(left_hand.replace('/', '_') + '_' + 'highlight' + '.mp4', writer='ffmpeg', fps=fps, dpi=300)

def get_height_graph(height_path):
    height = pd.read_pickle(height_path)
    height.plot(label='height')

# for f in [('data/overhang_exported/acc_LH','data/overhang_exported/acc_RH'), ('data/traverse_exported/acc_LH','data/traverse_exported/acc_RH'), ('data/traverse_exported/acc_LH','data/traverse_exported/acc_RH')]:
# for f in [('data/vertical_exported/acc_LH','data/vertical_exported/acc_RH')]:
#     get_highlight_graph(f[0],f[1])
get_height_graph('data/vertical_exported/climbs_0_height_profile')

