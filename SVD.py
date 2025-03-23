# SVD算法的实现
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt


def fspectrum(wavelengths):
    a1 = 2.14
    b1 = 682.6
    c1 = 11.2
    a2 = 60.32
    b2 = 737.8
    c2 = 11.36
    a3 = -59.89
    b3 = 737.8
    c3 = 11.33
    a4 = 2.03
    b4 = 727.3
    c4 = 48.98
    x = wavelengths
    hf = a1 * np.exp(-((x - b1) / c1) * ((x - b1) / c1)) + a2 * np.exp(
        -((x - b2) / c2) * ((x - b2) / c2)) + a3 * np.exp(-((x - b3) / c3) * ((x - b3) / c3)) + a4 * np.exp(
        -((x - b4) / c4) * ((x - b4) / c4))

    # hf = (hf - np.min(hf)) / (np.max(hf) - np.min(hf))

    return hf


def SVD_train(IRR_matrix, DataWvl):
    try:
        U, sigma, VT = np.linalg.svd(IRR_matrix, full_matrices=False)
        # Python与matlab分解得到的V矩阵互为转置
        V = VT.T

        if V.shape[1] < 7:
            V = np.hstack((V, np.zeros((V.shape[0], 7 - V.shape[1]))))

        V1 = V[:, 0]
        V2 = V[:, 1]
        V3 = V[:, 2]
        V4 = V[:, 3]
        V5 = V[:, 4]
        V6 = V[:, 5]
        V7 = V[:, 6]

        wl = DataWvl
        hf = fspectrum(wl)

        C = np.array(
            [hf, V1 * wl, V1 * wl ** 2, V1 * wl ** 3, V1 * wl ** 4, V1, V2, V3, V4, V5, V6, V7])

        C_pinv = np.linalg.pinv(C.T)

        return C_pinv

    except:
        print('SVD分解失败')


def fluor(C_pinv, RAD, DataWvl, in_loc):
    C4 = np.dot(C_pinv, RAD)
    hffull = fspectrum(DataWvl)
    hf1 = hffull[in_loc]
    SIF_SVD = C4[0] * hf1

    return SIF_SVD


def SVD(path, pathout):
    if not os.path.exists(pathout):
        os.makedirs(pathout)

    path_dirs = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            path_dirs.append(os.path.join(name))
    path_dirs.sort()

    for pathdir in path_dirs:
        folder = os.path.join(path, pathdir)
        filenames = os.listdir(folder)
        filenames.sort()
        if not os.path.exists(pathout):
            os.makedirs(pathout)

        SIF1d = pd.DataFrame(columns=('Time', 'SVD'))

        IRR_list = []

        start = 0
        DataWvl = pd.read_csv(fr'D:\SIF\多算法对比\NEWDATA\wl.csv', encoding='utf-8')['DataWvl'].ravel()[start:]
        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')
            IRR = data['IRR'].ravel()[start:]
            IRR_list.append(IRR)
        IRR_matrix = np.array(IRR_list)
        SVD_pinv = SVD_train(IRR_matrix, DataWvl)

        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')
            RAD = data['RAD'].ravel()[start:]
            Time = data['Time'].ravel()[0]
            in_loc = data['in_loc'].ravel()[0] - start

            SIF_SVD = fluor(SVD_pinv, RAD, DataWvl, in_loc)

            SIF1d = pd.concat([SIF1d, pd.DataFrame({'Time': Time, 'SVD': SIF_SVD}, index=[i])])

        pathday = pathout + '\\' + folder[-10:] + '.csv'

        # 输出反演结果
        SIF1d.to_csv(pathday, sep=",", index=False)


if __name__ == '__main__':
    path = r'D:\SIF\多算法对比\NEWDATA\质量合格'
    pathout = r'D:\SIF\多算法对比\NEWDATA\SVD'
    SVD(path, pathout)
