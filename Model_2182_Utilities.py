import pyvisa as pv
from time import sleep

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
        Set voltage range for measurement.

        Parameters
        ===========
            Range can be one of the values in (100, 10, 1, 0.1, 0.01). and the unit is Volt.
        '''
        if Range < 0:
            Range = 0
        elif Range > 120:
            Range = 120
        self.Instr.write(f":VOLT:RANG {Range}")
    
    def Display(self, Enable:bool = True) -> None:
        '''
        Set the display on the front panel to be on/off.

        Parameter
        ========
            Enable == True/False ---> Display on/off
        '''
        if Enable:
            self.Instr.write(":DISP:ENAB ON")
        else:
            self.Instr.write(":DISP:ENAB OFF")
    
    def Sense_Volt(self, Avg_times:int =  1) -> float:
        '''
        Retrieve data multiple times and take the average.

        Parameter
        ========
        Avg_times can be any positive integers.
        
        Between two consecutive measurements, this program sleeps for 0.1 sec.
        '''
        if Avg_times < 1:
            Avg_times = 1
        val = 0
        for _ in range(Avg_times):
            val += float(self.Instr.query(":SENS:DATA?"))
            sleep(0.1) # sleep for 100 ms
        val /= Avg_times
        return val
    
    def Select_PLC(self, PLC:float = 1) -> None:
        '''
        Select power line cycle (PLC).

        Parameter
        ========
            PLC can be any decimal numbers from 0.01 to 120.

        Notes
        =====
            Note that, in Taiwan, our ac electricity freq is 60 Hz, which implies 1 PLC = 1 / 60 sec ~ 0.0167 sec.
            
            It would be better to set PLC to 1 or 2 for the instrument to suppress noises from power line efficiently without waiting too much time.

            For example, if PLC has been set to 1, then it would take 0.0167 sec to determine a value.
        '''
        if PLC < 0.01:
            PLC = 0.01
        elif PLC > 60:
            PLC = 60
        self.Instr.write(f":VOLT:NPLC {PLC}")
    
    def Digital_Filter_Setting(self, Enable:bool = True, Type:int = 0, Count:int = 10, Window:float = 0.01) -> None:
        '''
        Use internal digital filter to average readings.

        Parameters
        ======
            Enable == True/False ---> Turn on/off the filter
            
            Type == 0/1 ---> Moving Average/Repeat Average

            Count can be any positive integer.

            Window can be one of the values in (10, 1, 0.1, 0.01), and the unit is %.

        Notes
        =====
            The window percentage means the percentage of the sense voltage range.
            
            For example, if the voltage range is 0.01 V, and the window is 0.01 %.

            Then the filter threshold is 0.01 V * 0.01 % = 1 uV. This value is the minimal sensitivity.
            
            Therefore, if your signal is less than 1 uV, the window might not be that helpful.
        '''
        if Enable:
            self.Instr.write(f":VOLT:DFIL:WIND {Window}")
            if Type == 0:
                self.Instr.write(":VOLT:DFIL:TCON MOV") # Moving window
            else:
                self.Instr.write(":VOLT:DFIL:TCON REP") # Repeating window
            if Count < 1:
                Count = 1
            elif Count > 100:
                Count = 100
            self.Instr.write(f":VOLT:DFIL:COUN {Count}")
            self.Instr.write(":VOLT:DFIL ON")
        else:
            self.Instr.write(":VOLT:DFIL OFF")
    
    def Analog_Filter_Setting(self, Enable:bool = False):
        '''
        Use internal analog filter to suppress noises.

        Parameter
        =====
            Enable == True/False ---> Turn on/off the filter.

        Notes
        =====
            This filter could only be appied when the sense range is 10 mV.

            And it would take additional 125 ms for the reading to settle.
            
            Therefore, the reading rate could be greatly reduced.
            
            For more details, see manual 3-8 ~ 3-10.

            My personaly experience is this filter is capable of dramatically filter out noises from the power noise of electromagnet.
        '''
        if Enable:
            self.Instr.write(f"VOLT:LPAS ON")
        else:
            self.Instr.write(f"VOLT:LPAS OFF")
        
if __name__ == "__main__":
    my_Model_2182 = Model_2182("GPIB0::7::INSTR")
    my_Model_2182.Select_Volt_Range(Range = 0.01)
    my_Model_2182.Select_PLC(PLC = 2)
    my_Model_2182.Digital_Filter_Setting(Count = 10)
    my_Model_2182.Analog_Filter_Setting(Enable = True)
    print(my_Model_2182.Sense_Volt())

    
