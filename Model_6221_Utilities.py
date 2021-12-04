import pyvisa as pv
import time

rm = pv.ResourceManager()

class Model_6221:

    def __init__(self, GPIB_Addr:str) -> None:
        self.Addr = GPIB_Addr
        self.Identity = rm.open_resource(GPIB_Addr)
    
    def Reset(self) -> None:
        self.Identity.write("*RST")

if __name__ == "__main__":
    my_Model_6221 = Model_6221