from TableStable.GHOST_Utilities import GHOST
from Rohde_and_Schwarz.SMB100A_Utilities import SMB100A
from Opto_Sigma.Opto_Stage_Utilities import Opto_Stage
from datetime import datetime
import numpy as np
'''
This code is for spatial scanning to measure spatial dependence of magnon signal.
It requires motorized stages (SHOT-302GS), rf generator (SMB100A), and BLS (Ghost)
To control SHOT-302GS, it should be set to HOST mode.
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

def Two_pts():

    BLS = GHOST()
    RF = SMB100A("GPIB::28::INSTR")
    Stages = Opto_Stage("GPIB::8::INSTR")

    # Stages Part
    Length = int(input("Length of Scanning in X direction (pulse) = "))
    Stepx = int(input("Step Size of Scanning in X direction (pulse) = "))
    Width = int(input("Length of Scanning in Y direction (pulse) = "))
    Stepy = int(input("Step Size of Scanning in Y direction (pulse) = "))
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
            Stages.Move_Relative(Axis = "Y", Displacement = Stepy)
            Stages.Wait_For_Running()
            # File Part
            filename = f"{datetime.today().date()}_Point_{i}_Point_{j}"
            fname_list.append(filename)
            # BLS Part
            BLS.Measurement_Start(Sleep_Time = Time)
            BLS.Data_Saving(filename = filename)
            BLS.Clear_Spectrum()
            print(f"{filename} is saved!")
        Stages.Move_Relative(Axis = "Y", Displacement = -Width)
        Stages.Wait_For_Running()
        Stages.Move_Relative(Axis = "X", Displacement = Stepx)
        Stages.Wait_For_Running()
    Stages.Move_Relative(Axis = "X", Displacement = -Length)
    Stages.Wait_For_Running()
    
    # Disconnect from BLS
    BLS.Close()
    # Close RF
    RF.Set_Output_State(False)

    # Read files and draw a map
    Read_Files_And_Plot(Folder = "D:\Data", fnames = fname_list, freq = Freq)

def Two_vectors_And_Origin():
    '''
    Assume the scanned area is a parallelogram.
    It can be spanned by an origin and two vectors starting from the origin.
    '''
    
    BLS = GHOST()
    RF = SMB100A("GPIB::28::INSTR")
    Stages = Opto_Stage("GPIB::8::INSTR")

    # BLS Part
    Time = float(input("Accumulation Time for each BLS Spectrum (min) = "))
    BLS.Set_Saving_Directory("D:\Data")
    # RF Part
    Freq = float(input("Frequency of RF (GHz) = "))
    Power = float(input("Output Power Level of RF (dBm) = "))
    RF.Set_CW_Freq(Freq = Freq)
    RF.Set_Output_Power(Power = Power)
    RF.Set_Output_State(True)
    # Stage Part
    vecs = []

    for i in range(2):
        compx = int(input(f"Input vector {i + 1} x component = "))
        compy = int(input(f"Input vector {i + 1} y component = "))
        vecs.append((compx, compy))
    
    step1 = int(input("Input the number of step to divide the vector 1 = "))
    step2 = int(input("Input the number of step to divide the vector 2 = "))

    x0 = int(input("Input origin's x component = "))
    y0 = int(input("Input origin's y component = "))

    Stages.Move_Absolute(Axis = "X", Position = x0)
    Stages.Wait_For_Running()
    Stages.Move_Absolute(Axis = "Y", Position = y0)
    Stages.Wait_For_Running()

    fname_list = []
    # Start Scanning
    i = 0
    j = 0
    for c1 in np.arange(start = 0, stop = 1, step = 1 / step1):
        i += 1
        j = 0
        for c2 in np.arange(start = 0, stop = 1, step = 1 / step2):
            j += 1
            x = int(x0 + c1 * vecs[0][0] + c2 * vecs[1][0])
            y = int(y0 + c1 * vecs[0][1] + c2 * vecs[1][1])
            Stages.Move_Absolute(Axis = "X", Position = x)
            Stages.Wait_For_Running()
            Stages.Move_Absolute(Axis = "Y", Position = y)
            Stages.Wait_For_Running()

            filename = f"{datetime.today().date()}_({i},{j})"
            fname_list.append(filename)

            BLS.Measurement_Start(Sleep_Time = Time)
            BLS.Data_Saving(filename = filename)
            BLS.Clear_Spectrum()

            print(f"{filename} is saved!")
    
    # Disconnect from BLS
    BLS.Close()
    # Close RF
    RF.Set_Output_State(False)
    # Read files and draw a map
    Read_Files_And_Plot(Folder = "D:\Data", fnames = fname_list, freq = Freq)

if __name__ == "__main__":
    Two_vectors_And_Origin()