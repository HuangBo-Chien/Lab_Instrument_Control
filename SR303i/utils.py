from ctypes import *
import numpy as np

class Andor_Spectrometer:

    def __init__(self):
        self.path = r"C:\Users\admin\AppData\Local\Programs\Python\Python38\Lib\site-packages\pylablib\aux_libs\devices\libs\x64\\"
        self.atmcd64d = cdll.LoadLibrary(self.path + "atmcd64d.dll")
        self.atshamrock = cdll.LoadLibrary(self.path + "atshamrock.dll")
        self.ShamrockCIF = cdll.LoadLibrary(self.path + "ShamrockCIF.dll")
        self.ATSHAMROCKCS = cdll.LoadLibrary(self.path + "ATSHAMROCKCS.dll")
        
        self._DRV_SUCC()
        self.DEV_Info()
        self.read_setting()

    def _DRV_SUCC(self):
    
        self.nod = c_int(100) # 先隨意初始化一個數字
    
        status = self.ShamrockCIF.ShamrockInitialize(self.path + "detector.ini")
        if status == 20202:
            self.ShamrockCIF.ShamrockGetNumberDevices.argtypes = [POINTER(c_int)] # 用傳參考的方式，傳一個整數
            self.ShamrockCIF.ShamrockGetNumberDevices.restype = c_uint # 回傳unsigned int
            status = self.ShamrockCIF.ShamrockGetNumberDevices(byref(self.nod)) # 把nod的addr傳到dll
            if status == 20202:
                return True
            else:
                print("GetNumberDevices Error!")
                return False
        else:
            print("DRV Error!")
            return False

    def DEV_Info(self):
    
        self.SN = create_string_buffer(64) # seriaal number，暫時給一個64bit的string buffer
        self.FL = c_float(0.0) # focal length
        self.AD = c_float(0.0) # Angular Deviation
        self.FT = c_float(0.0) #  
    
        self.ShamrockCIF.ShamrockGetSerialNumber.argtypes = [c_int, c_char_p] # 傳一個整數跟一個char *
        status = self.ShamrockCIF.ShamrockGetSerialNumber(0, self.SN)
        if status == 20202:
            self.ShamrockCIF.ShamrockEepromGetOpticalParams.argtypes = [c_int, POINTER(c_float), POINTER(c_float), POINTER(c_float)]
            status = self.ShamrockCIF.ShamrockEepromGetOpticalParams(0, byref(self.FL), byref(self.AD), byref(self.FT))
            if status == 20202:
                return True
            else:
##                print("EepromGetOpticalParams Error")
                return False
        else:
##            print("GetSerialNumber Error!")
            return False

    def read_setting(self):
    
        self.GP = c_int(100) # Grating Present
        self.Turret = c_int(5)
        self.NG = c_int(100) # No Grating
        self.G = c_int(100) # Grating
        self.DO = c_int(100) # Detector offset
        self.lines = c_float(0.0)
        self.blaze = create_string_buffer(64)
        self.home = c_int(100)
        self.offset = c_int(100)
        self.GO = c_int(100) # Grating offset
    
        self.ShamrockCIF.ShamrockGratingIsPresent.argtypes = [c_int, POINTER(c_int)]
        self.ShamrockCIF.ShamrockGetTurret.argtypes = [c_int, POINTER(c_int)]
        self.ShamrockCIF.ShamrockGetNumberGratings.argtypes = [c_int, POINTER(c_int)]
        self.ShamrockCIF.ShamrockGetGrating.argtypes = [c_int, POINTER(c_int)]
        self.ShamrockCIF.ShamrockGetDetectorOffset.argtypes = [c_int, POINTER(c_int)]
        self.ShamrockCIF.ShamrockGetGratingInfo.argtypes = [c_int, c_int, POINTER(c_float), c_char_p, POINTER(c_int), POINTER(c_int)]
        self.ShamrockCIF.ShamrockGetGratingOffset.argtypes = [c_int, c_int, POINTER(c_int)]

        self.ShamrockCIF.ShamrockGratingIsPresent(0, byref(self.GP))
        self.ShamrockCIF.ShamrockGetTurret(0, byref(self.Turret))
        self.ShamrockCIF.ShamrockGetNumberGratings(0, byref(self.NG))
        self.ShamrockCIF.ShamrockGetGrating(0, byref(self.G))
        self.ShamrockCIF.ShamrockGetDetectorOffset(0, byref(self.DO))
        self.ShamrockCIF.ShamrockGetGratingInfo(0, self.G, self.lines, self.blaze, byref(self.home), byref(self.offset))
        self.ShamrockCIF.ShamrockGetGratingOffset(0, self.G, byref(self.GO))

        print("0 False / 1 True = %d\n"\
          "Turret = %d\n"\
          "No Gratings = %d\n"\
          "Grating = %d\n"\
          "Detector Offset = %d\n"\
          "Grating Offset = %d\n"\
          "lines/mm = %f\n"\
          "blaze = %s\n"\
          "home = %d\n"\
          "offset = %d\n"\
          %(self.GP.value, self.Turret.value, self.NG.value, self.G.value, self.DO.value,
            self.GO.value, self.lines.value, self.blaze.value, self.home.value, self.offset.value)
        )
          
    def setT(self, temp):
        self.cooleron()
        c_temp = c_int(temp)
