# 辐射定标的实现程序
import os, operator
import pandas as pd
import numpy as np


def oneday(i, filenames, folder, Para1, Para2, Para1T, Para2T):
    # 读取一天内某一时刻的源数据
    file = os.path.join(folder, filenames[i])
    Time = filenames[i][-12:-10] + ':' + filenames[i][-9:-7] + ':' + filenames[i][-6:-4]
    data = []
    with open(file, 'r') as csvfile:
        for line in csvfile:
            data.append(list(line.strip().split(',')))
        DataWvl = list(map(float, data[5][1:]))
        IrrT1 = float(data[10][2])  # 秒
        IrrDN1 = list(map(float, data[10][3:]))
        RadT = float(data[11][2])  # 秒
        RadDN = list(map(float, data[11][3:]))
        IrrT2 = float(data[12][2])  # 秒
        IrrDN2 = list(map(float, data[12][3:]))
        latitude = float(data[0][10].split('?')[0]) + float(data[0][10].split('?')[1]) / 60 + float(
            data[0][10].split('?')[2]) / 3600
        longitude = float(data[0][12].split('?')[0]) + float(data[0][12].split('?')[1]) / 60 + float(
            data[0][12].split('?')[2]) / 3600

    op = operator.eq(DataWvl, Para1['wvl'])
    if op.all():
        IRR1 = np.array([a * b * Para1T / IrrT1 / np.pi for a, b in zip(IrrDN1, Para1['para'])])  # W/m2/nm/sr
        RAD = np.array([a * b * Para2T / RadT for a, b in zip(RadDN, Para2['para'])])  # W/m2/nm/sr
        IRR2 = np.array([a * b * Para1T / IrrT2 / np.pi for a, b in zip(IrrDN2, Para1['para'])])  # W/m2/nm/sr
    else:
        IrrPara = np.interp(DataWvl, Para1['wvl'], Para1['para'])
        RadPara = np.interp(DataWvl, Para2['wvl'], Para2['para'])
        IRR1 = np.array([a * b * Para1T / IrrT1 / np.pi for a, b in zip(IrrDN1, IrrPara)])  # W/m2/nm/sr
        RAD = np.array([a * b * Para2T / RadT for a, b in zip(RadDN, RadPara)])  # W/m2/nm/sr
        IRR2 = np.array([a * b * Para1T / IrrT2 / np.pi for a, b in zip(IrrDN2, IrrPara)])  # W/m2/nm/sr

    DataWvl = np.array(DataWvl)
    loc_730 = np.where(np.abs(DataWvl - 730) == np.min(np.abs(DataWvl - 730)))[0][0]  # 730nm处的位置

    # 从730nm处开始截取数据
    DataWvl = DataWvl[loc_730:]
    IRR1 = IRR1[loc_730:]
    RAD = RAD[loc_730:]
    IRR2 = IRR2[loc_730:]

    IRR = (IRR1 + IRR2) / 2
    IrrDN_max = max(IrrDN1[loc_730:], IrrDN2[loc_730:])

    return DataWvl, IRR, IRR1, RAD, IRR2, IrrDN_max, Time, latitude, longitude


def radiation_correction(path, pathout, pathdb1, pathdb2, pathwl):
    # 程序入口，供调用

    # 如果输出文件夹不存在，则创建
    if not os.path.exists(pathout):
        os.makedirs(pathout)

    ## 读取每日数据文件夹
    path_dirs = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            path_dirs.append(os.path.join(name))
    path_dirs.sort()  # 按日期排序

    # 读取辐射定标文件
    Para1 = pd.read_csv(pathdb1, encoding='utf-8')
    Para2 = pd.read_csv(pathdb2, encoding='utf-8')

    Para1T = int(Para1.columns.values[0])  # 列名为定标的积分时间
    Para2T = int(Para2.columns.values[0])  # 列名为定标的积分时间

    Para1.columns = ['para']
    Para1['wvl'] = Para1.index
    Para2.columns = ['para']
    Para2['wvl'] = Para2.index

    wlfile = pd.read_csv(pathwl, encoding='utf-8')
    in_loc = np.where(np.abs(wlfile['DataWvl'] - 760) == np.min(np.abs(wlfile['DataWvl'] - 760)))[0][0]

    # 以下为遍历每一天的数据进行处理
    for pathdir in path_dirs:
        folder = os.path.join(path, pathdir)
        filenames = os.listdir(folder)
        filenames.sort()
        pathday = pathout + '\\' + folder[-10:]
        if not os.path.exists(pathday):
            os.makedirs(pathday)
        for i in range(0, len(filenames)):
            DataWvl, IRR, IRR1, RAD, IRR2, IrrDN_max, Time, latitude, longitude = oneday(i, filenames, folder, Para1,
                                                                                         Para2, Para1T, Para2T)

            # 根据标准波长文件进行插值
            IRR = np.interp(wlfile['DataWvl'], DataWvl, IRR)
            RAD = np.interp(wlfile['DataWvl'], DataWvl, RAD)
            IRR1 = np.interp(wlfile['DataWvl'], DataWvl, IRR1)
            IRR2 = np.interp(wlfile['DataWvl'], DataWvl, IRR2)
            IrrDN_max = np.interp(wlfile['DataWvl'], DataWvl, IrrDN_max)
            Ref = RAD / IRR

            data = {'DataWvl': wlfile['DataWvl'], 'IRR': IRR, 'IRR1': IRR1, 'RAD': RAD, 'IRR2': IRR2,
                    'IrrDN_max': IrrDN_max,
                    'Time': Time, 'Ref': Ref, 'latitude': latitude, 'longitude': longitude, 'in_loc': in_loc}
            df = pd.DataFrame(data)

            # 输出定标结果
            df.to_csv(pathday + '\\' + filenames[i][:-4] + '.csv', index=False, sep=',')


if __name__ == '__main__':
    # 测试用例
    path = r'D:\1\SIF\code\GUI\SIFCal6GUI\Data\源数据'  # 输入数据
    pathout = r'D:\1\SIF\code\GUI\SIFCal6GUI\Data\定标结果'  # 输出数据
    pathdb1 = r'D:\1\SIF\code\GUI\SIFCal6GUI\Data\辐射定标文件\FSNISIF1.csv'  # 入射辐射定标文件
    pathdb2 = r'D:\1\SIF\code\GUI\SIFCal6GUI\Data\辐射定标文件\FSNISIF2.csv'  # 反射辐射定标文件
    pathwl = r'D:\1\SIF\code\GUI\SIFCal6GUI\Data\wl.csv'  # 标准波长文件
    radiation_correction(path, pathout, pathdb1, pathdb2, pathwl)
