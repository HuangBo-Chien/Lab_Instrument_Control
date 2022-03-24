import pyvisa as pv
from time import sleep

rm = pv.ResourceManager()

class Model_475:

    def __init__(self, GPIB_Addr:str) -> None:
        
        self.GPIB_Addr = GPIB_Addr
        self.Instr = rm.open_resource(GPIB_Addr)
    
    def Reset(self) -> None:

        self.Instr.write("*RST")
    
    def Set_Unit(self, Mode:int) -> None:
        '''
        Set the unit of magnetic field

        Parameter
        =========
            Mode == 1 ---> G

            Mode == 2 ---> T
            
            Mode == 3 ---> Oe
            
            Mode == 4 ---> A/m
        
        Notes
        =====
            Depending on the value, the unit could have an additional kilo- prefix. i.e. Oe becomes kOe
        '''
        if 1 <= Mode <= 4:
            self.Instr.write(f"UNIT {Mode}")
    
    def Set_Range(self, Mode:int) -> None:
        '''
        Set the range of measurement

        Parameter
        ==========
            Mode can be 1 ~ 5 (from lowest to highest)

        Notes
        ========
            The range is probe dependent. Please check the actual range manually.
        '''
        if 1 <= Mode <= 5:
            self.Instr.write(f"RANGE {Mode}")
    
    def Check_Range(self) -> int:
        '''
        Check the current measurement range
        '''
        return int(self.Instr.query("RANGE?"))
    
    def Read_Field(self) -> float:
        '''
        Measure the mag field
        '''
        val = float(self.Instr.query("RDGFIELD?"))
        return val
    
    def Measurement_Setting(self, Mode:int, Resolution:int = 1, RMS_Filter_mode:int = 1, Peak_Mode:int = 1, Peak_Display:int = 1) -> None:
        '''
        Set measurement mode

        Parameters
        ========
            Mode == 1 ---> DC

            Mode == 2 ---> RMS
            
            Mode == 3 ---> Peak

            Resolution == 1 ---> 3 digits
            
            Resolution == 2 ---> 4 digits
            
            Resolution == 3 ---> 5 digits

            RMS Filter == 1 ---> Wide Band
            
            RMS Filter == 2 ---> Narrow Band
            
            RMS Filter == 3 ---> Low Pass

            Peak Mode == 1 ---> Periodic
            
            Peak Mode == 2 ---> Pulse

            Peak Display == 1 ---> Positive
            
            Peak Display == 2 ---> Negative
            
            Peak Display == 3 ---> Both
        '''
        if Mode < 1 or Mode > 3:
            return
        if Resolution < 1 or Resolution > 3:
            return
        if RMS_Filter_mode < 1 or RMS_Filter_mode > 3:
            return
        if Peak_Mode < 1 or Peak_Mode > 2:
            return
        if Peak_Display < 1 or Peak_Display > 3:
            return
        
        self.Instr.write(f"RDGMODE {Mode},{Resolution},{RMS_Filter_mode},{Peak_Mode},{Peak_Display}")
    
    def Read_Freq(self) -> float:
        '''
        Measure AC field freq (Hz).
        It can be used only when the measurement mode is RMS.
        '''
        freq = float(self.Instr.query("RDGFRQ?"))
        return freq

    def Read_Resist(self) -> float:
        '''
        Measure resistance of the Hall sensor
        '''
        resist = float(self.Instr.query("RDGOHM?"))
        return resist
    
    def Read_Peak(self) -> tuple:
        '''
        Measure positive and negative peak values
        '''
        vals = tuple(map(float, self.Instr.query("RDGPEAK?").split()))
        return vals

    def Read_Probe_Temp(self) -> float:
        '''
        Measure probe temperature
        '''
        temp = float(self.Instr.query("RDGTEMP?"))
        return temp

if __name__ == "__main__":
    my475 = Model_475("GPIB::14::INSTR")
    my475.Set_Unit(Mode = 3)
    my475.Set_Range(Mode = 4)
    print(my475.Read_Field())