##        print("Temp setpoint is %d" %(temp))
        status = self.atmcd64d.SetTemperature(c_temp)
        if status == 20075:
            return "Set Temp Problem"
##            print("It's set temp problem")    
        
    
    def readT(self):
        current_temp = c_int(0)
        self.atmcd64d.GetTemperature.argtypes = [POINTER(c_int)]
        status = self.atmcd64d.GetTemperature(byref(current_temp)) # 如果status == 20036表示溫度穩定
        return status, current_temp.value

    def cooleron(self):
        status = self.atmcd64d.CoolerON()
        if status == 20075:
            return "CoolerOn Problem"
##            print("It's cooler problem")

    def cooleroff(self):
        status = self.atmcd64d.CoolerOFF()
        if status == 20075:
            return "CoolerOFF Problem"

    def camera_ini(self):
        path = r"C:\Users\admin\AppData\Local\Programs\Python\Python38\Lib\site-packages\pylablib\aux_libs\devices\libs\x64\\"
        s = c_wchar_p("")
        print(self.atmcd64d.Initialize(s))
        time.sleep(2)

    def ShutDown(self):
        self.atmcd64d.ShutDown()

    def Read_Mode(self, Mode = 0, Cen_Row = 128, Height = 20, Num_of_Row = 5, offset = 0, Pos = [None], hbin = 1, vbin = 1, hstart = 1, hend = 1024, vstart = 1, vend = 256):
        c_Mode = c_int(Mode)
        if Mode == 0: # FVB
            self.atmcd64d.SetReadMode(c_Mode)
        elif Mode == 1: # Multi Track
            self.atmcd64d.SetReadMode(c_Mode)
            c_NoR = c_int(Num_of_Row)
            c_Height = c_int(Height)
            c_offset = c_int(offset)
            c_bottom = c_int()
            c_gap = c_int()
            self.atmcd64d.SetMultiTrack(c_NoR, c_Height, c_offset, byref(c_bottom), byref(c_gap))
        elif Mode == 2: # Random Track
            self.atmcd64d.SetReadMode(c_Mode)
            c_NoR = c_int(Num_of_Row)
            c_pos = c_int(Pos) # May have bugs
            self.atmcd64d.SetRandomTracks(c_NoR, c_pos)
        elif Mode == 3: # Single Track
            self.atmcd64d.SetReadMode(c_Mode)
            c_Cen_Row = c_int(Cen_Row)
            c_Height = c_int(Height)
            self.atmcd64d.SetSingleTrack(c_Cen_Row, c_Height)
        elif Mode == 4: # Image
            self.atmcd64d.SetReadMode(c_Mode)
            c_hbin = c_int(hbin)
            c_vbin = c_int(vbin)
            c_hstart = c_int(hstart)
            c_hend = c_int(hend)
            c_vstart = c_int(vstart)
            c_vend = c_int(vend)
            self.atmcd64d.SetImage(c_hbin, c_vbin, c_hstart, c_hend, c_vstart, c_vend)
        elif Mode == 5: # Cropped
            'I will finish this part someday...'
            pass

    def Acq_Mode(self, Mode = 1, Exp_Time = 1, ACyc_Num = 1, ACyc_Time = 1, KCyc_Num = 1, KCyc_Time = 1):
        c_Mode = c_int(Mode)
        c_exp = c_float(Exp_Time)
        if Mode == 1: # Single
            self.atmcd64d.SetAcquisitionMode(c_Mode)
            self.atmcd64d.SetExposureTime(c_exp)
        elif Mode == 2: # Accumulate
            c_acycn = c_int(ACyc_Num)
            c_acyct = c_float(ACyc_Time)
            self.atmcd64d.SetAcquisitionMode(c_Mode)
            self.atmcd64d.SetExposureTime(c_exp)
            self.atmcd64d.SetNumberAccumulations(c_acycn)
            self.atmcd64d.SetAccumulationCycleTime(c_acyct) # Only works if user selects "Internal" trigger
        elif Mode == 3: # Kinetic Series
            c_acycn = c_int(ACyc_Num)
            c_acyct = c_float(ACyc_Time)
            c_kcycn = c_int(KCyc_Num)
            c_kcyct = c_float(KCyc_Time)
            self.atmcd64d.SetAcquisitionMode(c_Mode)
            self.atmcd64d.SetExposureTime(c_exp)
            self.atmcd64d.SetNumberAccumulations(c_acycn)
            self.atmcd64d.SetAccumulationCycleTime(c_acyct)
            self.atmcd64d.SetNumberKinetics(c_kcycn)
            self.atmcd64d.SetKineticycleTime(c_kcyct)
        elif Mode == 5: # Run Till Abort
            c_kcyct = c_float(0)
            self.atmcd64d.SetAcquisitionMode(c_Mode)
            self.atmcd64d.SetExposureTime(c_exp)
            self.atmcd64d.SetKineticycleTime(c_kcyct)

    def Tri_Mode(self, Mode):
        c_Mode = c_int(Mode)
        if Mode == 0: # Internal
            self.atmcd64d.SetTriggerMode(c_Mode)

    def Gate_Mode(self, Mode):
        c_Mode = c_int(Mode)
        if Mode == 1:
            self.atmcd64d.SetGateMode(c_Mode)

    def Acq_Start(self):
        self.atmcd64d.StartAcquisition()

    def Get_Status(self):
        '''
        status code
        20072 --> DRV_ACQUIRING
        20073 --> DRV_IDLE
        '''
        c_status = c_int()
        r = self.atmcd64d.GetStatus(byref(c_status))
        return r, c_status.value

    def Fetch_Data(self):
        x, y = self.Get_Det()
        
