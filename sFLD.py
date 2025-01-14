# sFLD算法的实现
import os
import numpy as np
import pandas as pd


def fluor(in_loc, out_loc, RAD, IRR):
    # sFLD算法，根据公式直接计算
    SIF_sFLD = (RAD[in_loc] * IRR[out_loc] - RAD[out_loc] * IRR[in_loc]) / (
            IRR[out_loc] - IRR[in_loc])

    return SIF_sFLD


# 输入参数
def sFLD(path, pathout, out_wvl):
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
        filenames.sort()  # 对获取的文件按字符键值排序

        if not os.path.exists(pathout):
            os.makedirs(pathout)
        SIF1d = pd.DataFrame(columns=('Time', 'sFLD'))

        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')
            DataWvl = data['DataWvl'].ravel()
            IRR = data['IRR'].ravel()
            RAD = data['RAD'].ravel()
            Time = data['Time'].ravel()[0]
            in_loc = data['in_loc'].ravel()[0]

            out_loc = np.where(np.abs(DataWvl - out_wvl) == np.min(np.abs(DataWvl - out_wvl)))
            try:
                # 进行最终计算
                SIF_sFLD = fluor(in_loc, out_loc, RAD, IRR)

                # 输出结果包含时间和反演结果
                SIF1d = pd.concat([SIF1d, pd.DataFrame(
                    {'Time': Time, 'sFLD': SIF_sFLD},
                    index=[i])])
            except Exception as e:
                print(e)

        pathday = pathout + '\\' + folder[-10:] + '.csv'
        # 输出反演结果
        SIF1d.to_csv(pathday, sep=",", index=False)


if __name__ == '__main__':
    # 测试用例
    path = r'C:\Users\DZY\Desktop\P4\定标结果'  # 输入数据
    pathout = r'C:\Users\DZY\Desktop\P4\未经质量控制的反演结果\sFLD'  # 输出数据
    out_wvl = 758  # 吸收线外波段
    sFLD(path, pathout, out_wvl)
