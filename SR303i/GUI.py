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
        while status != 20036: # Temp not stable yet
            status, temp = self.dev.readT()
            self.msg.emit("Current Temp is " + str(temp) + "\n")
            time.sleep(1)
        self.msg.emit("Temperature is stable.")
        self.finish.emit() # 最後發送finish的訊號

class Acq_Set(QtCore.QThread):

    finish = QtCore.pyqtSignal() # 判斷這個thread結束沒
    msg = QtCore.pyqtSignal(str) # 傳訊息

    def __init__(self, dev, acq_mode, read_mode, exp = 1, acq_cyc = 1, acc = 1, kin_cyc = 1, kin = 1):
        super(Acq_Set, self).__init__()
        self.dev = dev
        self.acq_mode = acq_mode
        self.read_mode = read_mode
        self.exp = exp
        self.acq_cyc = acq_cyc
        self.acc = acc
        self.kin_cyc = kin_cyc
        self.kin = kin

    def run(self):
        self.dev.Acq_Mode(self.acq_mode, self.exp, self.acc_cyc, self.acc, self.kin_cyc, self.kin)
        self.dev.Read_Mode(self.read_mode, 128, 20, 5)
        self.msg.emit("Setting Complete!")
        self.finish.emit()


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
        self.tab = QtWidgets.QTabWidget(MainWindow)
        self.tab.resize(600, 400)
        self.tab.move(100, 50)
        self.log = QtWidgets.QPlainTextEdit(MainWindow) # 秀出儀器記錄
        self.log.move(100, 450)
        self.log.resize(600, 100)

        self.SR303i = Andor_Spectrometer()

        '''其他thread'''
        self.cooler = Cooler(self.SR303i)
        self.acq = Acq_Set(self.SR303i)

        '''輸出訊息'''
        self.cooler.msg.connect(self.show_msg)
        self.acq.msg.connect(self.show_msg)
        
        '''分頁設置'''
        self._TG_set()
        self._SG_set()
        
        '''Tab Control'''
        self.tab.addTab(self.Temp_Group, "Temp Control")
        self.tab.addTab(self.Spec_Group, "Acquisition Setting")

    def _TG_set(self):
        '''Temp Group'''
        self.Temp_Group = QtWidgets.QGroupBox()
##        self.Temp_Group.move(50, 50)
##        self.Temp_Group.setTitle("Temperature Setting")
        settemp_lab = QtWidgets.QLabel(self.Temp_Group) # set temp標語
        settemp_lab.setText("Set Temperature (C)")
        settemp_lab.adjustSize()
        settemp_lab.move(90, 50)
        inputtemp = QtWidgets.QSlider(self.Temp_Group)
        inputtemp.move(50, 50)
        inputtemp.setMaximum(0) # 最高0度 (沒啥理由)
        inputtemp.setMinimum(-55) # 最低-55度 (spec說-100度)
        inputtemp.setSingleStep(1) # 溫度step 1度
        inputtemp.setValue(-40) # 預設-40度
        inputtemp.setTickInterval(5)
        inputtemp.setTickPosition(QtWidgets.QSlider.TicksRight)
        inputtemp.valueChanged.connect(self._showtemp)
        showtemp = QtWidgets.QLineEdit(self.Temp_Group)
        showtemp.move(90, 90)
        showtemp.setText("-40")
        showtemp.resize(30, 20)
        settempbutton = QtWidgets.QPushButton(self.Temp_Group)
        settempbutton.move(150, 90)
        settempbutton.resize(50, 20)
        settempbutton.setText("Set")
        settempbutton.clicked.connect(self._cooler_start)
        self.Temp_Group.adjustSize() # GroupBox自動調整大小

    def _SG_set(self):
        self.Spec_Group = QtWidgets.QGroupBox()
##        self.test2.setTitle("bbbb")
        AM = QtWidgets.QComboBox(self.Spec_Group)
        AM_item = ["Single", "Accumulate", "Kinetic"]
        AM.addItems(AM_item)
        AM.move(30, 30)

        AMLab = QtWidgets.QLabel(self.Spec_Group)
        AMLab.setText("Acquisition Mode")
        AMLab.move(30, 10)

        RM = QtWidgets.QComboBox(self.Spec_Group)
        RM_item = ["FVB", "MT Track", "Image"]
        RM.addItems(RM_item)
        RM.move(120, 30)

        RMLab = QtWidgets.QLabel(self.Spec_Group)
        RMLab.setText("Read Mode")
        RMLab.move(120, 10)

        setacqbutton = QtWidgets.QPushButton(self.Spec_Group)
        setacqbutton.move(300, 30)
        setacqbutton.resize(50, 20)
        setacqbutton.setText("Select")

        Exp = QtWidgets.QLineEdit(self.Spec_Group)
        Exp.move(30, 130)
        Exp.setText("1")
        Exp.resize(100, 20)

        ExpLab = QtWidgets.QLabel(self.Spec_Group)
        ExpLab.setText("Exposure TIme (s)")
        ExpLab.move(30, 110)

        Acc_Cyc = QtWidgets.QLineEdit(self.Spec_Group)
        Acc_Cyc.move(30, 190)
        Acc_Cyc.setText("1")
        Acc_Cyc.resize(100, 20)

        Acc_CycLab = QtWidgets.QLabel(self.Spec_Group)
        Acc_CycLab.setText("Accumulatation Cycle")
        Acc_CycLab.move(30, 170)

        Acc = QtWidgets.QLineEdit(self.Spec_Group)
        Acc.move(30, 250)
        Acc.setText("1")
        Acc.resize(100, 20)

        AccLab = QtWidgets.QLabel(self.Spec_Group)
        AccLab.setText("Accumulatation Time (s)")
        AccLab.move(30, 230)

        Kin_Cyc = QtWidgets.QLineEdit(self.Spec_Group)
        Kin_Cyc.move(150, 190)
        Kin_Cyc.setText("1")
        Kin_Cyc.resize(100, 20)

        Kin_CycLab = QtWidgets.QLabel(self.Spec_Group)
        Kin_CycLab.setText("Kinetic Cycle")
        Kin_CycLab.move(150, 170)

        Kin = QtWidgets.QLineEdit(self.Spec_Group)
        Kin.move(150, 250)
        Kin.setText("1")
        Kin.resize(100, 20)

        KinLab = QtWidgets.QLabel(self.Spec_Group)
        KinLab.setText("Kinetic Time (s)")
        KinLab.move(150, 230)

        OK_button = QtWidgets.QPushButton(self.Spec_Group)
        OK_button.move(30, 300)
        OK_button.resize(50, 20)
        OK_button.setText("Set")

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