##        print("x = %d" %(x))
##        data = np.arange(0, x, 1)
##        dataPtr = data.ctypes.data_as(POINTER(c_int))
##        print(data)
        c_data_arr = (c_int * (5 * x))()
##        c_data_arr = c_int(0)
        c_size = c_ulong(5 * x) # not sure if this can still work in Image mode
##        self.atmcd64d.GetAcquiredData(byref(c_data_arr), c_size)
        self.atmcd64d.GetAcquiredData.argtypes = [POINTER(c_int), c_ulong]
##        print(len(data))
        status = self.atmcd64d.GetAcquiredData(c_data_arr, c_size)
        print("data status = ", status)
        return c_data_arr

    def Get_Det(self):
        x_pix = c_int()
        y_pix = c_int()
        self.atmcd64d.GetDetector(byref(x_pix), byref(y_pix))
        return x_pix.value, y_pix.value

    def change_setting(self, code = 0, Turrent = -1, Grating = -1, Det_off = 0, Gra_off = 0):
        c_dev_num = c_int(0)
        c_T = c_int(Turrent)
        c_G = c_int(Grating)
        c_DO = c_int(Det_off)
        c_GO = c_int(Gra_off)
        if code & 1 != 0:
            self.ShamrockCIF.ShamrockSetTurret(c_dev_num, c_T)
        elif code & 2 != 0
            self.ShamrockCIF.ShamrockSetGrating(c_dev_num, c_G)
        elif code & 4 != 0:
            self.ShamrockCIF.ShamrockWavelengthReset(c_dev_num)
        elif code & 8 != 0:
            self.ShamrockCIF.ShamrockSetDetectorOffset(c_dev_num, c_DO)
        elif code & 16 != 0:
            self.ShamrockCIF.ShamrockSetGratingOffset(c_dev_num, c_GO)
        
if __name__ == "__main__":
    import time
    import matplotlib.pyplot as plt
    SR303i = Andor_Spectrometer()

    try:
        SR303i.setT(-40)
        while True:
            s, t = SR303i.readT()
            print("Temp = %d" %(t))
            if s == 20036:
                print("Temp is stable")
                break
            time.sleep(1)
        SR303i.camera_ini()
        SR303i.Acq_Mode(Mode = 1, Exp_Time = 1)
        SR303i.Read_Mode(Mode = 1, Cen_Row = 215, Height = 50, offset = 0)
        SR303i.Gate_Mode(Mode = 1)
        SR303i.Tri_Mode(Mode = 0)
        SR303i.Acq_Start()
        while True:
            r, status = SR303i.Get_Status()
            print("status = %d" %(status))
            print("r = %d" %(r))
            if status != 20072:
                break
            else:
                time.sleep(1)
##        for i in range(1600*400):
##            ss = SR303i.Fetch_Data(i)
##            if ss != 20067:
##                print("i = ", i)
##                break
        data = SR303i.Fetch_Data()
        plt.plot(data)
##        print(data[0])
##        for i in range(len(data)):
##            print("%d data is %d" %(i, data[i]))
        print("Finished")
        SR303i.cooleroff()
        SR303i.ShutDown()
    except:
        SR303i.cooleroff()
        SR303i.ShutDown()
    plt.show()
    

    
