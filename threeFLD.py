# 3FLD算法的实现
import os
import numpy as np
import pandas as pd


def fluor(in_loc, left_loc, right_loc, left_wvl, right_wvl, in_wvl, RAD, IRR):
    # 3FLD算法，根据公式计算
    w_lift = (right_wvl - in_wvl) / (right_wvl - left_wvl)
    w_right = (in_wvl - left_wvl) / (right_wvl - left_wvl)
    IRR_out = w_lift * IRR[left_loc] + w_right * IRR[right_loc]
    RAD_out = w_lift * RAD[left_loc] + w_right * RAD[right_loc]
    SIF_3FLD = (RAD[in_loc] * IRR_out - RAD_out * IRR[in_loc]) / (
            IRR_out - IRR[in_loc])

    return SIF_3FLD


def threeFLD(path, pathout, left_wvl, right_wvl):
    # 程序入口，供调用

    if not os.path.exists(pathout):
        os.makedirs(pathout)

    path_dirs = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            path_dirs.append(os.path.join(name))
    path_dirs.sort()  # 按日期排序，需改成在窗口中选择日期文件夹

    # 以下为遍历每一天的数据进行处理
    for pathdir in path_dirs:
        folder = os.path.join(path, pathdir)
        filenames = os.listdir(folder)
        filenames.sort()

        if not os.path.exists(pathout):
            os.makedirs(pathout)
        SIF1d = pd.DataFrame(columns=('Time', '3FLD'))

        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')
            DataWvl = data['DataWvl'].ravel()
            IRR = data['IRR'].ravel()
            RAD = data['RAD'].ravel()
            Time = data['Time'].ravel()[0]
            in_loc = data['in_loc'].ravel()[0]
            in_wvl = DataWvl[in_loc]
            left_loc = np.where(np.abs(DataWvl - left_wvl) == np.min(np.abs(DataWvl - left_wvl)))
            right_loc = np.where(np.abs(DataWvl - right_wvl) == np.min(np.abs(DataWvl - right_wvl)))

            try:
                # 进行最终计算
                SIF_3FLD = fluor(in_loc, left_loc, right_loc, left_wvl, right_wvl, in_wvl, RAD, IRR)

                # 输出结果包含时间和反演结果
                SIF1d = pd.concat([SIF1d, pd.DataFrame(
                    {'Time': Time, '3FLD': SIF_3FLD},
                    index=[i])])
            except Exception as e:
                print(e)

        pathday = pathout + '\\' + folder[-10:] + '.csv'

        # 输出反演结果
        SIF1d.to_csv(pathday, sep=",", index=False)


if __name__ == '__main__':
    # 测试用例
    path = r'C:\Users\DZY\Desktop\P4\定标结果'  # 输入数据
    pathout = r'C:\Users\DZY\Desktop\P4\未经质量控制的反演结果\3FLD'  # 输出数据
    left_wvl = 758  # 氧气波段左肩
    right_wvl = 770  # 氧气波段右肩
    threeFLD(path, pathout, left_wvl, right_wvl)
