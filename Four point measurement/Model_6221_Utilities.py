from importlib.resources import Resource
import pyvisa as pv

rm = pv.ResourceManager()

def Device_Connection(GPIB: str) -> Resource:
    '''
    Reture an instance of VISA resource
    '''
    return rm.open_resource(GPIB_Addr)

def Reset(Dev: Resource) -> None:
    '''
    Send *RST to model 6221
    '''
    Dev.write("*RST")

def Check_2182_Connection(Dev) -> bool:
    '''
    Check if model 2182 is connected.
    '''
    ans = Dev.query(":SOUR:PDEL:NVPR?")
    return (ans == 1) # ans == 1 means conenction is ok, vice versa.

def Send_Commands_to_2182(Dev, Commands:list) -> None:
    '''
    Send commands to model 2182 through model 6221
    '''
    prefix = "SYST:COMM:SER " # common prefix
    for command in Commands:
        Dev.write(f"{prefix}\"{command}\"")

def Send_Commands_to_6221(Dev, Commands:list) -> None:
    for command in Commands:
        Dev.write(command)

class PulseDelta_Setting():
    
    def __init__(self) -> None:
        self.setting = {} # create a dict to store setting

if __name__ == "__main__":
    GPIB_Addr = "GPIB::0:INSTR"
    model_6221 = Device_Connection(GPIB = GPIB_Addr)