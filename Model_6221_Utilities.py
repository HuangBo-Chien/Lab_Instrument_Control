import pyvisa as pv
import time

rm = pv.ResourceManager()

class Model_6221:

    def __init__(self, GPIB_Addr:str) -> None:
        self.Addr = GPIB_Addr
        self.Identity = rm.open_resource(GPIB_Addr)
    
    def Reset(self) -> None:
        self.Identity.write("*RST")
    
    def Check_2182_Connection(self, Mode:str) -> bool:
        '''
        Mode can only be DEL, PDEL, DCON
        '''
        Modes = ("DEL", "PDEL", "DCON")
        if Mode in Modes:
            self.Identity.query(f":SOUR:{Mode}:NVPR?")
        else:
            return False

    def PulseDelta_Setting_and_Arm(self, I_high:float, I_low:float, Width:float, Src_delay:float, CountNum:str = "INF", SrcRng:str = "Best", Interval:int = 5, Sweep:bool = False, Low_Meas:int = 2) -> None:
        '''
        Pulse Delta Mode
        '''
        if self.Check_2182_Connection("PulseDelta"):
            if -105e-3 <= I_high <= 105e-3:
                self.Identity.write(f":SOUR:PDEL:HIGH {I_high}")
            if -105e-3 <= I_low <= 105e-3:
                self.Identity.write(f":SOUR:PDEL:LOW {I_low}")
            if 50e-6 <= Width <= 12e-3:
                self.Identity.write(f":SOUR:PDEL:WIDT {Width}")
            if 16e-6 <= Src_delay <= 11.966e-3:
                self.Identity.write(f":SOUR:PDEL:SDEL {Src_delay}")
            if (CountNum.isnumeric() and 1 <= int(CountNum) <= 65636) or CountNum == "INF":
                self.Identity.write(f":SOUR:PDEL:COUN {CountNum}")
            if SrcRng in ("BEST", "FIX"):
                self.Identity.write(f":SOUR:PDEL:RANG {SrcRng}")
            if 5 <= Interval <= 999999:
                self.Identity.write(f":SOUR:PDEL:INT {Interval}")
            self.Identity.write(f":SOUR:PDEL:SWE {Sweep}")
            if Sweep:
                self.Identity(f"SOUR:SWE:")
            if Low_Meas in (1, 2):
                self.Identity.write(f":SOUR:PDEL:LME {Low_Meas}")
        else:
            pass
            # raise DevConnectionError(Devname = "Model 2182")

if __name__ == "__main__":
    my_Model_6221 = Model_6221