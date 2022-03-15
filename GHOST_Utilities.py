from time import sleep
from telnetlib import Telnet

class GHOST:

    def __init__(self) -> None:
        self.tn = Telnet("127.0.0.1", 4000)
        self.Take_Control()

    def Input_command(self, command:str) -> str:
        '''
        Turn input command into byte string, and to the host server
        '''
        sleep(1)
        print(command)
        self.tn.write(command.encode('ascii') + b"\r\n")
        
        while True:
            sleep(0.5)
            msg = self.tn.read_very_eager().decode()
            if msg != "":
                print("Msg = ", msg)
                break
        return msg
    
    def Take_Control(self) -> None:
        '''
        Take over the remote control
        '''
        self.Input_command("OVERRIDE")
    
    def Set_Saving_Directory(self, dir:str) -> None:
        '''
        Set the directory where data are saved.
        If dir is not a legit directory, then data will be saved under D:\\Data
        '''
        try:
            self.Input_command(f"WDIR {dir}")
        except:
            self.Input_command(r"WDIR D:\Data")
    
    def Measurement_Start(self, Cycle:int = 0, Sleep_Time:int = 10) -> None:
        '''
        Start BLS measurement
        100 cycle is about 1 min
        You can either input cycle or sleep time.
        the unit of sleep time is minute
        '''
        self.Input_command(f"START {Cycle}")
        if Cycle == 0:
            Sleep_Time *= 60 # sec
            sleep(Sleep_Time)
            self.Input_command("STOP")
        else:
            Sleep_Time = (Cycle / 100 + 0.5) * 60 # sec
            sleep(Sleep_Time)
    
    def Data_Saving(self, filename:str) -> None:
        '''
        Save dat and raw files
        '''
        self.Input_command(f"SAVE {filename}.dat")
        self.Input_command(f"SAVERAW {filename}.raw")
    
    def Clear_Spectrum(self) -> None:
        '''
        Clear old spectrum
        '''
        self.Input_command("DELETE")

    def Close(self) -> None:
        '''
        Close telnet window
        '''
        self.Input_command("CLOSE")
    
    def Set_Channel(self, Mode:int) -> None:
        '''
        Set Channel
        Mode == 0 ---> 256
        Mode == 1 ---> 512
        Mode == 2 ---> 1024
        Default is 1024
        '''
        if Mode == 0:
            self.Input_command("SET256")
        elif Mode == 1:
            self.Input_command("SET512")
        else:
            self.Input_command("SET1024")
    
    def Get_Current_Spectrum(self) -> list:
        '''
        Get current spectrum
        '''
        const = 25 # status
        data = list(map(int, self.Input_command("GET_DATA").split()[const:-1]))
##        print("Data = ", data)
##        print("Len = ", len(data))
        return data

if __name__ == "__main__":
    myGhost = GHOST()
    dir = r"D:\DATA"
#    myGhost.Set_Saving_Directory(dir = dir)
    myGhost.Measurement_Start(Sleep_Time = 1)
    myGhost.Data_Saving(filename = "test") #檔名不能有空白鍵
#    print("file saved!!")
    # res = myGhost.Get_Current_Spectrum()
    myGhost.Clear_Spectrum()
    myGhost.Close()
