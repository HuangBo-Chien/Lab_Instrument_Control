from turtle import width
import pyvisa as pv
import time
import numpy as np

rm = pv.ResourceManager()

class Model_6221:

    def __init__(self, GPIB_Addr:str) -> None:
        self.Addr = GPIB_Addr
        self.Identity = rm.open_resource(GPIB_Addr)
        self.Reset()
    
    def Reset(self) -> None:
        self.Identity.write("*RST")

    def Check_2812_Connection(self, Mode:str) -> bool:
        '''
        Mode can only be DEL, PDEL, DCON
        '''
        Modes = ("DEL", "PDEL", "DCON")
        if Mode in Modes:
            q = self.Identity.query(f":SOUR:{Mode}:NVPR?") # check if Model 2182 is correctly connected with Nodel 6221
            return (q == 1) # 1 = yes, 0 = no
        else:
            return False
    
    def Send_Command_to_2182(self, Commands:list) -> None:
        '''
        send commands from 6221 to 2182
        '''
        prefix = "SYST:COMM:SER "
        for command in Commands:
            self.Identity.write(f"{prefix}\"{command}\"")
    
    def Set_Compliance(self, Comp:int = 105) -> None:
        if 1 <= Comp <= 105:
            self.Identity.write(f"SOUR:CURR:COMP {Comp}")

    def PulseDelta_Mode(self) -> np.array:
        PD = self.Pulsedelta
        commands = PD.Generate_Command()
        for command in commands:
            self.Identity.write(command)
        
        self.Identity.write(":SOUR:PDEL:ARM")
        self.Identity.write(":INIT:IMM") # start the measurement
        count_num = 0
        while True:
            event_response = self.Identity.query(":STAT:OPER:EVEN?")
            if (event_response & 1024) >> 10 and not (event_response & 64) >> 6:
                break
            if (event_response & 32) >> 5:
                count_num += 1
                print(count_num)
        self.Identity.write(":SOUR:SWE:ABOR")
        return np.reshape(np.array(map(np.float64, self.Identity.query(":TRAC:DATA?").split(","))), (-1, 2))

    class Pulsedelta:
        """
        Pulse Delta Mode
        Unit of params related to current are uA.
        Unit of delay time and pulse width are us.
        Unit of interval is power line cycle (PLC). e.g. 60Hz ---> 1 PLC = 1 / 60 s ~ 16.667 ms
        
        If Sweep mode is on, then I_high and I_low are replaced with I_start and I_stop in the sweep mode.
        CountNUm in the Pulse Delta mode is also replaced with CountNum in the Sweep mode.
        """
        def __init__(self) -> None:
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
        
        def Set_I_High(self, I_high:float) -> None:
            self.PD["HIGH"] = I_high
        
        def Set_I_Low(self, I_low:float) -> None:
            self.PD["LOW"] = I_low
        
        def Set_Pulse_Width(self, Width:int) -> None:
            self.PD["WIDT"] = Width
        
        def Set_Source_Delay(self, Delay:int) -> None:
            self.PD["SDEL"] = Delay
        
        def Set_Count_Num(self, Number:int) -> None:
            self.PD["COUN"] = Number
        
        def Set_Source_Range(self, Mode:str) -> None:
            self.PD["RANG"] = Mode
        
        def Set_Interval(self, Interval:int) -> None:
            self.PD["INT"] = Interval
        
        def Set_Low_Measurement(self, Mode:int) -> None:
            self.PD["LME"] = Mode
        
        def Set_Sweep(self, Mode:bool) -> None:
            self.PD["SWE"] = Mode
        
        def Set_CURR_Compliance(self, Comp:int) -> None:
            self.CURR["COMP"] = Comp
        
        def Set_CURR_Start(self, I:float) -> None:
            self.CURR["STAR"] = I

        def Set_CURR_Stop(self, I:float) -> None:
            self.CURR["STOP"] = I
        
        def Set_Sweep_Cycle(self, Cycle:int) -> None:
            self.SWE["COUN"] = 1

        def Set_Sweep_Range(self, Range:str) -> None:
            self.SWE["RANG"] = Range
        
        def Set_Sweep_Point(self, Pt:int) -> None:
            self.SWE["POIN"] = Pt
        
        def Set_Sweep_Pattern(self, Mode:int) -> None:
            self.SWE["SPAC"] = Mode

        def Show_Setting(self):
            print(f"\
            ********** Pulse Delta Mode Setting **********\
            I high = {self.I_high} uA\n\
            I low = {self.I_low} uA\n\
            Pulse Width = {self.Width} us\n\
            Source Delay = {self.Src_delay} us\n\
            Number of pts to collect = {self.CountNum} \n\
            Source Range setting = {self.SrcRng} \n\
            Interval = {self.Interval} PLC \n\
            **********************************************")
        
        def Generate_Command(self) -> list:
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

    class Sweep:

        def __init__(self) -> None:
            pass
    
    class Delta:

        def __init__(self) -> None:
            pass

    class Diff_Cond:

        def __init__(self) -> None:
            pass
    

    # def PulseDelta_Setting(self, I_high:float, I_low:float, Width:float, Src_delay:float, CountNum:str = "INF", SrcRng:str = "Best", Interval:int = 5, Sweep:bool = False, Low_Meas:int = 2) -> None:
    #     '''
    #     Pulse Delta Mode
    #     '''
    #     if self.Check_2182_Connection("PulseDelta"):
    #         if -105e-3 <= I_high <= 105e-3:
    #             self.Identity.write(f":SOUR:PDEL:HIGH {I_high}")
    #         if -105e-3 <= I_low <= 105e-3:
    #             self.Identity.write(f":SOUR:PDEL:LOW {I_low}")
    #         if 50e-6 <= Width <= 12e-3:
    #             self.Identity.write(f":SOUR:PDEL:WIDT {Width}")
    #         if 16e-6 <= Src_delay <= 11.966e-3:
    #             self.Identity.write(f":SOUR:PDEL:SDEL {Src_delay}")
    #         if (CountNum.isnumeric() and 1 <= int(CountNum) <= 65636) or CountNum == "INF":
    #             self.Identity.write(f":SOUR:PDEL:COUN {CountNum}")
    #             self.Identity.write(f":TRAC:POIN {CountNum}") # the number of traced points == the number of count
    #         if SrcRng in ("BEST", "FIX"):
    #             self.Identity.write(f":SOUR:PDEL:RANG {SrcRng}")
    #         if 5 <= Interval <= 999999:
    #             self.Identity.write(f":SOUR:PDEL:INT {Interval}")
    #         self.Identity.write(f":SOUR:PDEL:SWE {Sweep}")
    #         if Low_Meas in (1, 2):
    #             self.Identity.write(f":SOUR:PDEL:LME {Low_Meas}")
    #     else:
    #         pass
    #         # raise DevConnectionError(Devname = "Model 2182")
    
    def Show_Setting(self, Mode:str) -> None:

        if Mode == "PulseDelta":
            pass

if __name__ == "__main__":
    my_Model_6221 = Model_6221
    # check model 2182 connection
    # set model 2182 volt range and number of plc
    # set model 6221 to pulse delta mode
    # arm the mode
    # start the measurement
