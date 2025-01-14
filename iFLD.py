# iFLD算法的实现
import os
import pandas as pd
import numpy as np
from scipy.interpolate import splrep, splev


def fluor(in_loc, out_loc, left_loc, right_loc, in_wvl, DataWvl, RAD, IRR, Ref, k_Ref, k_IRR):
    # 获取波段的两个分割点
    left = int(left_loc[0])
    right = int(right_loc[0])
    weights = np.full(len(DataWvl), 1)
    weights[left:right] = 0

    tck_Ref = splrep(DataWvl, Ref, w=weights, k=k_Ref)
    tck_IRR = splrep(DataWvl, IRR, w=weights, k=k_IRR)

    a_Ref = Ref[out_loc] / splev(in_wvl, tck_Ref)
    a_F = a_Ref * IRR[out_loc] / splev(in_wvl, tck_IRR)

    up = RAD[in_loc] * IRR[out_loc] * a_Ref - RAD[out_loc] * IRR[in_loc]
    down = IRR[out_loc] * a_Ref - IRR[in_loc] * a_F
    SIF_iFLD = up / down

    return SIF_iFLD


def iFLD(path, pathout, out_wvl, left_wvl, right_wvl, k_Ref, k_IRR):
    # 程序入口，供调用

    if not os.path.exists(pathout):
        os.makedirs(pathout)

    path_dirs = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            path_dirs.append(os.path.join(name))
    path_dirs.sort()  # 对获取的文件夹按字符键值排序

    for pathdir in path_dirs:
        folder = os.path.join(path, pathdir)
        filenames = os.listdir(folder)
        filenames.sort()  # 对获取的文件按字符键值排序

        if not os.path.exists(pathout):
            os.makedirs(pathout)

        SIF1d = pd.DataFrame(columns=('Time', 'iFLD'))

        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')

            DataWvl = data['DataWvl'].ravel()
            IRR = data['IRR'].ravel()
            RAD = data['RAD'].ravel()
            Time = data['Time'].ravel()[0]
            Ref = data['Ref'].ravel()
            in_loc = data['in_loc'].ravel()[0]
            in_wvl = DataWvl[in_loc]

            out_loc = np.where(np.abs(DataWvl - out_wvl) == np.min(np.abs(DataWvl - out_wvl)))  # 758nm处，吸收线外
            left_loc = np.where(np.abs(DataWvl - left_wvl) == np.min(np.abs(DataWvl - left_wvl)))  # 758nm处，左肩
            right_loc = np.where(np.abs(DataWvl - right_wvl) == np.min(np.abs(DataWvl - right_wvl)))  # 770nm处，右肩

            try:
                # 进行最终计算
                SIF_iFLD = fluor(in_loc, out_loc, left_loc, right_loc, in_wvl, DataWvl, RAD, IRR, Ref, k_Ref, k_IRR)
                # 输出结果包含时间和反演结果
                SIF1d = pd.concat([SIF1d, pd.DataFrame(
                    {'Time': Time, 'iFLD': SIF_iFLD},
                    index=[i])])

            except Exception as e:
                print(e)

        pathday = pathout + '\\' + folder[-10:] + '.csv'

        # 输出反演结果
        SIF1d.to_csv(pathday, sep=",", index=False)


if __name__ == '__main__':
    # 测试用例
    path = r'C:\Users\DZY\Desktop\P4\定标结果'  # 输入数据
    pathout = r'C:\Users\DZY\Desktop\P4\未经质量控制的反演结果\iFLD'  # 输出数据
    out_wvl = 758  # 吸收线外波段
    left_wvl = 758  # 氧气波段左肩
    right_wvl = 770  # 氧气波段右肩
    k_Ref = 3  # 参考光谱插值次数
    k_IRR = 3  # 入射辐射光谱插值次数
    iFLD(path, pathout, out_wvl, left_wvl, right_wvl, k_Ref, k_IRR)
