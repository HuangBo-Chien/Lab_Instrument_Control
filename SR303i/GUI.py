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
        self.msg.emit("Temperature is stable.\n")
        self.finish.emit() # 最後發送finish的訊號

class Acq_Set(QtCore.QThread):

    finish = QtCore.pyqtSignal() # 判斷這個thread結束沒
    msg = QtCore.pyqtSignal(str) # 傳訊息

    def __init__(self, dev, acq_mode = 1, read_mode = 1, exp = 1, acq_cyc = 1, acc = 1, kin_cyc = 1, kin = 1):
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
        print("Start Running")
        self.dev.Acq_Mode(Mode = self.acq_mode, Exp_Time = self.exp, ACyc_Num = self.acq_cyc, ACyc_Time = self.acc, KCyc_Num = self.kin_cyc, KCyc_Time = self.kin)
        self.msg.emit("Acquisition Mode Setting Complete!\n")
        print("Acquisition Mode Setting Complete!")
        self.dev.Read_Mode(Mode = self.read_mode, Cen_Row = 215, Height = 50, offset = 0)
        self.msg.emit("Read Mode Setting Complete!\n")
        print("Read Mode Setting Complete!")
        self.finish.emit()

class Grating_Set(QtCore.QThread):
    
    finish = QtCore.pyqtSignal() # 判斷這個thread結束沒
    msg = QtCore.pyqtSignal(str) # 傳訊息

    def __init__(self, dev, grating = 1):
        super(Grating_Set, self).__init__()
        self.dev = dev
        self.grating = grating # number of grating

    def run(self):
        #grating 設定
        self.dev.change_setting(code = 2, Turrent = 1, Grating = self.grating)
        self.msg.emit("Setting Complete!\n")
        self.finish.emit()

class Spectrum_Center_Set(QtCore.QThread):

    finish = QtCore.pyqtSignal() # 判斷這個thread結束沒
    msg = QtCore.pyqtSignal(str) # 傳訊息

    def __init__(self, dev, w_cen = 560):
        super(Spectrum_Center_Set, self).__init__()
        self.dev = dev
        self.w_cen = w_cen

    def run(self):
        self.msg.emit("Setting Complete!\n")
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

