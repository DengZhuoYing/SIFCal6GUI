import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from scipy.interpolate import splrep, splev
from sklearn.decomposition import PCA


def FPCA(path_wvl, path_fluorescence, DataWvl, sif_com, interp_scope):
    columns_wl = pd.read_table(path_wvl, sep='\s+', skiprows=2, header=None, )
    columns_wl = columns_wl.iloc[:, 240:450]
    columns_sif = pd.read_table(path_fluorescence, sep='\s+', skiprows=2, header=None)
    columns_sif = columns_sif.iloc[:, 0:210]
    wl = np.array(columns_wl).ravel()
    sif = np.array(columns_sif)

    f = interp1d(wl, sif[:, :], kind=interp_scope)
    seleted_sif = f(DataWvl) / 1000  # 统一单位为W/m2/nm/sr
    selected_df_sif = pd.DataFrame(seleted_sif)

    pca = PCA(n_components=sif_com, random_state=0)
    pca.fit(selected_df_sif.T)
    transformed_sif = pca.transform(selected_df_sif.T)
    transformed_df_sif = pd.DataFrame(transformed_sif)

    return transformed_df_sif


def nonlinear_func(x, a, b, j1, j2, j3, j4, j5):
    sif_part = 0
    jnp = np.array([j1, j2, j3, j4, j5])
    for i in range(5):
        sif_part += jnp[i] * x[i + 2]

    return x[1] * (a * x[0] + b) + sif_part


def fluor(in_loc, RAD, IRR, Ref, transformed_df_sif, sif_com, left, right, DataWvl):
    weights = np.full(len(DataWvl), 1)
    weights[left:right] = 0

    tck_Ref = splrep(DataWvl, Ref, w=weights, k=3)
    ref_inter = splev(DataWvl[left:right], tck_Ref)

    IRR_fit = IRR[left:right]
    RAD_fit = RAD[left:right]
    sif_np = np.array(transformed_df_sif[left:right])
    x = np.array(sif_np)
    x2 = np.vstack((ref_inter * IRR_fit, IRR_fit))
    x3 = np.hstack((x2.T, x)).T

    initial_guess = np.concatenate(([1, 0], np.zeros(sif_com)))  # 初始猜测值
    lbounds = np.concatenate(([0, -1], np.full(sif_com, -np.inf)))  # 初始猜测值
    ubounds = np.concatenate(([2, 1], np.full(sif_com, np.inf)))  # 初始猜测值

    params, _ = curve_fit(nonlinear_func, x3, RAD_fit, p0=initial_guess, bounds=(lbounds, ubounds), method='trf')
    params_pca = params[2:2 + sif_com]
    sif_pca = np.dot(transformed_df_sif, params_pca)
    SIF_SFM = sif_pca.ravel()[in_loc]

    return SIF_SFM


def SFM(path, pathout, left_wvl, right_wvl):
    if not os.path.exists(pathout):
        os.makedirs(pathout)

    files = os.listdir(path)
    path2 = path + '\\' + files[0]
    files2 = os.listdir(path2)
    data = pd.read_csv(path + '\\' + files[0] + '\\' + files2[0])
    DataWvl = data['DataWvl'].ravel()
    left = np.where(np.abs(DataWvl - left_wvl) == np.min(np.abs(DataWvl - left_wvl)))[0][0]
    right = np.where(np.abs(DataWvl - right_wvl) == np.min(np.abs(DataWvl - right_wvl)))[0][0]

    sif_com = 5

    transformed_df_sif = FPCA('res/scope/wl.dat', 'res/scope/fluorescence.dat', DataWvl, sif_com, 3)

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

        SIF1d = pd.DataFrame(columns=('Time', 'SFM'))

        for i in range(0, len(filenames)):
            data = pd.read_csv(folder + '\\' + filenames[i], encoding='utf-8')
            DataWvl = data['DataWvl'].ravel()
            IRR = data['IRR'].ravel()
            RAD = data['RAD'].ravel()
            Time = data['Time'].ravel()[0]
            Ref = data['Ref'].ravel()
            in_loc = data['in_loc'].ravel()[0]

            SIF_SFM = fluor(in_loc, RAD, IRR, Ref, transformed_df_sif, sif_com, left, right, DataWvl)
            SIF1d = pd.concat([SIF1d, pd.DataFrame({'Time': Time, 'SFM': SIF_SFM}, index=[i])])

        pathday = pathout + '\\' + folder[-10:] + '.csv'

        SIF1d.to_csv(pathday, sep=",", index=False)


if __name__ == '__main__':
    path = r'D:\SIF\多算法对比\NEWDATA\质量合格'  # 输入数据
    pathout = fr'D:\SIF\多算法对比\NEWDATA\SFM'  # 输出数据
    left_wvl = 758
    right_wvl = 770
    SFM(path, pathout, left_wvl, right_wvl)
