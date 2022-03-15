import GHOST_Utilities
import SMB100A_Utilities
import Opto_Stage_Utilities
from datetime import datetime
'''
This code is for spatial scanning to measure spatial dependence of magnon signal.
It requires motorized stages (SHOT-302GS), rf generator (SMB100A), and BLS (Ghost)
To control SHOT-302GS, it should be setted to HOST mode.
'''

def Read_Files_And_Plot(Folder:str, fnames:list, freq:float) -> None:
    '''
    Read files and plot as 3d map
    '''
    import numpy as np
    import originpro as op

    origin = op.set_show()
    
    for file in fnames:
        data = np.loadtxt(fname = Folder + "\\" + file + '.raw')
        f = data[:, 0]
        count = data[:, 1]

        worsheet = op.new_sheet(type = 'w')
        worsheet.from_list(col = 0, data = f, lname = "Frequency", units = "GHz")
        worsheet.from_list(col = 1, data = count, lname = "Count", units = "a.u.", comments = file)

        gp = op.new_graph()
        gl = gp[0]
        gl.add_plot(obj = worsheet, colx = 0, coly = 1)
        gl.rescale()


if __name__ == "__main__":
    
    BLS = GHOST_Utilities.GHOST()
    RF = SMB100A_Utilities.SMB100A("GPIB::28::INSTR")
    Stages = Opto_Stage_Utilities.Opto_Stage("GPIB::8::INSTR")

    # Stages Part
    Length = int(input("Length of Scanning in X direction (step) = "))
    Stepx = int(input("Step Size of Scanning in X direction (step) = "))
    Width = int(input("Length of Scanning in Y direction (step) = "))
    Stepy = int(input("Step Size of Scanning in Y direction (step) = "))
    # BLS Part
    Time = float(input("Accumulation Time for each BLS Spectrum (min) = "))
    BLS.Set_Saving_Directory("D:\Data")
    # RF Part
    Freq = float(input("Frequency of RF (GHz) = "))
    Power = float(input("Output Power Level of RF (dBm) = "))
    RF.Set_CW_Freq(Freq = Freq)
    RF.Set_Output_Power(Power = Power)
    RF.Set_Output_State(True)

    # File name list
    fname_list = []

    # Start Measurement
    for i in range(0, Length, Stepx):
        for j in range(0, Width, Stepy):
            print(f"i = {i}, and j = {j}")
            # Stage Part
            Stages.Move_Relative(Axis = "Y", Direction = "+", Displacement = Stepy)
            Stages.Wait_For_Running()
            # File Part
            filename = f"{datetime.today().date()}_Point_{i}_Point_{j}"
            fname_list.append(filename)
            # BLS Part
            BLS.Measurement_Start(Sleep_Time = Time)
            BLS.Data_Saving(filename = filename)
            BLS.Clear_Spectrum()
            print(f"{filename} is saved!")
        Stages.Move_Relative(Axis = "Y", Direction = "-", Displacement = Width)
        Stages.Wait_For_Running()
        Stages.Move_Relative(Axis = "X", Direction = "+", Displacement = Stepx)
        Stages.Wait_For_Running()
    Stages.Move_Relative(Axis = "X", Direction = "-", Displacement = Length)
    Stages.Wait_For_Running()
    
    # Disconnect from BLS
    BLS.Close()
    # Close RF
    RF.Set_Output_State(False)

    # Read files and draw a map
    Read_Files_And_Plot(Folder = "D:\Data", fnames = fname_list, freq = Freq)