import pyvisa as pv
import time

rm = pv.ResourceManager()

class Opto_Stage:

    def __init__(self, GPIB_Addr:str) -> None:
        
        self.GPIB_Addr = GPIB_Addr
        self.Instr = rm.open_resource(self.GPIB_Addr)
        self.Axis_Table = {"X":1, "Y":2}

    def Start(self) -> None:
        '''
        Execute Command
        '''
        time.sleep(0.5)
        self.Instr.write("G:")
    
    def Jogging(self, Direction:chr, Axis:chr) -> None:
        '''
        Move steadily toward a specific direction along an axis.
        Direction can be + or -
        Axis can be X or Y
        '''
        self.Instr.write(f"J:{self.Axis_Table[Axis]}{Direction}")

    def Wait_For_Running(self) -> None:
        '''
        Wait for the stages to stop
        '''
        while True:
            time.sleep(0.5)
            status = self.Instr.query("!:")
            # print(status)
            if status == "R\r\n":
                break
        print("Stage Idle!")
    
    def Homing(self, Axis:chr) -> None:
        '''
        Return to mechanical origin
        Axis can be either X or Y
        '''
        if Axis == "X" or Axis == "Y":
            self.Instr.write(f"H:{self.Axis_Table[Axis]}")
    
    def Move_Relative(self, Axis:chr, Displacement:int) -> None:
        '''
        Move relative to the current stage position
        Axis can be either X or Y
        The unit of Displacement is
        1. Pulse, if it's open loop
        2. um, if it's closed loop
        '''

        if Displacement < 0:
            Direction = "-"
        else:
            Direction = "+"

        if (Axis == "X" or Axis == "Y"):
            self.Instr.write(f"M:{self.Axis_Table[Axis]}{Direction}P{abs(Displacement)}")
            self.Start()

    def Move_Absolute(self, Axis:chr, Position:int):
        '''
        Move to absolute position
        The unit of Displacement is
        1. Pulse, if it's open loop
        2. um, if it's closed loop
        '''

        if Position < 0:
            Direction = "-"
        else:
            Direction = "+"

        if (Axis == "X" or Axis == "Y"):
            self.Instr.write(f"A:{self.Axis_Table[Axis]}{Direction}P{abs(Position)}")
            self.Start()

    def Set_Moving_Speed(self, Axis:chr, Min_Speed:int, Max_Speed:int, Acceleration_Time:int) -> None:
        '''
        Set moveing speed
        '''
        if Min_Speed < 1 or Min_Speed > 500000 or Max_Speed < 1 or Max_Speed > 500000 or Acceleration_Time < 1 or Acceleration_Time > 1000:
            return
        if Min_Speed > Max_Speed:
            return
        if Min_Speed < 64 and Max_Speed >= 8000:
            return
        if Axis == "X" or Axis == "Y":
            self.Instr.write(f"D:{self.Axis_Table[Axis]}S{Min_Speed}F{Max_Speed}R{Acceleration_Time}")
    
    def Set_Number_of_Steps(self, Axis:str, Num_of_Steps:int) -> None:
        '''
        Refer to the manual page 27
        1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 80, 100, 125, 200, 250 are allowed values
        '''
        if Axis != "X" and Axis != "Y":
            return
        
        allowed_num_of_steps = set(1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 80, 100, 125, 200, 250)

        if Num_of_Steps in allowed_num_of_steps:
            self.Instr.write(f"S:{self.Axis_Table[Axis]}{Num_of_Steps}")

if __name__ == "__main__":
    mystage = Opto_Stage("GPIB::8::INSTR")
    mystage.Move_Absolute(Axis = "X", Position = -300)
    mystage.Wait_For_Running()
    mystage.Move_Absolute(Axis = "Y", Position = 7900)
    # mystage.Move_Relative(Axis = 'X', Direction = '-', Displacement = 500)
    mystage.Wait_For_Running()
    