class Stage_Moving(QtCore.QThread):

    finish = QtCore.pyqtSignal() # 判斷這個thread結束沒
    msg = QtCore.pyqtSignal(str) # 傳訊息

    def __init__(self, dev_x, dev_y, dev_z, x = 0, y = 0, z = 0):

        super(Stage_Moving, self).__init__()
        self.dev_x = dev_x
        self.dev_y = dev_y
        self.dev_z = dev_z
        self.r = [x, y, z]

    def run(self):
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
        self.gs = Grating_Set(self.SR303i)
        self.sps = Spectrum_Center_Set(self.SR303i)

        '''輸出訊息'''
        self.cooler.msg.connect(self.show_msg)
        self.acq.msg.connect(self.show_msg)
        self.gs.msg.connect(self.show_msg)
        self.sps.msg.connect(self.show_msg)
        
        '''分頁設置'''
        self._TG_set()
        self._SG_set()
        self._HG_set()
        self._SGG_set()
        
        '''Tab Control'''
        self.tab.addTab(self.Temp_Group, "Temp Control")
        self.tab.addTab(self.Spec_Group, "Acquisition Setting")
        self.tab.addTab(self.HW_Group, "Hardware Setting")
        self.tab.addTab(self.Stage_Group, "Stage Setting")

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
        settempbutton.clicked.connect(lambda: self._cooler_start(inputtemp.value()))
        self.Temp_Group.adjustSize() # GroupBox自動調整大小

    def _SG_set(self):
        '''accumulation setting'''
        def acq_mode_select(self):
            if AM.currentText() == "Single":
                Acc.setEnabled(False)
                Acc_Cyc.setEnabled(False)
                Kin.setEnabled(False)
                Kin_Cyc.setEnabled(False)
            elif AM.currentText() == "Accumulate":
                Acc.setEnabled(True)
                Acc_Cyc.setEnabled(True)
                Kin.setEnabled(False)
                Kin_Cyc.setEnabled(False)
            elif AM.currentText() == "Kinetic":
                Acc.setEnabled(True)
                Acc_Cyc.setEnabled(True)
                Kin.setEnabled(True)
                Kin_Cyc.setEnabled(True)
        
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
        setacqbutton.clicked.connect(acq_mode_select)

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
        Acc_Cyc.setEnabled(False)

        Acc_CycLab = QtWidgets.QLabel(self.Spec_Group)
        Acc_CycLab.setText("Accumulatation Cycle")
        Acc_CycLab.move(30, 170)

        Acc = QtWidgets.QLineEdit(self.Spec_Group)
        Acc.move(30, 250)
        Acc.setText("1.01")
        Acc.resize(100, 20)
        Acc.setEnabled(False)

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
        Kin_Cyc.setEnabled(False)

        Kin = QtWidgets.QLineEdit(self.Spec_Group)
        Kin.move(150, 250)
        Kin.setText("1.01")
        Kin.resize(100, 20)
        Kin.setEnabled(False)

        KinLab = QtWidgets.QLabel(self.Spec_Group)
        KinLab.setText("Kinetic Time (s)")
        KinLab.move(150, 230)

        OK_button = QtWidgets.QPushButton(self.Spec_Group)
        OK_button.move(30, 300)
        OK_button.resize(50, 20)
        OK_button.setText("Set")   
        OK_button.clicked.connect(lambda: self.acq_change_set(AM.currentText(), Exp.text(), Acc_Cyc.text(), Acc.text(), Kin_Cyc.text(), Kin.text(), RM.currentText()))

    def _HG_set(self):

        self.HW_Group = QtWidgets.QGroupBox()

        Grating = QtWidgets.QComboBox(self.HW_Group)
        Grating_list = ["100/500", "300/500", "1200/500"]
        Grating.addItems(Grating_list)
        Grating.move(30, 30)

        GratingLab = QtWidgets.QLabel(self.HW_Group)
        GratingLab.move(30, 10)
        GratingLab.resize(50, 20)
        GratingLab.setText("Grating")

        SC = QtWidgets.QLineEdit(self.HW_Group)
        SC.move(130, 30)
        SC.resize(100, 20)
        SC.setText("1000")

        SCLab = QtWidgets.QLabel(self.HW_Group)
        SCLab.move(130, 10)
        SCLab.setText("Spectrum Center")

        Unit = QtWidgets.QComboBox(self.HW_Group)
        unit = ["nm", "cm-1"]
        Unit.addItems(unit)
        Unit.move(250, 30)

        UnitLab = QtWidgets.QLabel(self.HW_Group)
        UnitLab.move(250, 10)
        UnitLab.setText("Unit")

        OK_button = QtWidgets.QPushButton(self.HW_Group)
        OK_button.move(30, 300)
        OK_button.resize(50, 20)
        OK_button.setText("Set")   
        OK_button.clicked.connect(lambda: self.HW_set(Unit.currentText(), SC.text())) #[1, 2]

    def _SGG_set(self):
        self.Stage_Group = QtWidgets.QGroupBox()

    def _showtemp(self):
        self.showtemp.setText(str(self.inputtemp.value()))

    def _cooler_start(self, temp):        
        self.cooler.temp = int(temp) #self.inputtemp.value()
        self.cooler.start()

    def acq_change_set(self, AcqMode = "Single", Exp_Time = "1", ACyc_Num = "1", ACyc_Time = "1.01", KCyc_Num = "1", KCyc_Time = "1", ReadMode = "FVB"):
        if AcqMode == "Single":
            self.acq.acq_mode = 1
        elif AcqMode == "Accumulate":
            self.acq.acq_mode = 2
        elif AcqMode == "Kinetic":
            self.acq.acq_mode = 3
        print("Acq Mode = %d" %(self.acq.acq_mode))
        if ReadMode == "FVB":
            self.acq.read_mode = 0
        elif ReadMode == "MT Track":
            self.acq.read_mode = 1
        elif ReadMode == "Image":
            self.acq.read_mode = 4
        print("Read mode = %d" %(self.acq.read_mode))
        self.acq.exp = float(Exp_Time)
        self.acq.acq_cyc = int(ACyc_Num)
        self.acq.acc = float(ACyc_Time)
        self.acq.kin_cyc = int(KCyc_Num)
        self.acq.kin = float(KCyc_Time)
        self.acq.start()

    def HW_set(self, unit, val):
        if unit == "cm-1":
            shift = float(val)
            w0 = 532 # nm
            self.sps.w_cen = round(1 / (1 / w0 - shift * 1e-7), 2)
        else:
            self.sps.w_cen = round(float(val))
##        print(self.sps.w_cen)
        self.gs.start()
        self.gs.wait()
        self.sps.start()

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

'''
[1]: https://stackoverflow.com/questions/940555/pyqt-sending-parameter-to-slot-when-connecting-to-a-signal
[2]: https://eli.thegreenplace.net/2011/04/25/passing-extra-arguments-to-pyqt-slot
'''
