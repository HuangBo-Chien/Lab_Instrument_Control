from importlib.resources import Resource
import pyvisa as pv

rm = pv.ResourceManager()

class SR830:

    def __init__(self, GPIB_Addr:str) -> None:
        
        self.GPIB_Addr = GPIB_Addr
        self.Instr = rm.open_resource(GPIB_Addr)
        self.Reset()
    
    def Reset(self) -> None:
        """
        Reset the instrument
        """
        self.Instr.write("*RST")
    
    def Auto_Phase(self) -> None:
        """
        auto-set the phase
        """
        pass

    def Auto_Range(self) -> None:
        """
        auto-set the volt range
        """
        pass

    def Set_Time_Const(self, time_const:int) -> None:
        pass

if __name__ == "__main__":
    mySR830 = SR830()