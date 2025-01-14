# SVD算法的实现
import numpy as np
import os
import pandas as pd


def fspectrum(wavelengths):
    # 形状函数参数,可变
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

    return hf


def simple_fspectrum(wavelengths, uh, dh):
    # 更简单的形状函数参数,可变
    hf = np.exp(-(wavelengths - uh) * (wavelengths - uh) / (2 * dh * dh))

    return hf


def SVD_train(IRR_matrix, DataWvl, uh, dh):
    try:
        # 对数据进行SVD分解
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
        # hf= fspectrum(wl)
        hf = simple_fspectrum(wl, uh, dh)

        # 进行最小二乘法所需的矩阵
        C = np.array(
            [V1, V1 * wl / 100, V1 * wl * wl / 10000, V2, V2 * wl / 100, V2 * wl * wl / 10000, V3, V4, V5, V6, V7, hf])
        C_pinv = np.linalg.pinv(C.T)

        return C_pinv

    except:
        print('SVD分解失败')


def fluor(C_pinv, RAD, DataWvl, in_loc, uh, dh):
    # 进行最小二乘法拟合，前期准备工作已在读取数据前完成
    C4 = np.dot(C_pinv, RAD)
    # 计算该处形状函数值
    # hf1 = fspectrum(DataWvl[in_loc]) # 使用较为复杂的形状函数
    hf1 = simple_fspectrum(DataWvl[in_loc], uh, dh)  # 更简单的形状函数
    SIF_SVD = C4[11] * hf1

    return SIF_SVD


def SVD(path, pathout, uh, dh):
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

        SIF1d = pd.DataFrame(columns=('Time', 'SVD'))

        IRR_list = []
        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')
            DataWvl = data['DataWvl'].ravel()
            IRR = data['IRR'].ravel()
            IRR_list.append(IRR)
        IRR_matrix = np.array(IRR_list)
        SVD_pinv = SVD_train(IRR_matrix, DataWvl, uh, dh)

        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')

            DataWvl = data['DataWvl'].ravel()
            RAD = data['RAD'].ravel()
            Time = data['Time'].ravel()[0]
            in_loc = data['in_loc'].ravel()[0]

            try:
                # 进行最终计算
                SIF_SVD = fluor(SVD_pinv, RAD, DataWvl, in_loc, uh, dh)

                # 输出结果包含时间和反演结果
                SIF1d = pd.concat([SIF1d, pd.DataFrame(
                    {'Time': Time, 'SVD': SIF_SVD},
                    index=[i])])

            except Exception as e:
                print(e)

        pathday = pathout + '\\' + folder[-10:] + '.csv'

        # 输出反演结果
        SIF1d.to_csv(pathday, sep=",", index=False)


if __name__ == '__main__':
    # 测试用例
    path = r'C:\Users\DZY\Desktop\P4\定标结果'  # 输入数据
    pathout = r'C:\Users\DZY\Desktop\P4\未经质量控制的反演结果\SVD'  # 输出数据
    uh = 740  # 荧光形状参数1
    dh = 10  # 荧光形状参数2
    SVD(path, pathout, uh, dh)
