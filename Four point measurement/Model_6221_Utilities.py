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
        # pulse delta setting
        self.PD = {}
        self.PD["HIGH"] = 100.0
        self.PD["LOW"] = 0.0
        self.PD["WIDT"] = 100
        self.PD["SDEL"] = 100
        self.PD["COUN"] = 1
        self.PD["RANG"] = "Best"
        self.PD["INT"] = 5
        self.PD["LME"] = 2
        self.PD["SWE"] = False
        # sweep setting for the sweep mode
        self.SWE = {}
        self.SWE["SPAC"] = 1
        self.SWE["POIN"] = 1
        self.SWE["RANG"] = "Best"
        self.SWE["COUN"] = 1
        # current setting in tje sweep mode
        self.CURR = {}
        self.CURR["STAR"] = 10.0
        self.CURR["STOP"] = 0.0
        self.CURR["COMP"] = 105
    
    def Commands_Generation(self) -> list:
        Commands = []
        prefix = "SOUR:PDEL:"
        for key, val in self.PD.items():
            Commands.append(f"{prefix}{key} {val}")
        if self.PD["SWE"] == True:
            prefix = "SOUR:SWE:"
            for key, val in self.SWE.items():
                Commands.append(f"{prefix}{key} {val}")
            prefix = "SOUR:CURR:"
            for key, val in self.CURR.items():
                Commands.append(f"{prefix}{key} {val}")
        return Commands

if __name__ == "__main__":
    GPIB_Addr = "GPIB::0:INSTR"
    model_6221 = Device_Connection(GPIB = GPIB_Addr)
    PD_Setting = PulseDelta_Setting