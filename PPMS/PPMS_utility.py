import pyvisa

class PPMS:

    def __init__(self, GPIB_Addr = 15) -> None:
        self.GPIB_Addr = GPIB_Addr
    
    def Check_Status(self):
        pass
    
    def Wait_For_Temp(self):
        pass

    def Wait_For_Field(self):
        pass

    def Set_Temp(self, Temp = 300):
        pass

    def Set_Field(self, Field = 0, Rate = 10, Approach_Mode = 0, Mag_Mode = 0):
        # Magnetic field in Oe
        # Rate in Oe/sec
        # Approach mode: 0 ---> Linear Approach, 1 ---> No Overshoot Approach, 2 ---> Oscillate Approach
        # Mag mode: 0 ---> Persistent Mode, 1 ---> Driven Mode
        pass

    def Show_Status(self):
        pass
