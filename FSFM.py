# F-SFM算法的实现
import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from sklearn.decomposition import PCA
from scipy.optimize import curve_fit
from scipy.linalg import lstsq


def FPCA(path_wvl, path_reflectance, path_fluorescence, DataWvl, sif_com, left, right, ref_com, interp_scope,
         interp_noref):
    # 根据scope模型数据进行训练
    # 反射率部分
    columns_ref = pd.read_table(path_wvl, sep='\s+', skiprows=2, header=None)
    data_ref = pd.read_table(path_reflectance, sep='\s+', skiprows=2, header=None)
    df_ref = pd.concat([columns_ref, data_ref])
    selected_columns_ref = df_ref.columns[(df_ref.iloc[0] >= 400.0) & (df_ref.iloc[0] <= 3000.0)]
    selected_df_ref = df_ref[selected_columns_ref]
    selected_ref = np.array(selected_df_ref)

    # 将模拟值插值至数据波段
    f1 = interp1d(selected_ref[0, :], selected_ref[1:, :], kind=interp_scope)
    selected_ref = f1(DataWvl)

    # 剔除原吸收波段的反射率
    selected_ref = np.hstack((selected_ref[:, :left], selected_ref[:, right:]))
    selectet_wl = np.hstack((DataWvl[:left], DataWvl[right:]))
    f2 = interp1d(selectet_wl, selected_ref, kind=interp_noref)
    selected_ref = f2(DataWvl)
    selected_df_ref = pd.DataFrame(selected_ref)

    # 保留前60个主成分,否则重建的反射率差别过大s
    pca = PCA(n_components=ref_com, random_state=0)
    pca.fit(selected_df_ref.T)
    transformed_ref = pca.transform(selected_df_ref.T)
    transformed_df_ref = pd.DataFrame(transformed_ref)

    # SIF部分
    columns_wl = pd.read_table(path_wvl, sep='\s+', skiprows=2, header=None, )
    columns_wl = columns_wl.iloc[:, 240:450]
    columns_sif = pd.read_table(path_fluorescence, sep='\s+', skiprows=2, header=None)
    columns_sif = columns_sif.iloc[:, 0:210]
    wl = np.array(columns_wl).ravel()
    sif = np.array(columns_sif)

    # 将模拟值插值至数据波段
    f3 = interp1d(wl, sif[:, :], kind=interp_scope)
    seleted_sif = f3(DataWvl) / 1000  # 统一单位为W/m2/nm/sr
    selected_df_sif = pd.DataFrame(seleted_sif)

    # 保留前5个主成分
    pca = PCA(n_components=sif_com, random_state=0)
    pca.fit(selected_df_sif.T)
    transformed_sif = pca.transform(selected_df_sif.T)
    transformed_df_sif = pd.DataFrame(transformed_sif)
    # print(selected_df_sif.T)
    # print(transformed_df_sif)
    # print(transformed_df_ref)

    return transformed_df_ref, transformed_df_sif


# sif主成分数量为5时使用的拟合函数
def nonlinear_func(x, a, b, j1, j2, j3, j4, j5):
    sif_part = 0
    jnp = np.array([j1, j2, j3, j4, j5])
    for i in range(5):
        sif_part += jnp[i] * x[i + 2]

    return x[1] * (a * x[0] + b) + sif_part


# sif主成分数量为10时使用的拟合函数
# def nonlinear_func(x, a, b, j1, j2, j3, j4, j5,j6,j7,j8,j9,j10):
#     sif_part = 0
#     jnp = np.array([j1, j2, j3, j4, j5,j6,j7,j8,j9,j10])
#     for i in range(10):
#         sif_part += jnp[i] * x[i + 2]
#
#     return x[1] * (a * x[0] + b) + sif_part


