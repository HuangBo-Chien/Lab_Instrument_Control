from importlib.resources import Resource
import pyvisa as pv

rm = pv.ResourceManager()

class Model_6221:
    def __init__(self, GPIB_Addr) -> None:
        
        self.GPIB_Addr = GPIB_Addr
        self.Instr = rm.open_resource(GPIB_Addr)
        self.Reset()
    
    def Reset(self) -> None:
        '''
        Reset model 6221 to its default settings
        '''
        self.Instr.write("*RST")

    def Check_2182_Connection(self) -> bool:
        '''
        Check if model 2182 is connected.
        '''
        ans = self.Instr.query(":SOUR:PDEL:NVPR?")
        return (ans == 1) # ans == 1 means conenction is ok, vice versa.

    def Send_Commands_to_2182(self, Commands:list) -> None:
        '''
        Send commands to model 2182 through model 6221.
        Those commands should be model 2182's commands.
        '''
        prefix = "SYST:COMM:SER " # common prefix
        for command in Commands:
            self.Instr.write(f"{prefix}\"{command}\"")

    def Send_Commands_to_6221(self, Commands:list) -> None:
        '''
        Send commands to model 6221.
        '''
        for command in Commands:
            self.Instr.write(command)

class PulseDelta_Setting():
    
    def __init__(self) -> None:
        self.setting = {} # create a dict to store setting

class Sweep_Setting():
    pass

if __name__ == "__main__":
    '''
    declare Model_6221 which provides basic methods to communicate with the instrument
    declare different classes for users to set and store functions' parameters e.g. pulse delta
    generate corresponding GPIB commands, and collect them as a list of command
    send those commands through Model_6221's function
    return results
    '''
    GPIB_Addr = "GPIB::0:INSTR"
    My_6221 = Model_6221(GPIB_Addr = GPIB_Addr)