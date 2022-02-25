import Model_6221_Utilities as M6U
import numpy as np
import matplotlib.pyplot as plt
import pyvisa as pv

if __name__ == "__main__":
    GPIB_Addr = "GPIB::0::INSTR"
    Model_6221 = M6U.Device_Connection(GPIB = GPIB_Addr) # create an instance for model 6221
    
    if M6U.Check_2182_Connection(Model_6221):
        print("Model 2182 is conencted")
    else:
        print("Model 2182 is missing.")
    
    PD_Setting = M6U.PulseDelta_Setting # create an instance for pulse delta mode setting
    
