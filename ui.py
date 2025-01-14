# 本程序控制ui界面的显示
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import sys, os


# UI窗口类
class Ui_MainWindow(object):

    def __init__(self):
        self.pathdb1 = 'Data/辐射定标文件/FSNISIF1.csv'
        self.pathdb2 = 'Data/辐射定标文件/FSNISIF2.csv'
        self.pathwl = 'Data/wl.csv'

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2000, 1000)
        self.showMaximized()
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        MainWindow.setFont(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget = QtWidgets.QWidget(self.centralwidget)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())

        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(self.widget)

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)

        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(80, 0))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMinimumSize(QtCore.QSize(80, 0))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)

        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setMinimumSize(QtCore.QSize(80, 0))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_3.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_5.addWidget(self.lineEdit_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_5.addWidget(self.pushButton_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setMinimumSize(QtCore.QSize(80, 0))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_4.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_6.addWidget(self.lineEdit_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_6.addWidget(self.pushButton_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setMinimumSize(QtCore.QSize(80, 0))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_5.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_7.addWidget(self.lineEdit_5)
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_7.addWidget(self.pushButton_8)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget_2)
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_2.addWidget(self.pushButton_6)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget)

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)

        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setMinimumSize(QtCore.QSize(80, 0))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_6.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.horizontalLayout_8.addWidget(self.lineEdit_6)
        self.pushButton_9 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_8.addWidget(self.pushButton_9)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setMinimumSize(QtCore.QSize(80, 0))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_9.addWidget(self.label_7)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_7.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_9.addWidget(self.lineEdit_7)
        self.pushButton_10 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_9.addWidget(self.pushButton_10)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radioButton)
        self.horizontalLayout_3.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_2.setObjectName("radioButton_2")
        self.buttonGroup.addButton(self.radioButton_2)
        self.horizontalLayout_3.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_3.setObjectName("radioButton_3")
        self.buttonGroup.addButton(self.radioButton_3)
        self.horizontalLayout_3.addWidget(self.radioButton_3)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_4.setChecked(False)
        self.radioButton_4.setObjectName("radioButton_4")
        self.buttonGroup.addButton(self.radioButton_4)
        self.horizontalLayout_11.addWidget(self.radioButton_4)
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_5.setObjectName("radioButton_5")
        self.buttonGroup.addButton(self.radioButton_5)
        self.horizontalLayout_11.addWidget(self.radioButton_5)
        self.radioButton_6 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_6.setObjectName("radioButton_6")
        self.buttonGroup.addButton(self.radioButton_6)
        self.horizontalLayout_11.addWidget(self.radioButton_6)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_11)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_3.addWidget(self.pushButton_7)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setMinimumSize(QtCore.QSize(80, 0))
        self.label_8.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_10.addWidget(self.label_8)
        self.comboBox = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_10.addWidget(self.comboBox)
        self.pushButton_11 = QtWidgets.QPushButton(self.groupBox_3)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_11.sizePolicy().hasHeightForWidth())

        self.pushButton_11.setSizePolicy(sizePolicy)
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout_10.addWidget(self.pushButton_11)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.horizontalLayout_4.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())

        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_4.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2000, 24))

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)

        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        # 打开当前文件夹
        self.action1_1 = QtWidgets.QAction(MainWindow)
        self.action1_1.setObjectName("action")
        self.action1_1.setText("打开当前文件夹")
        self.action1_1.triggered.connect(self.lookfolder)
        self.menu.addAction(self.action1_1)

        # 选择入射辐射定标文件
        self.action1_2 = QtWidgets.QAction(MainWindow)
        self.action1_2.setObjectName("action")
        self.action1_2.setText("选择入射辐射定标文件")
        self.action1_2.triggered.connect(self.setpathdb1)
        self.menu.addAction(self.action1_2)

        # 选择反射辐射定标文件
        self.action1_3 = QtWidgets.QAction(MainWindow)
        self.action1_3.setObjectName("action")
        self.action1_3.setText("选择反射辐射定标文件")
        self.action1_3.triggered.connect(self.setpathdb2)
        self.menu.addAction(self.action1_3)

        # 选择标准波长文件
        self.action1_4 = QtWidgets.QAction(MainWindow)
        self.action1_4.setObjectName("action")
        self.action1_4.setText("选择标准波长文件")
        self.action1_4.triggered.connect(self.setpathwl)
        self.menu.addAction(self.action1_4)

        # 查看使用说明
        self.action2_1 = QtWidgets.QAction(MainWindow)
        self.action2_1.setObjectName("action")
        self.action2_1.setText("使用说明")
        self.action2_1.triggered.connect(self.lookhelp)
        self.menu_2.addAction(self.action2_1)

        # 查看软件说明
        self.action3_1 = QtWidgets.QAction(MainWindow)
        self.action3_1.setObjectName("action")
        self.action3_1.setText("软件说明")
        self.action3_1.triggered.connect(self.looksoftware)
        self.menu_3.addAction(self.action3_1)

        # 查看团队
        self.action4_1 = QtWidgets.QAction(MainWindow)
        self.action4_1.setObjectName("action")
        self.action4_1.setText("团队")
        self.action4_1.triggered.connect(self.lookteam1)

        # 查看版权
        self.action4_2 = QtWidgets.QAction(MainWindow)
        self.action4_2.setObjectName("action")
        self.action4_2.setText("版权")
        self.action4_2.triggered.connect(self.lookteam2)

        self.menu_4.addAction(self.action4_1)
        self.menu_4.addAction(self.action4_2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SIF多算法反演集成软件V1.0"))
        self.setWindowIcon(QIcon('res/1.png'))  # 设置窗口图标
        self.groupBox.setTitle(_translate("MainWindow", "Step1:辐射定标"))
        self.label.setText(_translate("MainWindow", "源数据:"))
        self.pushButton.setText(_translate("MainWindow", "选择"))
        self.label_2.setText(_translate("MainWindow", "定标结果:"))
        self.pushButton_3.setText(_translate("MainWindow", "选择"))
        self.pushButton_2.setText(_translate("MainWindow", "辐射定标"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Step2：质量控制"))
        self.label_3.setText(_translate("MainWindow", "定标结果:"))
        self.pushButton_4.setText(_translate("MainWindow", "选择"))
        self.label_4.setText(_translate("MainWindow", "质量合格:"))
        self.pushButton_5.setText(_translate("MainWindow", "选择"))
        self.label_5.setText(_translate("MainWindow", "质量不合格:"))
        self.pushButton_8.setText(_translate("MainWindow", "选择"))
        self.pushButton_6.setText(_translate("MainWindow", "质量控制"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Step3：多算法反演和结果展示"))
        self.label_6.setText(_translate("MainWindow", "质量合格:"))
        self.pushButton_9.setText(_translate("MainWindow", "选择"))
        self.label_7.setText(_translate("MainWindow", "结果:"))
        self.pushButton_10.setText(_translate("MainWindow", "选择"))
        self.radioButton.setText(_translate("MainWindow", "sFLD"))
        self.radioButton_2.setText(_translate("MainWindow", "3FLD"))
        self.radioButton_3.setText(_translate("MainWindow", "iFLD"))
        self.radioButton_4.setText(_translate("MainWindow", "F-SFM"))
        self.radioButton_5.setText(_translate("MainWindow", "SVD"))
        self.radioButton_6.setText(_translate("MainWindow", "BSF"))
        self.pushButton_7.setText(_translate("MainWindow", "计算"))
        self.label_8.setText(_translate("MainWindow", "文件展示:"))
        self.pushButton_11.setText(_translate("MainWindow", "绘图"))

        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "帮助"))
        self.menu_3.setTitle(_translate("MainWindow", "关于"))
        self.menu_4.setTitle(_translate("MainWindow", "联系我们"))

    def closeEvent(self, event):  # 函数名固定不可变
        reply = QtWidgets.QMessageBox.question(self, u'警告', u'您确定要退出吗?', QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        # QtWidgets.QMessageBox.question(self,u'弹窗名',u'弹窗内容',选项1,选项2)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()  # 关闭窗口
        else:
            event.ignore()  # 忽视点击X事件

    def lookfolder(self):
        # 打开当前程序所在文件夹
        os.system('explorer.exe %s' % os.getcwd())

    def looksoftware(self):

        text = '本软件为SIF多算法反演集成软件V1.0，于2024年2月2日发布。'
        QMessageBox.information(self, "软件说明", text, QMessageBox.Yes)

    def lookteam1(self):

        text = '本团队由陈敬华老师指导。\n团队联系方式：chenjh.14b@igsnrr.ac.cn>'
        QMessageBox.information(self, "团队", text, QMessageBox.Yes)

    def lookteam2(self):

        text = '版权所属单位：中国科学院地理科学与资源研究所'
        QMessageBox.information(self, "版权", text, QMessageBox.Yes)

    def lookhelp(self):

        text = '1.首先进行辐射定标，选择源数据文件夹和定标结果的输出文件夹,点击”辐射定标“按钮，即可对文件夹下的所有日期的数据进行定标。\n' \
               '2.进行辐射定标后,即可进行第二步，也即质量控制。选择定标结果文件夹，以及质量合格文件和不合格文件存放的文件夹，同时可以选择质量' \
               '控制参数，包括最大DN值、最大反射率、辐照度变化率%、暗电流最大占比、最大太阳天顶角。\n' \
               '3.进行质量控制后，可以选择质量合格的文件进行SIF反演计算。这里提供了sFLD(即标准夫琅禾费暗线反演方法）、3FLD、iFLD、F-SFM、' \
               'SVD、BSF算法,选择不同算法时可以输入不同的参数进行调整。算法原理可参考软件说明文档。\n' \
               '4.算法反演完毕后，可以选择某一天的反演结果进行展示。\n' \
               '5.可在上方菜单栏中选择入射辐射定标文件、反射辐射定标文件、标准波长文件。若没有选择，则使用默认定标文件。'

        QMessageBox.information(self, "说明文档", text, QMessageBox.Yes)

    def setpathdb1(self):

        directory1, _ = QFileDialog.getOpenFileName(self, "选择辐射定标文件", "", "CSV Files (*.csv)")

        if directory1:
            self.pathdb1 = directory1
            text = '入射辐射定标文件为：' + directory1
            QMessageBox.information(self, "辐射定标", text, QMessageBox.Yes)

    def setpathdb2(self):

        directory1, _ = QFileDialog.getOpenFileName(self, "选择辐射定标文件", "", "CSV Files (*.csv)")

        if directory1:
            self.pathdb2 = directory1
            text = '反射辐射定标文件为：' + directory1
            QMessageBox.information(self, "辐射定标", text, QMessageBox.Yes)

    def setpathwl(self):

        directory1, _ = QFileDialog.getOpenFileName(self, "选择标准波长文件", "", "CSV Files (*.csv)")

        if directory1:
            self.pathwl = directory1
            text = '标准波长文件为：' + directory1
            QMessageBox.information(self, "标准波长", text, QMessageBox.Yes)
