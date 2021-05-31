from ctypes import *

class Andor_Spectrometer:

    def __init__(self):
        self.path = r"C:\Users\admin\AppData\Local\Programs\Python\Python38\Lib\site-packages\pylablib\aux_libs\devices\libs\x64\\"
        self.atmcd64d = cdll.LoadLibrary(self.path + "atmcd64d.dll")
        self.atshamrock = cdll.LoadLibrary(self.path + "atshamrock.dll")
        self.ShamrockCIF = cdll.LoadLibrary(self.path + "ShamrockCIF.dll")
        self.ATSHAMROCKCS = cdll.LoadLibrary(self.path + "ATSHAMROCKCS.dll")
        
        self._DRV_SUCC()
        self.DEV_Info()
        self.read_set()

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

    def read_set(self):
    
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

##        print("0 False / 1 True = %d\n"\
##          "Turret = %d\n"\
##          "No Gratings = %d\n"\
##          "Grating = %d\n"\
##          "Detector Offset = %d\n"\
##          "Grating Offset = %d\n"\
##          "lines/mm = %f\n"\
##          "blaze = %s\n"\
##          "home = %d\n"\
##          "offset = %d\n"\
##          %(self.GP.value, self.Turret.value, self.NG.value, self.G.value, self.DO.value,
##            self.GO.value, self.lines.value, self.blaze.value, self.home.value, self.offset.value)
##        )
          
    def setT(self, temp):
        status = self.atmcd64d.CoolerON()
        if status == 20075:
            return "CoolerOn Problem"
##            print("It's cooler problem")
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
        
if __name__ == "__main__":
    import time
    SR303i = Andor_Spectrometer()
    SR303i.setT(-20)
    while True:
        s, t = SR303i.readT()
        print("Temp = %d" %(t))
        if s == 20036:
            print("Temp is stable")
            break
        time.sleep(1)
