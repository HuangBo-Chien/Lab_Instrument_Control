import pyvisa as pv
import time
import numpy as np

rm = pv.ResourceManager()

class Model_6221:

    def __init__(self, GPIB_Addr:str) -> None:
        self.Addr = GPIB_Addr
        self.Identity = rm.open_resource(GPIB_Addr)
    
    def Reset(self) -> None:
        self.Identity.write("*RST")

    class Model_2182_Setting:

        def __init__(self, RNG:float = 0.1, NPLC:int = 1) -> None:
            self.RNG = RNG
            self.NPLC = NPLC

        def Check_Connection(self, Mode:str) -> bool:
            '''
            Mode can only be DEL, PDEL, DCON
            '''
            Modes = ("DEL", "PDEL", "DCON")
            if Mode in Modes:
                q = self.Identity.query(f":SOUR:{Mode}:NVPR?") # check if Model 2182 is correctly connected with Nodel 6221
                return (q == 1) # 1 = yes, 0 = no
            else:
                return False
        
        def Send_Command(self, Command:str) -> None:
            prefix = "SYST:COMM:SER "
            # self.

    class Pulsedelta:
        """
        Pulse Delta Mode
        Unit of params related to current are uA.
        Unit of delay time and pulse width are us.
        Unit of interval is power line cycle (PLC). e.g. 60Hz ---> 1 PLC = 1 / 60 s ~ 16.667 ms
        """
        def __init__(self, Sweep:bool = False) -> None:
            if Sweep:
                self.Sweep_Pulse()
            else:
                self.Fixed_Pulse()

        def Fixed_Pulse(self, I_high:np.float64 = np.float64(100.0), I_low:np.float64 = np.float64(100.0), Width:np.float64 = np.float64(100.0), Src_delay:np.float64 = np.float64(100), CountNum:str = "1", SrcRng:str = "Best", Interval:np.int64 = 5, Low_Meas:np.int64 = 2) -> None:
            self.I_high = np.around(I_high, decimals = 2)
            self.I_low = np.around(I_low, decimals = 2)
            self.Width = np.around(Width, decimals = 2)
            self.Src_delay = np.around(Src_delay, decimals = 2)
            self.CountNum = CountNum
            self.SrcRng = SrcRng
            self.Interval = Interval
            self.Low_Meas = Low_Meas
        
        def Sweep_Pulse(self) -> None:
            pass
        
        def Show_Setting(self):
            print(f"\
            ********** Pulse Delta Mode Setting **********\
            I high = {self.I_high} uA\n\
            I low = {self.I_low} uA\n\
            Pulse Width = {self.Width} us\n\
            Source Delay = {self.Src_delay} us\n\
            Number of pts to collect = {self.CountNum} \n\
            Source Range setting = {self.SrcRng} \n\
            Interval = {self.Interval} PLC \n\
            **********************************************")

    class Sweep:

        def __init__(self) -> None:
            pass
    
    class Delta:

        def __init__(self) -> None:
            pass

    class Diff_Cond:

        def __init__(self) -> None:
            pass
    

    # def PulseDelta_Setting(self, I_high:float, I_low:float, Width:float, Src_delay:float, CountNum:str = "INF", SrcRng:str = "Best", Interval:int = 5, Sweep:bool = False, Low_Meas:int = 2) -> None:
    #     '''
    #     Pulse Delta Mode
    #     '''
    #     if self.Check_2182_Connection("PulseDelta"):
    #         if -105e-3 <= I_high <= 105e-3:
    #             self.Identity.write(f":SOUR:PDEL:HIGH {I_high}")
    #         if -105e-3 <= I_low <= 105e-3:
    #             self.Identity.write(f":SOUR:PDEL:LOW {I_low}")
    #         if 50e-6 <= Width <= 12e-3:
    #             self.Identity.write(f":SOUR:PDEL:WIDT {Width}")
    #         if 16e-6 <= Src_delay <= 11.966e-3:
    #             self.Identity.write(f":SOUR:PDEL:SDEL {Src_delay}")
    #         if (CountNum.isnumeric() and 1 <= int(CountNum) <= 65636) or CountNum == "INF":
    #             self.Identity.write(f":SOUR:PDEL:COUN {CountNum}")
    #             self.Identity.write(f":TRAC:POIN {CountNum}") # the number of traced points == the number of count
    #         if SrcRng in ("BEST", "FIX"):
    #             self.Identity.write(f":SOUR:PDEL:RANG {SrcRng}")
    #         if 5 <= Interval <= 999999:
    #             self.Identity.write(f":SOUR:PDEL:INT {Interval}")
    #         self.Identity.write(f":SOUR:PDEL:SWE {Sweep}")
    #         if Low_Meas in (1, 2):
    #             self.Identity.write(f":SOUR:PDEL:LME {Low_Meas}")
    #     else:
    #         pass
    #         # raise DevConnectionError(Devname = "Model 2182")
    
    def Show_Setting(self, Mode:str) -> None:

        if Mode == "PulseDelta":
            pass

    def Communication_with_2182(self, RNG:float = 1, NPLC:int = 2):
        pass
    
    def PulseDelta_Measure(self) -> list:
        self.Identity.write(":SOUR:PDEL:ARM")
        self.Identity.write(":INIT:IMM") # start the measurement
        count_num = 0
        while True:
            event_response = self.Identity.query(":STAT:OPER:EVEN?")
            if (event_response & 1024) >> 10 and not (event_response & 64) >> 6:
                break
            if (event_response & 32) >> 5:
                count_num += 1
                print(count_num)
        self.Identity.write(":SOUR:SWE:ABOR")
        return self.Identity.query(":TRAC:DATA?")


if __name__ == "__main__":
    my_Model_6221 = Model_6221