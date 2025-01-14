import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


# 展示结果窗口类
class MyFigure(FigureCanvas):
    def __init__(self, width=4, height=10, dpi=100):
        self.fig = Figure(tight_layout=True, figsize=(width, height), dpi=dpi)
        super(MyFigure, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_alpha(1)
        self.axes.set(facecolor="none")
        #
        self.axes.set_facecolor((248 / 255, 252 / 255, 255 / 255))

        self.axes.grid()
        # 鼠标左键拖拽事件
        self.lastx = 0  # 获取鼠标按下时的坐标X
        self.lasty = 0  # 获取鼠标按下时的坐标Y
        self.press = False

        self.fig.canvas.mpl_connect("button_press_event", self.on_press)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_move)
        # 鼠标滚轮事件
        self.fig.canvas.mpl_connect('scroll_event', self.call_back)

    # ================ 鼠标左键拖拽坐标 ================ #
    def on_press(self, event):
        if event.inaxes:  # 判断鼠标是否在axes内
            if event.button == 1:  # 判断按下的是否为鼠标左键1（右键是3）
                self.press = True
                self.lastx = event.xdata  # 获取鼠标按下时的坐标X
                self.lasty = event.ydata  # 获取鼠标按下时的坐标Y

    def on_move(self, event):
        axtemp = event.inaxes
        if axtemp:
            if self.press:  # 按下状态
                # 计算新的坐标原点并移动
                # 获取当前最新鼠标坐标与按下时坐标的差值
                x = event.xdata - self.lastx
                y = event.ydata - self.lasty
                # 获取当前原点和最大点的4个位置
                x_min, x_max = axtemp.get_xlim()
                y_min, y_max = axtemp.get_ylim()

                x_min = x_min - x
                x_max = x_max - x
                y_min = y_min - y
                y_max = y_max - y

                axtemp.set_xlim(x_min, x_max)
                axtemp.set_ylim(y_min, y_max)
                self.figure.canvas.draw()  # 绘图动作实时反映在图像上

    def on_release(self, event):
        if self.press:
            self.press = False  # 鼠标松开，结束移动

    # ================ 鼠标滚轮放大缩小坐标 ================ #
    def call_back(self, event):
        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        y_min, y_max = axtemp.get_ylim()
        xfanwei = (x_max - x_min) / 10
        yfanwei = (y_max - y_min) / 10
        if event.button == 'up':
            axtemp.set(xlim=(x_min + xfanwei, x_max - xfanwei))
            axtemp.set(ylim=(y_min + yfanwei, y_max - yfanwei))
        elif event.button == 'down':
            axtemp.set(xlim=(x_min - xfanwei, x_max + xfanwei))
            axtemp.set(ylim=(y_min - yfanwei, y_max + yfanwei))
        self.figure.canvas.draw_idle()  # 绘图动作实时反映在图像上
