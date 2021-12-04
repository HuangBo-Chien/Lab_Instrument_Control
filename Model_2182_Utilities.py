'''
Before using program to control model 2182, please make sure it has been correctly connected to the computer via GPIB by clicking "scan for instrument" button on NIMAX
'''
import pyvisa as pv
import time

rm = pv.ResourceManager()

class Model_2182:

    def __init__(self, GPIB_Addr:str) -> None:
        self.Addr = GPIB_Addr
        self.Identity = rm.open_resource(GPIB_Addr)
    
    def Reset(self) -> None:
        self.Identity.write("*RST")
    
    def Select_Volt_Range(self, Range:float = 10) -> None:
        '''
        On the front panel, 100V, 10V, 1V, 0.1V, 0.01V can be chosen
        '''
        if Range < 0:
            Range = 0
        elif Range > 120:
            Range = 120
        self.Identity.write(f":SENS:RANG {Range}")
    
    def Display(self, Enable:bool = True) -> None:
        if Enable:
            self.Identity.write(":DISP:ENAB ON")
        else:
            self.Identity.write(":DISP:ENAB OFF")
    
    def Sense_Volt(self, Avg_times:int =  1) -> float:
        if Avg_times < 1:
            Avg_times = 1
        val = 0
        for _ in range(Avg_times):
            val += self.Identity.query(":SENS:DATA")
            time.sleep(0.1) # sleep for 100 ms
        val /= Avg_times
        return val
    
    def Select_PLC(self, PLC:float = 1) -> None:
        '''
        In Taiwan, our electricity is 60 Hz
        PLC 1~2 is recommended
        '''
        if PLC < 0.01:
            PLC = 0.01
        elif PLC > 60:
            PLC = 60
        self.Identity.write(f":SENS:NPLC {PLC}")
    
    def Filter_Setting(self, Enable:bool = True, Type:int = 0, Count:int = 10, Window:float = 0.01) -> None:
        if Enable:
            self.Identity.write(f":SENS:WIND {Window}")
            if Type == 0:
                self.Identity.write(":SENS:TCON MOV") # Moving window
            else:
                self.Identity.write(":SENS:TCON REP") # Repeating window
            if Count < 1:
                Count = 1
            elif Count > 100:
                Count = 100
            self.Identity.write(f":SENS:COUN {Count}")
            self.Identity.write(":SENS:DFIL ON")
        else:
            self.Identity.write(":SENS:DFIL OFF")
        
if __name__ == "__main__":
    my_Model_2182 = Model_2182("GPIB0::7::INSTR")

    
