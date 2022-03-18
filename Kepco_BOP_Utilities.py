import pyvisa as pv

rm = pv.ResourceManager()

class Kepco_BOP:

    def __init__(self, GPIB_Addr:str) -> None:
        
        self.GPIB_Addr = GPIB_Addr
        self.Instr = rm.open_resource(GPIB_Addr)
        self.Reset()

    def Reset(self) -> None:
        self.Instr.write("*RST")
        self.Clear()
    
    def Clear(self) -> None:
        self.Instr.clear()
    
    def Output_Mode(self, Mode:str) -> None:
        '''
        Mode can be either VOLT or CURR
        '''
        if Mode == "VOLT" or Mode == "CURR":
            self.Instr.write(f"FUNC:MODE {Mode}")
        self.Clear()
    
    def Power_Output(self, Switch:bool) -> None:
        '''
        Switch on/off the output
        '''
        if Switch:
            self.Instr.write("OUTP ON")
        else:
            self.Instr.write("OUTP OFF")
        self.Clear()
    
    def Set_Current_Output(self, Current:float) -> None:
        '''
        Set output current (A)
        this can only be used when the output mode is current mode
        '''
        self.Instr.write(f"CURR {Current}")
        self.Clear()

    def Set_Voltage_Limit(self, Voltage:float) -> None:
        '''
        Set voltage output limit (V) to protect the instrument
        this can only be used when the output mode is current mode
        '''
        self.Instr.write(f"VOLT {Voltage}")
        self.Clear()
    
    def Set_Voltage_Output(self, Voltage:float) -> None:
        '''
        Set output voltage (V)
        this can only be used when the output mode is voltage mode
        '''
        self.Instr.write(f"VOLT {Voltage}")
        self.Clear()
    
    def Set_Current_Limit(self, Current:float) -> None:
        '''
        Set current output limit (A) to protect the instrument
        this can only be used when the output mode is voltage mode
        '''
        self.Instr.write(f"CURR {Current}")

if __name__ == "__main__":
    BOP_36_12 = Kepco_BOP("GPIB::6::INSTR")
    BOP_36_12.Power_Output(Switch = True)
    BOP_36_12.Output_Mode("CURR")
    BOP_36_12.Set_Voltage_Limit(Voltage = 10)
    BOP_36_12.Set_Current_Output(Current = 1)
    