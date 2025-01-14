# 本程序用于多线程的创建，防止程序卡顿
from PyQt5.QtCore import QThread, pyqtSignal
from radiation_correction import radiation_correction
from quality import quality
from sFLD import sFLD
from threeFLD import threeFLD
from iFLD import iFLD
from FSFM import FSFM
from SVD import SVD
from BSF import BSF


# 线程类
class mythread(QThread):
    d = pyqtSignal(int)

    def __init__(self, index, data):
        super(mythread, self).__init__()
        self.index = index
        self._data = data

    def run(self) -> None:

        if self.index == 0:
            path = self._data[0]
            pathout = self._data[1]
            pathdb1 = self._data[2]
            pathdb2 = self._data[3]
            pathwl = self._data[4]
            print("开始辐射定标")

            radiation_correction(path, pathout, pathdb1, pathdb2, pathwl)

            print("辐射定标完成")

        elif self.index == 1:

            path = self._data[0]
            pathout = self._data[1]
            pathout2 = self._data[2]
            self.paramQual = self._data[3]
            # 以下参数可调
            maxDN = float(self.paramQual[0][1])  # 饱和DN值
            maxRef = float(self.paramQual[1][1])  # 最大反射率
            maxdelta = float(self.paramQual[2][1]) / 100  # 最大IRR差异
            maxSZA = float(self.paramQual[4][1])  # 最大太阳天顶角
            print('质量控制参数:', '饱和DN值:', maxDN, '最大反射率:', maxRef, '最大IRR差异:', maxdelta,
                  '最大太阳天顶角:', maxSZA)
            print("开始质量控制")
            quality(path, pathout, pathout2, maxDN, maxRef, maxdelta, maxSZA)
            print("质量控制完成")

        elif self.index == 2:

            path = self._data[0]
            pathout = self._data[1]
            self.params = self._data[-1]
            nowIndex = self._data[-2]
            if nowIndex == 0:

                print('开始sFLD算法处理')
                print('sFLD参数,', float(self.params['sFLD'][0][1]))

                sFLD(path, pathout, float(self.params['sFLD'][0][1]))

                print('sFLD处理完成')

            elif nowIndex == 1:

                print('开始3FLD算法处理')
                print('3FLD参数,', float(self.params['3FLD'][0][1]), float(self.params['3FLD'][1][1]))

                threeFLD(path, pathout, float(self.params['3FLD'][0][1]), float(self.params['3FLD'][1][1]))

                print('3FLD处理完成')

            elif nowIndex == 2:

                print('开始iFLD算法处理')
                print('iFLD参数,', float(self.params['iFLD'][0][1]), float(self.params['iFLD'][1][1]),
                      float(self.params['iFLD'][2][1]), int(self.params['iFLD'][3][1]),
                      int(self.params['iFLD'][4][1]))

                iFLD(path, pathout, float(self.params['iFLD'][0][1]), float(self.params['iFLD'][1][1]),
                     float(self.params['iFLD'][2][1]), int(self.params['iFLD'][3][1]),
                     int(self.params['iFLD'][4][1]))

                print('iFLD处理完成')

            elif nowIndex == 3:

                print('开始F-SFM算法处理')
                print('F-SFM参数,', float(self.params['F-SFM'][0][1]), float(self.params['F-SFM'][1][1]),
                      int(self.params['F-SFM'][2][1]), int(self.params['F-SFM'][3][1]), self.params['F-SFM'][4][1],
                      self.params['F-SFM'][5][1])

                FSFM(path, pathout, float(self.params['F-SFM'][0][1]), float(self.params['F-SFM'][1][1]),
                     int(self.params['F-SFM'][2][1]), int(self.params['F-SFM'][3][1]), self.params['F-SFM'][4][1],
                     self.params['F-SFM'][5][1])

                print('FSFM处理完成')

            elif nowIndex == 4:

                print('开始SVD算法处理')
                print('SVD参数,', float(self.params['SVD'][0][1]), float(self.params['SVD'][1][1]))

                SVD(path, pathout, float(self.params['SVD'][0][1]), float(self.params['SVD'][1][1]))

                print('SVD处理完成')

            elif nowIndex == 5:

                print('开始BSF算法处理')
                print('BSF参数,', float(self.params['BSF'][0][1]), float(self.params['BSF'][1][1]),
                      float(self.params['BSF'][2][1]),
                      float(self.params['BSF'][3][1]), float(self.params['BSF'][4][1]))

                BSF(path, pathout, float(self.params['BSF'][0][1]), float(self.params['BSF'][1][1]),
                    float(self.params['BSF'][2][1]),
                    float(self.params['BSF'][3][1]), float(self.params['BSF'][4][1]))

                print('BSF处理完成')

        self.d.emit(self.index)
