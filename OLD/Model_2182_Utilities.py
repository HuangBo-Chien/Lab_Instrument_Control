'''
Before using program to control model 2182, please make sure it has been correctly connected to the computer via GPIB by clicking "scan for instrument" button on NIMAX
'''
import pyvisa as pv
import time

rm = pv.ResourceManager()

class Model_2182:

    def __init__(self, GPIB_Addr:str) -> None:
        self.Addr = GPIB_Addr
        self.Instr = rm.open_resource(GPIB_Addr)
    
    def Reset(self) -> None:
        '''
        Reset Model 2182 to its default settings
        '''
        self.Instr.write("*RST")
    
    def Select_Volt_Range(self, Range:float = 10) -> None:
        '''
        Set voltage range for measurement
        On the front panel, 100V, 10V, 1V, 0.1V, 0.01V can be chosen
        '''
        if Range < 0:
            Range = 0
        elif Range > 120:
            Range = 120
        self.Instr.write(f":SENS:RANG {Range}")
    
    def Display(self, Enable:bool = True) -> None:
        '''
        Set the display on the front panel to be on/off.
        '''
        if Enable:
            self.Instr.write(":DISP:ENAB ON")
        else:
            self.Instr.write(":DISP:ENAB OFF")
    
    def Sense_Volt(self, Avg_times:int =  1) -> float:
        '''
        Retrieve data multiple times and take the average
        '''
        if Avg_times < 1:
            Avg_times = 1
        val = 0
        for _ in range(Avg_times):
            val += self.Instr.query(":SENS:DATA")
            time.sleep(0.1) # sleep for 100 ms
        val /= Avg_times
        return val
    
    def Select_PLC(self, PLC:float = 1) -> None:
        '''
        In Taiwan, our electricity is 60 Hz
        PLC 1 or 2 is recommended according to the manual
        '''
        if PLC < 0.01:
            PLC = 0.01
        elif PLC > 60:
            PLC = 60
        self.Instr.write(f":SENS:NPLC {PLC}")
    
    def Digital_Filter_Setting(self, Enable:bool = True, Type:int = 0, Count:int = 10, Window:float = 0.01) -> None:
        '''
        Digital filter
        Average readings
        The threshold is determined by the sense range.
        e.g.:
        0.01 % of 10 mV is 1 uV
        '''
        if Enable:
            self.Instr.write(f":SENS:WIND {Window}")
            if Type == 0:
                self.Instr.write(":SENS:TCON MOV") # Moving window
            else:
                self.Instr.write(":SENS:TCON REP") # Repeating window
            if Count < 1:
                Count = 1
            elif Count > 100:
                Count = 100
            self.Instr.write(f":SENS:COUN {Count}")
            self.Instr.write(":SENS:DFIL ON")
        else:
            self.Instr.write(":SENS:DFIL OFF")
    
    def Analog_Filter_Setting(self, Enable:bool = False):
        '''
        Analog Filter
        This filter could only be used when the sense range is 10 mV.
        And it would take additional 125 ms for the reading to settle.
        Therefore, the reading rate could be greatly reduced.
        See manual 3-8 ~ 3-10
        '''
        if Enable:
            self.Instr.write(f"SENS:LPAS ON")
        else:
            self.Instr.write(f"SENS:LPAS OFF")
        
if __name__ == "__main__":
    my_Model_2182 = Model_2182("GPIB0::7::INSTR")

    