def fluor(in_loc, RAD, IRR, Ref, transformed_df_ref, transformed_df_sif, sif_com, left, right, k, DataWvl):
    # 使用主成分重建反射率
    ref_60 = np.array(transformed_df_ref)
    weights = np.zeros(len(DataWvl))
    weights[left:right] = 1
    sqrt_weights = np.sqrt(1 - weights)
    A_weighted = ref_60 * sqrt_weights[:, np.newaxis]
    b_weighted = Ref * sqrt_weights
    # 将为0的值剔除
    A_weighted2 = A_weighted[~np.all(A_weighted == 0, axis=1)]
    b_weighted2 = b_weighted[~np.all(A_weighted == 0, axis=1)]
    ref_k, _, _, _ = lstsq(A_weighted2, b_weighted2, lapack_driver='gelsy')
    ref_pca = np.dot(transformed_df_ref, ref_k)
    ref_pca_fit = ref_pca.ravel()[left:right]

    # 拟合参数准备
    IRR_fit = IRR[left:right]
    RAD_fit = RAD[left:right]
    sif_np = np.array(transformed_df_sif[left:right])
    x = np.array(sif_np)
    x2 = np.vstack((ref_pca_fit, IRR_fit))
    x3 = np.hstack((x2.T, x)).T
    initial_guess = np.concatenate(([1, 0], np.zeros(sif_com)))  # 初始猜测值
    lbounds = np.concatenate(([0, -1], np.full(sif_com, -np.inf)))  # 初始猜测值
    ubounds = np.concatenate(([2, 1], np.full(sif_com, np.inf)))  # 初始猜测值
    params, _ = curve_fit(nonlinear_func, x3, RAD_fit, p0=initial_guess, bounds=(lbounds, ubounds), method='trf')
    params_pca = params[2:2 + sif_com]

    # 得到用主成分模拟的全波段荧光光谱
    sif_pca = np.dot(transformed_df_sif, params_pca)

    # 进行迭代
    for i in range(0, k):
        # 获得新的反射率
        ref_pca = (RAD - sif_pca) / IRR
        ref_pca = ref_pca.ravel()
        A_weighted = ref_60 * sqrt_weights[:, np.newaxis]
        b_weighted = ref_pca * sqrt_weights
        ref_k, _, _, _ = lstsq(A_weighted, b_weighted, lapack_driver='gelsy')
        ref_pca = np.dot(transformed_df_ref, ref_k)
        ref_pca_fit = ref_pca[left:right]

        # 拟合参数准备
        x = np.array(sif_np)
        x2 = np.vstack((ref_pca_fit, IRR_fit))
        x3 = np.hstack((x2.T, x)).T
        initial_guess = np.concatenate(([1, 0], np.zeros(sif_com)))  # 初始猜测值
        lbounds = np.concatenate(([0, -1], np.full(sif_com, -np.inf)))  # 初始猜测值
        ubounds = np.concatenate(([2, 1], np.full(sif_com, np.inf)))  # 初始猜测值
        params, _ = curve_fit(nonlinear_func, x3, RAD_fit, p0=initial_guess, bounds=(lbounds, ubounds), method='trf')
        params_pca = params[2:2 + sif_com]

        # 得到用主成分模拟的全波段荧光光谱
        sif_pca = np.dot(transformed_df_sif, params_pca)

    SIF_FSFM = sif_pca.ravel()[in_loc]

    return SIF_FSFM


def FSFM(path, pathout, left_wvl, right_wvl, ref_com, k, interp_scope, interp_noref):
    # 程序入口，供调用

    if not os.path.exists(pathout):
        os.makedirs(pathout)

    files = os.listdir(path)
    path2 = path + '\\' + files[0]
    files2 = os.listdir(path2)
    data = pd.read_csv(path + '\\' + files[0] + '\\' + files2[0])  # 获取第一个文件夹的第一个文件
    DataWvl = data['DataWvl'].ravel()
    left = np.where(np.abs(DataWvl - left_wvl) == np.min(np.abs(DataWvl - left_wvl)))[0][0]
    right = np.where(np.abs(DataWvl - right_wvl) == np.min(np.abs(DataWvl - right_wvl)))[0][0]

    sif_com = 5  # sif主成分数，该参数不可调

    # FSFM算法数据训练
    transformed_df_ref, transformed_df_sif = FPCA('res/scope/wl.dat', 'res/scope/reflectance.dat',
                                                  'res/scope/fluorescence.dat',
                                                  DataWvl, sif_com, left, right, ref_com, interp_scope, interp_noref)

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

        SIF1d = pd.DataFrame(columns=('Time', 'FSFM'))

        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')
            DataWvl = data['DataWvl'].ravel()
            IRR = data['IRR'].ravel()
            RAD = data['RAD'].ravel()
            Time = data['Time'].ravel()[0]
            Ref = data['Ref'].ravel()
            in_loc = data['in_loc'].ravel()[0]

            # 进行最终计算
            try:
                SIF_FSFM = fluor(in_loc, RAD, IRR, Ref, transformed_df_ref, transformed_df_sif, sif_com, left, right, k,
                                 DataWvl)

                # 输出结果包含时间和反演结果
                SIF1d = pd.concat([SIF1d, pd.DataFrame({'Time': Time, 'FSFM': SIF_FSFM}, index=[i])])

            except Exception as e:
                print(e)

        pathday = pathout + '\\' + folder[-10:] + '.csv'

        # 输出反演结果
        SIF1d.to_csv(pathday, sep=",", index=False)


if __name__ == '__main__':
    # 测试用例
    path = r'C:\Users\DZY\Desktop\P4\定标结果'  # 输入数据
    pathout = r'C:\Users\DZY\Desktop\P4\未经质量控制的反演结果\FSFM'  # 输出数据
    left_wvl = 759.8  # 最小二乘法拟合波段左肩波长
    right_wvl = 761.5  # 最小二乘法拟合波段右肩波长
    ref_com = 60  # 反射率主成分数
    k = 0  # 迭代次数
    interp_scope = 'linear'  # 反射率插值方式
    interp_noref = 'linear'  # 反射率剔除波段后插值方式
    FSFM(path, pathout, left_wvl, right_wvl, ref_com, k, interp_scope, interp_noref)
