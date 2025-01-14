# BSF算法的实现
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import least_squares
import pandas as pd
from sklearn.linear_model import LinearRegression
import os


def calculate_cos_sza(year, month, day, hour, minute, lon, lat):
    # 根据时间和经纬度计算太阳天顶角的余弦值，输入的时间为北京时间
    d = (np.datetime64(f'{year}-{month:02d}-{day:02d}') - np.datetime64(f'{year}-01-01')).astype(
        'timedelta64[D]').astype(int) + 1  # 计算日期是一年中的第几天
    T = 2 * np.pi * (d - 1) / 365

    SD = (0.006918 - 0.399912 * np.cos(T) + 0.070257 * np.sin(T) - 0.006758 * np.cos(2 * T) + 0.000907 * np.sin(
        2 * T) - 0.002697 * np.cos(3 * T) + 0.00148 * np.sin(3 * T))
    ST = hour + minute / 60 + (lon - 120) / 15
    w = 15 * (ST - 12)

    SZA = 90 - np.degrees(
        np.arcsin(np.sin(np.radians(lat)) * np.sin(SD) + np.cos(np.radians(lat)) * np.cos(SD) * np.cos(np.radians(w))))
    cos_sza = np.cos(np.radians(SZA))

    return cos_sza


def readCSRF(CSRFfile, O2A_wvl, cos_sza):
    # 读取CSRF校正文件
    CSRF_ori = pd.read_csv(CSRFfile)
    CSRF_ori = np.array(CSRF_ori)
    CSRF = np.interp(O2A_wvl, CSRF_ori[:, 1], CSRF_ori[:, 0])
    CSRF = CSRF * np.cos(30 * np.pi / 180) / cos_sza

    return CSRF


def barometric(cos_sza, cos_vza, height, Tem):
    # 计算a的先验值
    g = 9.81  # m/s^2
    M = 0.02896968  # kg/mol
    T0 = Tem + 273  # K
    cp = 1004  # J/(kg K)
    R0 = 8.314462618  # J/(mol K)

    p_p0 = (1 - g * height / (cp * T0)) ** (cp * M / R0)

    x1 = (1 - p_p0) / p_p0
    aprior = 1 + x1 * (1 + cos_sza / cos_vza)

    return aprior


def cost4F(F, logx, y, fwlf, logxlim, cos_sza, cos_vza, normpiL, SRC, aprior, priorweight):
    # 迭代函数
    a = aprior
    index = np.where(logx < logxlim)  # 只取较深的波段
    logy2 = 0

    for k in range(3):
        Fra = F * fwlf * np.exp(logx * (a - 1) / (1 + cos_vza / cos_sza))
        y2 = (y * normpiL - Fra) / (normpiL - F * fwlf)
        y2[y2 < 0] = 1e-16  # 考虑到单位与论文里相差10000倍
        logy2 = np.log(y2) - (a - 1) * SRC
        # 执行线性回归
        logxdf = pd.DataFrame(logx)
        logy2df = pd.DataFrame(logy2)
        model = LinearRegression(fit_intercept=False)
        model.fit(logxdf, logy2df)
        a = model.coef_.ravel()[0]

    logymod = a * logx
    E = np.append(logymod[index] - logy2[index], priorweight * (a - aprior))
    # 去掉空值
    E = E[~np.isnan(E)]

    return E


def fluor(DataWvl, RAD, IRR, year, month, day, hour, minute, lon, lat, priorweight, left_wvl, right_wvl, height, Tem,
          in_loc):
    # 取从左肩到右肩的DataWvl所有值的索引
    index2 = np.where((DataWvl >= left_wvl) & (DataWvl <= right_wvl))
    O2A_wvl = DataWvl[index2]
    IRR_O2A = IRR[index2]
    RAD_O2A = RAD[index2]
    # 获取指定位置的索引
    in_loc_BSF = in_loc - index2[0][0]

    # 用left与right两处的值进行线性插值
    f1 = interp1d([O2A_wvl[0], O2A_wvl[-1]], [IRR_O2A[0], IRR_O2A[-1]], kind='linear')
    f2 = interp1d([O2A_wvl[0], O2A_wvl[-1]], [RAD_O2A[0], RAD_O2A[-1]], kind='linear')
    # 用插值后的值计算O2A的IRR和RAD
    normE = f1(O2A_wvl)
    normpiL = f2(O2A_wvl)

    logx = np.log(IRR_O2A / normE)
    y = RAD_O2A / normpiL

    # 采用retrievalF.m里定义的F在O2A波段的衰减函数
    flwf = 0.7 + 0.3 * (np.arange(len(O2A_wvl), 0, -1) / len(O2A_wvl))
    logxlim = 0
    cos_sza = calculate_cos_sza(year, month, day, hour, minute, lon, lat)
    cos_vza = 1
    SRC = readCSRF('res/SRCA.csv', O2A_wvl, cos_sza)
    aprior = barometric(cos_sza, cos_vza, height, Tem)

    # 定义目标函数
    def f(Fi):
        return cost4F(Fi, logx, y, flwf, logxlim, cos_sza, cos_vza, normpiL, SRC, aprior, priorweight)

    if min(logx) < logxlim:
        result = least_squares(f, 0, bounds=(-1E17, 1E17), method='trf')
        F = result.x
    else:
        F = 0

    SIF_BSF = F * flwf[in_loc_BSF]

    return SIF_BSF


def BSF(path, pathout, left_wvl, right_wvl, height, priorweight, Tem):
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

        year = int(folder[-10:-6])
        month = int(folder[-5:-3])
        day = int(folder[-2:])

        SIF1d = pd.DataFrame(columns=('Time', 'BSF'))

        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')

            DataWvl = data['DataWvl'].ravel()
            IRR = data['IRR'].ravel()
            RAD = data['RAD'].ravel()
            Time = data['Time'].ravel()[0]
            hour = int(Time[0:2])
            minute = int(Time[3:5])
            lon = float(data['longitude'].ravel()[0])
            lat = float(data['latitude'].ravel()[0])
            in_loc = data['in_loc'].ravel()[0]

            try:
            # 进行最终计算
                SIF_BSF = fluor(DataWvl, RAD, IRR, year, month, day, hour, minute, lon, lat, priorweight, left_wvl,
                                right_wvl, height, Tem, in_loc)

                # 输出结果包含时间和反演结果
                SIF1d = pd.concat([SIF1d, pd.DataFrame(
                    {'Time': Time, 'BSF': SIF_BSF},
                    index=[i])])
            except Exception as e:
                print(e)

        pathday = pathout + '\\' + folder[-10:] + '.csv'

        # 输出反演结果
        SIF1d.to_csv(pathday, sep=",", index=False)


if __name__ == '__main__':
    # 测试用例
    path = r'C:\Users\DZY\Desktop\P4\定标结果'  # 输入数据
    pathout = r'C:\Users\DZY\Desktop\P4\未经质量控制的反演结果\BSF'  # 输出数据
    left_wvl = 758  # 氧气波段左肩
    right_wvl = 770  # 氧气波段右肩
    height = 10  # 观测高度
    priorweight = 1  # 先验权重
    Tem = 20  # 温度
    BSF(path, pathout, left_wvl, right_wvl, height, priorweight, Tem)
