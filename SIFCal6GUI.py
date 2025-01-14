# 程序入口
import sys, os
import pandas as pd
# 导入图形组件库
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QAbstractItemView, QVBoxLayout, \
    QHeaderView, QTableWidgetItem
from PyQt5.QtCore import QCoreApplication, Qt
# 导入做好的界面库
from ui import Ui_MainWindow
from figureFunc import MyFigure
# 导入多线程
from threadFunc import mythread


# 主窗口类
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # 继承(QMainWindow,Ui_MainWindow)父类的属性
        super(MainWindow, self).__init__()
        # 初始化界面组件
        self.setupUi(self)
        self.pathout = None

        '''嵌入画图界面'''
        self.F1 = MyFigure()
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.F1)
        self.layout1.setContentsMargins(0, 0, 0, 0)
        self.widget_2.setLayout(self.layout1)

        '''辐射定标功能'''
        # 源数据选择
        self.pushButton.clicked.connect(lambda: self.load(0))
        # 辐射定标结果文件选择
        self.pushButton_3.clicked.connect(lambda: self.load(1))
        # 辐射定标
        self.pushButton_2.clicked.connect(self.pretreatment)

        '''质量控制'''
        self.pushButton_4.clicked.connect(lambda: self.load(2))
        self.pushButton_5.clicked.connect(lambda: self.load(3))
        self.pushButton_8.clicked.connect(lambda: self.load(4))
        self.pushButton_6.clicked.connect(self.qualityControl)

        '''算法计算'''
        self.pushButton_9.clicked.connect(lambda: self.load(5))
        self.pushButton_10.clicked.connect(lambda: self.load(6))
        self.pushButton_7.clicked.connect(self.cal)
        self.pushButton_11.clicked.connect(self.plotFig)

        # 初始化参数
        self.params = {
            'sFLD': [
                ['吸收线外波段', 758]
            ],
            '3FLD': [
                ['吸收线左波段', 758],
                ['吸收线右波段', 770]
            ],
            'iFLD': [
                ['吸收线外波段', 758],
                ['吸收线左波段', 758],
                ['吸收线右波段', 770],
                ['反射光谱插值次数', 3],
                ['入射光谱插值次数', 3]
            ],
            'F-SFM': [
                ['拟合左端波段', 759.5],
                ['拟合右端波段', 761.5],
                ['反射率主成分数', 60],
                ['迭代次数', 0],
                ['模拟值插值法', 'linear'],
                ['剔除氧气带插值法', 'linear']
            ],
            'SVD': [
                ['形状函数均值', 740],
                ['形状函数标准差', 10]
            ],
            'BSF': [
                ['吸收线左波段', 758],
                ['吸收线右波段', 770],
                ['观测高度', 10],
                ['先验权重', 1],
                ['温度', 20]
            ],

        }
        # 加载参数
        self.loadParams()

        # 算法跳转
        self.radioButton.toggled.connect(self.loadParams)
        self.radioButton_2.toggled.connect(self.loadParams)
        self.radioButton_3.toggled.connect(self.loadParams)
        self.radioButton_4.toggled.connect(self.loadParams)
        self.radioButton_5.toggled.connect(self.loadParams)
        self.radioButton_6.toggled.connect(self.loadParams)
        # 表格修改事件
        # 连接itemChanged信号到处理函数
        self.tableWidget.cellChanged.connect(self.handleItemChanged)

        '''质量参数'''
        self.paramQual = [
            ["最大DN值", 65535],
            ["最大反射率", 1],
            ['辐照度变化率%', 10],
            ['暗电流最大占比%', 5],
            ['最大太阳天顶角', 70]

        ]
        self.showTable(self.tableWidget_2, self.paramQual)
        self.tableWidget_2.cellChanged.connect(self.handleItemChanged1)

    def handleItemChanged1(self, row, col):
        # 质量参数修改
        if col == 1:
            new_text = self.tableWidget_2.item(row, col).text()

            self.paramQual[row][1] = new_text

    def handleItemChanged(self, row, col):
        # 参数修改
        if col == 1:
            new_text = self.tableWidget.item(row, col).text()
            # 根据不同算法导入不同参数
            if self.radioButton.isChecked():
                self.params['sFLD'][row][1] = new_text
            elif self.radioButton_2.isChecked():
                self.params['3FLD'][row][1] = new_text
            elif self.radioButton_3.isChecked():
                self.params['iFLD'][row][1] = new_text
            elif self.radioButton_4.isChecked():
                self.params['F-SFM'][row][1] = new_text
            elif self.radioButton_5.isChecked():
                self.params['SVD'][row][1] = new_text
            elif self.radioButton_6.isChecked():
                self.params['BSF'][row][1] = new_text

    def cal(self):
        # 读取质量控制后的文件
        path = self.lineEdit_6.text()  # 输入文件夹
        pathout = self.lineEdit_7.text()  # 输出文件夹
        if path and pathout:
            self.pushButton_9.setEnabled(False)
            self.pushButton_10.setEnabled(False)
            self.pushButton_7.setEnabled(False)
            if self.radioButton.isChecked():
                self._thread = mythread(2, [path, pathout, 0, self.params])
            elif self.radioButton_2.isChecked():
                self._thread = mythread(2, [path, pathout, 1, self.params])
            elif self.radioButton_3.isChecked():
                self._thread = mythread(2, [path, pathout, 2, self.params])
            elif self.radioButton_4.isChecked():
                self._thread = mythread(2, [path, pathout, 3, self.params])
            elif self.radioButton_5.isChecked():
                self._thread = mythread(2, [path, pathout, 4, self.params])
            elif self.radioButton_6.isChecked():
                self._thread = mythread(2, [path, pathout, 5, self.params])

            # 更新算法结果，以便绘图展示
            self.pathout = pathout
            self._thread.d.connect(self.refrsh)
            self._thread.start()

            self.pushButton_7.setText('正在处理...')

        else:
            QMessageBox.warning(self, "警告", "存在未选择路径", QMessageBox.Yes)

    def plotFig(self):
        # 画图
        self.F1.axes.cla()
        # 获取结果文件夹的csv
        csvPath = os.path.join(self.pathout, self.comboBox.currentText())
        df = pd.read_csv(csvPath)
        columns = df.columns.tolist()

        _x = df[columns[0]]  # 获取横坐标
        _y = df[columns[1]]  # 获取纵坐标

        self.F1.axes.plot(range(len(_y)), _y)
        self.F1.axes.set_xlabel(columns[0])
        self.F1.axes.set_ylabel('$SIF_{760}\ (W\ m^{2}\ nm^{-1}\ sr^{-1})$')  # 展示的结果为760nm处的SIF值
        self.F1.axes.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

        _inter = int(len(_x) / 5) + 1  # 设置横轴刻度，不设置所有时刻
        self.F1.axes.set_xticks(range(0, len(_x), _inter), _x[::_inter])
        self.F1.axes.set_title(os.path.basename(csvPath[:-4]))  # 设置展示标题
        self.F1.axes.grid()
        self.F1.draw()

    def loadParams(self):
        # 根据不同算法导入不同参数
        if self.radioButton.isChecked():
            data = self.params['sFLD']
        elif self.radioButton_2.isChecked():
            data = self.params['3FLD']
        elif self.radioButton_3.isChecked():
            data = self.params['iFLD']
        elif self.radioButton_4.isChecked():
            data = self.params['F-SFM']
        elif self.radioButton_5.isChecked():
            data = self.params['SVD']
        elif self.radioButton_6.isChecked():
            data = self.params['BSF']
        self.showTable(self.tableWidget, data)

    def showTable(self, tableWidget, data):
        # 参数输入表格的设置
        tableWidget.clear()
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        tableWidget.setRowCount(len(data))  # 设置表格的行数
        tableWidget.setColumnCount(2)  # 设置表格的列数
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置纵向标签不可见
        tableWidget.verticalHeader().setVisible(False)
        tableWidget.horizontalHeader().setVisible(False)
        for i in range(len(data)):
            for m in range(2):
                newItem = QTableWidgetItem(str(data[i][m]))
                if m == 0:
                    newItem.setFlags(newItem.flags() & ~Qt.ItemIsEditable)
                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                tableWidget.setItem(i, m, newItem)  # 行列

    def load(self, index):
        # 选择不同的文件夹导入数据

        if index == 0:
            directory1 = QFileDialog.getExistingDirectory(self,
                                                          "选取源数据文件夹",
                                                          "./")  # 起始路径
            if directory1:
                self.lineEdit.setText(directory1)
        elif index == 1:
            directory1 = QFileDialog.getExistingDirectory(self,
                                                          "选取定标结果文件夹",
                                                          "./")  # 起始路径
            if directory1:
                self.lineEdit_2.setText(directory1)
        elif index == 2:
            directory1 = QFileDialog.getExistingDirectory(self,
                                                          "选取定标结果文件夹",
                                                          "./")  # 起始路径
            if directory1:
                self.lineEdit_3.setText(directory1)
        elif index == 3:
            directory1 = QFileDialog.getExistingDirectory(self,
                                                          "选取质量合格文件夹",
                                                          "./")  # 起始路径
            if directory1:
                self.lineEdit_4.setText(directory1)
        elif index == 4:
            directory1 = QFileDialog.getExistingDirectory(self,
                                                          "选取质量不合格文件夹",
                                                          "./")  # 起始路径
            if directory1:
                self.lineEdit_5.setText(directory1)
        elif index == 5:
            directory1 = QFileDialog.getExistingDirectory(self,
                                                          "选取质量合格文件夹",
                                                          "./")  # 起始路径
            if directory1:
                self.lineEdit_6.setText(directory1)
        elif index == 6:
            if self.radioButton.isChecked():
                directory1 = QFileDialog.getExistingDirectory(self,
                                                              "选取sFLD结果文件夹",
                                                              "./")  # 起始路径
                if directory1:
                    self.lineEdit_7.setText(directory1)
            elif self.radioButton_2.isChecked():
                directory1 = QFileDialog.getExistingDirectory(self,
                                                              "选取3FLD结果文件夹",
                                                              "./")  # 起始路径
                if directory1:
                    self.lineEdit_7.setText(directory1)
            elif self.radioButton_3.isChecked():
                directory1 = QFileDialog.getExistingDirectory(self,
                                                              "选取iFLD结果文件夹",
                                                              "./")  # 起始路径
                if directory1:
                    self.lineEdit_7.setText(directory1)
            elif self.radioButton_4.isChecked():
                directory1 = QFileDialog.getExistingDirectory(self,
                                                              "选取F-SFM结果文件夹",
                                                              "./")  # 起始路径
                if directory1:
                    self.lineEdit_7.setText(directory1)
            elif self.radioButton_5.isChecked():
                directory1 = QFileDialog.getExistingDirectory(self,
                                                              "选取SVD结果文件夹",
                                                              "./")  # 起始路径
                if directory1:
                    self.lineEdit_7.setText(directory1)
            elif self.radioButton_6.isChecked():
                directory1 = QFileDialog.getExistingDirectory(self,
                                                              "选取BSF结果文件夹",
                                                              "./")  # 起始路径
                if directory1:
                    self.lineEdit_7.setText(directory1)

    def pretreatment(self):
        # 输入输出路径
        path = self.lineEdit.text()  # 输入文件夹
        pathout = self.lineEdit_2.text()  # 输出文件夹
        pathdb1 = self.pathdb1
        pathdb2 = self.pathdb2
        pathwl = self.pathwl

        if path and pathout:
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self._thread = mythread(0, [path, pathout, pathdb1, pathdb2, pathwl])
            self._thread.d.connect(self.refrsh)
            self._thread.start()
            self.pushButton_2.setText('正在处理...')
        else:
            QMessageBox.warning(self, "警告", "存在未选择路径", QMessageBox.Yes)

    def refrsh(self, index):
        # 更新按钮状态
        if index == 0:
            QMessageBox.information(self, "提示", '辐射定标完成', QMessageBox.Yes)
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_2.setText('辐射定标')

        elif index == 1:
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_8.setEnabled(True)
            QMessageBox.information(self, "提示", '质量控制完成', QMessageBox.Yes)
            self.pushButton_6.setText('质量控制')

        elif index == 2:
            self.comboBox.clear()
            self.comboBox.addItems(os.listdir(self.pathout))
            self.pushButton_9.setEnabled(True)
            self.pushButton_10.setEnabled(True)
            self.pushButton_7.setEnabled(True)
            QMessageBox.information(self, "提示", '算法处理完成', QMessageBox.Yes)
            self.pushButton_7.setText('计算')

    def qualityControl(self):
        # 读辐射定标后的文件
        path = self.lineEdit_3.text()  # 输入文件夹
        pathout = self.lineEdit_4.text()  # 输出符合质量的文件
        pathout2 = self.lineEdit_5.text()  # 输出不符合质量的文件
        if path and pathout and pathout2:

            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_8.setEnabled(False)
            self._thread = mythread(1, [path, pathout, pathout2, self.paramQual])
            self._thread.d.connect(self.refrsh)
            self._thread.start()
            self.pushButton_6.setText('正在处理...')

        else:
            QMessageBox.warning(self, "警告", "存在未选择路径", QMessageBox.Yes)


if __name__ == "__main__":

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # 创建QApplication 固定写法
    app = QApplication(sys.argv)
    # 实例化界面
    window = MainWindow()

    # # 使用QSS样式表
    with open('res/style.qss', encoding='utf-8') as f:
        qss = f.read()
        window.setStyleSheet(qss)

    # 显示界面
    window.show()
    # 阻塞，固定写法
    sys.exit(app.exec_())
