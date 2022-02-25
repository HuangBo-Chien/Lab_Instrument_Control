import pyvisa as pv
import numpy as np

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
    
    def PulseDelta_Trigger(self) -> np.array:
        '''
        This method sends GPIB commands to trigger pulse delta mode measurement, and then return results.
        '''
        self.Instr.write(":SOUR:PDEL:ARM")
        self.Instr.write(":INIT:IMM") # start the measurement
        count_num = 0
        # keep asking whether the measurement has finished.
        while True:
            event_response = self.Instr.query(":STAT:OPER:EVEN?")
            if (event_response & 1024) >> 10 and not (event_response & 64) >> 6:
                break
            if (event_response & 32) >> 5:
                count_num += 1
                print(count_num)
        self.Instr.write(":SOUR:SWE:ABOR") # exit pulse delta mode
        return np.reshape(np.array(map(np.float64, self.Instr.query(":TRAC:DATA?").split(","))), (-1, 2))

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
    
    def Show_Setting(self) -> None:
        '''
        Print out Pulse Delta Mode setting on the screen.
        '''
        print("Pulse Delta Mode Settings")
        for key, val in self.PD.items():
            print(f"key = {key}, and val = {val}")
        if self.PD["SWE"]:
            print("Sweep Settings")
            for key, val in self.SWE.items():
                print(f"key = {key}, and val = {val}")
            print("Sweep Current Settings")
            for key, val in self.CURR.items():
                print(f"key = {key}, and val = {val}")


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
    PD = PulseDelta_Setting
    
