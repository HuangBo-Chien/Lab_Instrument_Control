import pyvisa as pv

rm = pv.ResourceManager()

class SMB100A:

    def __init__(self, GPIB_Addr:str) -> None:
        
        self.GPIB_Addr = GPIB_Addr
        self.Instr = rm.open_resource(GPIB_Addr)
        self.Unit_table = ["Hz", "kHz", "MHz", "GHz"]
        self.Reset()
    
    def Reset(self) -> None:

        self.Instr.write("*RST")
    
    def Set_CW_Freq(self, Freq:float, Unit:int = 3) -> None:
        '''
        Set the freq of continuous wave
        Unit == 0 ---> Hz
        Unit == 1 ---> kHz
        Unit == 2 ---> MHz
        Unit == 3 ---> GHz
        '''
        if Unit < 1 or Unit > 3:
            return
        self.Instr.write(f"SOUR:FREQ:CW {Freq}{self.Unit_table[Unit]}")
    
    def Set_Sweep_by_Center_Span(self, Center:float, Span:float, Unit:int = 3) -> None:
        '''
        Set freq sweeping by specifing center freq and freq span
        Unit == 0 ---> Hz
        Unit == 1 ---> kHz
        Unit == 2 ---> MHz
        Unit == 3 ---> GHz
        '''
        if Unit < 1 or Unit > 3:
            return
        self.Instr.write(f"SOUR:FREQ:CENT {Center}{self.Unit_table[Unit]}")
        self.Instr.write(f"SOUR:FREQ:SPAN {Span}{self.Unit_table[Unit]}")
    
    def Set_Sweep_by_Start_Stop(self, Start:float, Stop:float, Unit:int = 3) -> None:
        '''
        Set freq sweeping by specifing freq start and freq stop
        Unit == 0 ---> Hz
        Unit == 1 ---> kHz
        Unit == 2 ---> MHz
        Unit == 3 ---> GHz
        '''
        if Unit < 1 or Unit > 3:
            return
        if Start > Stop:
            print("Start Freq > Stop Freq")
            return
        self.Instr.write(f"SOUR:FREQ:STAR {Start}{self.Unit_table[Unit]}")
        self.Instr.write(f"SOUR:FREQ:STOP {Stop}{self.Unit_table[Unit]}")
    
    def Set_Output_Power(self, Power:float) -> None:
        '''
        Set output power (dBm)
        '''
        self.Instr.write(f"SOUR:POW:LEV:IMM:AMPL {Power}")
    
    def Set_Output_State(self, State:bool) -> None:
        '''
        Switch on/off the output
        State can be either Ture or False to indicate On or OFF
        '''
        if State:
            self.Instr.write("OUTP:STAT ON")
        else:
            self.Instr.write("OUTP:STAT OFF")

if __name__ == "__main__":
    mySMB100A = SMB100A("GPIB::28::INSTR")
    mySMB100A.Set_CW_Freq(Freq = 10) # set freq to 10 GHz
    mySMB100A.Set_Output_Power(Power = 15) # set power to 15 dBm
    mySMB100A.Set_Output_State(State = True)
    
    from time import sleep
    sleep(10)
    mySMB100A.Set_Output_State(State = False)

