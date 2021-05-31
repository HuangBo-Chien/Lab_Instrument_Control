from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from utils import *
import time

class Cooler(QtCore.QThread):

    finish = QtCore.pyqtSignal() # 判斷這個thread結束沒
    temp = QtCore.pyqtSignal(object, object, str) # 傳輸溫度資料
    msg = QtCore.pyqtSignal(str) # 傳訊息
    
    def __init__(self, dev):

        super(Cooler, self).__init__()
        self.temp = 100
        self.dev = dev

    def run(self):
##        print("Coolr start working.\nTemperature Setpoint = %f." %(self.temp))
        self.msg.emit("Cooler start cooling.\nTemperature Setpoint = " + str(self.temp) + " C\n")
        '''
        把cooling的事情寫在這
        '''
        self.dev.setT(self.temp)
        status = 0
        while status != 20036:
            status, temp = self.dev.readT()
            self.msg.emit("Current Temp is " + str(temp) + "\n")
            time.sleep(1)
        self.msg.emit("Temperature is stable.")
        self.finish.emit() # 最後發送finish的訊號

class TakeSignal(QtCore.QThread):

    finish = QtCore.pyqtSignal() # 判斷這個thread結束沒

    def __init__(self):

        super(TakeSignal, self).__init__()

    def run(self):
        print("Taking Signal")
        '''
        取資料
        '''
        self.finish.emit() # 最後發送finish的訊號

class TakeBG(QtCore.QThread):

    finish = QtCore.pyqtSignal() # 判斷這個thread結束沒

    def __init__(self):

        super(TakeBG, self).__init__()

    def run(self):
        print("Taking Background")
        '''
        取背景
        '''
        self.finish.emit() # 最後發送finish的訊號

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("GUI")
        MainWindow.setWindowTitle("SR303i")
        MainWindow.setGeometry(400, 400, 800, 600) # 視窗大小800 X 600，視窗左上角在(400, 400)的位置

        self.SR303i = Andor_Spectrometer()

        self.cooler = Cooler(self.SR303i)

        self.tab = QtWidgets.QTabWidget(MainWindow)
        self.tab.resize(300, 300)
        self.tab.move(300, 50)
        self._TG_set()

        self.log = QtWidgets.QPlainTextEdit(MainWindow) # 秀出儀器記錄
        self.log.move(50, 300)
        self.log.resize(400, 200)

        '''輸出訊息'''
        self.cooler.msg.connect(self.show_msg)

        self.test = QtWidgets.QGroupBox()
        self.test.setTitle("aaaa")
        self.tab.addTab(self.test, "Test1")
        self.test2 = QtWidgets.QGroupBox()
        self.test2.setTitle("bbbb")
        self.tab.addTab(self.test2, "Test2")
        
        

    def _TG_set(self):
        '''Temp Group'''
        self.Temp_Group = QtWidgets.QGroupBox(MainWindow)
        self.Temp_Group.move(50, 50)
        self.Temp_Group.setTitle("Tempeerature Setting")
        self.settemp_lab = QtWidgets.QLabel(self.Temp_Group) # set temp標語
        self.settemp_lab.setText("Set Temperature (C)")
        self.settemp_lab.adjustSize()
        self.settemp_lab.move(90, 50)
        self.inputtemp = QtWidgets.QSlider(self.Temp_Group)
        self.inputtemp.move(50, 50)
        self.inputtemp.setMaximum(0) # 最高0度 (沒啥理由)
        self.inputtemp.setMinimum(-55) # 最低-55度 (spec說-100度)
        self.inputtemp.setSingleStep(1) # 溫度step 1度
        self.inputtemp.setValue(-40) # 預設-40度
        self.inputtemp.setTickInterval(5)
        self.inputtemp.setTickPosition(QtWidgets.QSlider.TicksRight)
        self.inputtemp.valueChanged.connect(self._showtemp)
        self.showtemp = QtWidgets.QLineEdit(self.Temp_Group)
        self.showtemp.move(90, 90)
        self.showtemp.setText("-40")
        self.showtemp.resize(30, 20)
        self.settempbutton = QtWidgets.QPushButton(self.Temp_Group)
        self.settempbutton.move(150, 90)
        self.settempbutton.resize(50, 20)
        self.settempbutton.setText("Set")
        self.settempbutton.clicked.connect(self._cooler_start)
        self.Temp_Group.adjustSize() # GroupBox自動調整大小

    def _showtemp(self):
        self.showtemp.setText(str(self.inputtemp.value()))

    def _cooler_start(self):        
        self.cooler.temp = self.inputtemp.value()
        self.cooler.start()

    def show_msg(self, msg):
##        print("msg = %s" %(msg))
        self.log.insertPlainText(msg)

        
        
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
