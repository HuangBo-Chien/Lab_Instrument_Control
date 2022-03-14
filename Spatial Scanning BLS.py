import GHOST_Utilities
import SMB100A_Utilities
import Opto_Stage_Utilities

'''
This code is for spatial scanning to measure spatial dependence of magnon signal.
It requires motorized stages (SHOT-302GS), rf generator (SMB100A), and BLS (Ghost)
To control SHOT-302GS, it should be setted to HOST mode.
'''

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

    # Start Measurement
    for i in range(0, Length, Stepx):
        for j in range(0, Width, Stepy):
            print(f"i = {i}, and j = {j}")
            Stages.Move_Relative(Axis = "Y", Direction = "+", Displacement = Stepy)
            Stages.Wait_For_Running()
            filename = f"Point_{i}_Point_{j}"
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