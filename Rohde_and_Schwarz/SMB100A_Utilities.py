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
        Set the freq of continuous wave.

        Parameters
        ==========
            Freq can be any positive values as long as the device can achieve.

            Unit == 0/1/2/3 ---> Hz/kHz/MHz/GHz. Default is GHz.
        '''
        if Unit < 1 or Unit > 3:
            return
        self.Instr.write(f"SOUR:FREQ:CW {Freq}{self.Unit_table[Unit]}")
    
    def Set_Sweep_by_Center_Span(self, Center:float, Span:float, Unit:int = 3) -> None:
        '''
        Set freq sweeping by specifing center freq and freq span.

        Parameters
        ==========
            Center and Span can be any positive values as long as the device can achieve.

            Unit == 0/1/2/3 ---> Hz/kHz/MHz/GHz. Default is GHz.
        '''
        if Unit < 1 or Unit > 3:
            return
        self.Instr.write(f"SOUR:FREQ:CENT {Center}{self.Unit_table[Unit]}")
        self.Instr.write(f"SOUR:FREQ:SPAN {Span}{self.Unit_table[Unit]}")
    
    def Set_Sweep_by_Start_Stop(self, Start:float, Stop:float, Unit:int = 3) -> None:
        '''
        Set freq sweeping by specifing freq start and freq stop.

        Parameters
        ==========
            Start and Stop can be any positive values as long as the device can achieve. Stop > Start.

            Unit == 0/1/2/3 ---> Hz/kHz/MHz/GHz. Default is GHz.
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
        Set output power (dBm).
        
        Parameter
        ========
            Power can be any value as long as the device can really achieve.
        '''
        self.Instr.write(f"SOUR:POW:LEV:IMM:AMPL {Power}")
    
    def Set_Output_State(self, Switch:bool) -> None:
        '''
        Switch on/off the output.

        Parameter
        ==========
            Switch == True/False ---> Turn on/off the output.
        '''
        if Switch:
            self.Instr.write("OUTP:STAT ON")
        else:
            self.Instr.write("OUTP:STAT OFF")

if __name__ == "__main__":
    mySMB100A = SMB100A("GPIB::28::INSTR")
    mySMB100A.Set_CW_Freq(Freq = 10) # set freq to 10 GHz
    mySMB100A.Set_Output_Power(Power = 15) # set power to 15 dBm
    mySMB100A.Set_Output_State(Switch = True)
    
    from time import sleep
    sleep(10)
    mySMB100A.Set_Output_State(Switch = False)

