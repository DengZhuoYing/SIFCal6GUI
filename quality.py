# 质量控制程序
import os
import pandas as pd
import numpy as np


def calculate_sza(year, month, day, hour, minute, lon, lat):
    # 根据时间和经纬度计算太阳天顶角，输入的时间为北京时间
    d = (np.datetime64(f'{year}-{month:02d}-{day:02d}') - np.datetime64(f'{year}-01-01')).astype(
        'timedelta64[D]').astype(int) + 1  # 计算日期是一年中的第几天
    T = 2 * np.pi * (d - 1) / 365

    SD = (0.006918 - 0.399912 * np.cos(T) + 0.070257 * np.sin(T) - 0.006758 * np.cos(2 * T) + 0.000907 * np.sin(
        2 * T) - 0.002697 * np.cos(3 * T) + 0.00148 * np.sin(3 * T))
    ST = hour + minute / 60 + (lon - 120) / 15
    w = 15 * (ST - 12)

    SZA = 90 - np.degrees(
        np.arcsin(np.sin(np.radians(lat)) * np.sin(SD) + np.cos(np.radians(lat)) * np.cos(SD) * np.cos(np.radians(w))))

    return SZA


def quality(path, pathout, pathout2, maxDN, maxRef, maxdelta, maxSZA):
    # 程序入口，供调用

    # 如果输出文件夹不存在，则创建
    if not os.path.exists(pathout):
        os.makedirs(pathout)
    if not os.path.exists(pathout2):
        os.makedirs(pathout2)

    path_dirs = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            path_dirs.append(os.path.join(name))
    path_dirs.sort()  # 按日期排序，需改成在窗口中选择日期文件夹
    "----------------------------------------------------------------------------------------------------------------------"
    # 以下为遍历每一天的数据进行处理

    for pathdir in path_dirs:
        year = int(pathdir[0:4])
        month = int(pathdir[5:7])
        day = int(pathdir[8:10])

        folder = os.path.join(path, pathdir)
        filenames = os.listdir(folder)
        filenames.sort()
        pathday = pathout + '\\' + folder[-10:]
        pathday2 = pathout2 + '\\' + folder[-10:]

        # 如果输出文件夹不存在，则创建
        if not os.path.exists(pathday):
            os.makedirs(pathday)
        if not os.path.exists(pathday2):
            os.makedirs(pathday2)

        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')
            IRR1 = data['IRR1']
            IRR2 = data['IRR2']
            IRRdelta = max(abs(IRR1 - IRR2) / IRR1)
            IrrDN_max = data['IrrDN_max']
            Ref = data['Ref']
            latitude = data['latitude'][0]
            longitude = data['longitude'][0]
            Time = data['Time'][0]
            hour = int(Time[0:2])
            minute = int(Time[3:5])
            SZA = calculate_sza(year, month, day, hour, minute, longitude, latitude)
            df = pd.DataFrame(data)

            if (max(Ref) < maxRef and maxDN * 0.5 < max(IrrDN_max) < maxDN and IRRdelta < maxdelta and SZA < maxSZA):
                df.to_csv(pathday + '\\' + filenames[i][:-4] + '.csv', index=False, sep=',')

            # 反射率不满足要求
            elif (max(Ref) >= maxRef):
                df.to_csv(pathday2 + '\\' + filenames[i][:-4] + '.csv', index=False, sep=',')

            # 两次入射辐射变化率不满足要求
            elif (IRRdelta >= maxdelta):
                df.to_csv(pathday2 + '\\' + filenames[i][:-4] + '.csv', index=False, sep=',')

            # 入射电流不满足要求
            elif (max(IrrDN_max) >= maxDN or max(IrrDN_max) <= maxDN * 0.5):
                df.to_csv(pathday2 + '\\' + filenames[i][:-4] + '.csv', index=False, sep=',')

            # 太阳天顶角不满足要求
            elif (SZA >= maxSZA):
                df.to_csv(pathday2 + '\\' + filenames[i][:-4] + '.csv', index=False, sep=',')


if __name__ == '__main__':
    # 测试用例
    path = r'C:\Users\DZY\Desktop\P4\定标结果'  # 输入数据
    pathout = r'C:\Users\DZY\Desktop\P4\质量合格'  # 输出数据
    pathout2 = r'C:\Users\DZY\Desktop\P4\质量不合格'  # 输出数据
    maxDN = 65535  # 饱和DN值
    maxRef = 1  # 最大反射率
    maxdelta = 0.1  # 最大入射辐照度变化率
    maxSZA = 70  # 最大太阳天顶角
    quality(path, pathout, pathout2, maxDN, maxRef, maxdelta, maxSZA)
