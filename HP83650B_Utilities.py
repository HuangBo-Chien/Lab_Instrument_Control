import pyvisa as pv

rm = pv.ResourceManager()

class HP_83650B:

    def __init__(self, GPIB_Addr:str) -> None:
        self.GPIB_Addr = GPIB_Addr
        self.Instr = rm.open_resource(self.GPIB_Addr)
        self.Allowed_Unit = ["Hz", "kHz", "MHz", "GHz"]
        self.Reset()

    def Reset(self) -> None:
        self.Instr.write("*RST")
    
    def Set_CW_Freq(self, Freq:float, Unit:int) -> None:
        '''
        Set the freq of continuous wave
        unit = 0 ---> Hz
        unit = 1 ---> kHz
        unit = 2 ---> MHz
        unit = 3 ---> GHz
        '''
        if 0 <= Unit <= 3:
            self.Instr.write(f"FREQ:CW {Freq} {self.Allowed_Unit[Unit]}")
    
    def Set_Wave_Mode(self, Mode:int) -> None:
        '''
        mode = 0 ---> CW mode
        mode = 1 ---> Sweep mode
        mode = 2 ---> List (no availible now...)
        '''
        if 0 <= Mode <= 1:
            self.Instr.write(f"FREQ:MODE {Mode}")
    
    def Set_Sweep_by_Center_Span(self, Center:float, Span:float, Unit:int) -> None:
        '''
        unit = 0 ---> Hz
        unit = 1 ---> kHz
        unit = 2 ---> MHz
        unit = 3 ---> GHz
        '''
        if 0 <= Unit <= 1:
            self.Instr.write(f"FREQ:CEN {Center} {self.Allowed_Unit[Unit]}")
            self.Instr.write(f"FREQ:CEN {Span} {self.Allowed_Unit[Unit]}")
    
    def Set_Sweep_by_Start_Stop(self, Start:float, Stop:float, Unit:int) -> None:
        '''
        unit = 0 ---> Hz
        unit = 1 ---> kHz
        unit = 2 ---> MHz
        unit = 3 ---> GHz
        '''
        if 0 <= Unit <= 1:
            self.Instr.write(f"FREQ:CEN {Start} {self.Allowed_Unit[Unit]}")
            self.Instr.write(f"FREQ:CEN {Stop} {self.Allowed_Unit[Unit]}")
    
    def Set_AM_Mod_Linear_Depth(self, Depth:float) -> None:
        '''
        Set Amplitude Modulation Depth.
        '''
        pass

    def Set_Modulation_Mode(self, Mode:int) -> None:
        if Mode == 0:
            self.Instr.write("MOD:OUTP:AM")
        elif Mode == 1:
            self.Instr.write("MOD:OUTP:FM")
    
    def Switch_Modulation(self, Swith:bool) -> None:
        '''
        Switch On/Off modulation 
        '''
        self.Instr.write(f"MOD:OUTP:STAT {int(Swith)}")
    
    def Set_Power_Level(self, Lev:float) -> None:
        '''
        Set Output Power Level (dBm)
        '''
        self.Instr.write(f"POW:LEV {Lev} DBM")
    
    def Set_Sweep_Time(self, time:float) -> None:
        '''
        Set sweeping time for sweep functions
        '''
        pass

    def Power_Output(self, Switch:bool) -> None:
        '''
        Switch on/off the output
        '''
        if Switch:
            self.Instr.write("POW:STAT ON")
        else:
            self.Instr.write("POW:STAT OFF")

class AM_Modulation:

    def __init__(self) -> None:
        self.Depth = 30
        self.Freq = 1000
        self.State = False # off
    

if __name__ == "__main__":
    my83650B = HP_83650B("GPIB::19::INSTR")
    my83650B.Power_Output(Switch = True)
    my83650B.Set_Power_Level(Lev = 15)
    my83650B.Set_CW_Freq(Freq = 9, Unit = 3)