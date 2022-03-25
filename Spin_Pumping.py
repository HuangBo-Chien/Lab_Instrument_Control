from HP.HP83650B_Utilities import HP_83650B
from Kepco.Kepco_BOP_Utilities import Kepco_BOP
from Keithley.Model_2182_Utilities import Model_2182
from LakeShore.Model475_Utilities import Model_475
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

# Global
GM = Model_475("GPIB::14::INSTR")
VM = Model_2182("GPIB::7::INSTR")
Kepco = Kepco_BOP("GPIB::6::INSTR")
RF = HP_83650B("GPIB::19::INSTR")

def GM_Setting():

    GM.Set_Unit(3)
    GM.Set_Range(4)

def Kepco_Setting():
    Kepco.Power_Output(Switch = True)
    Kepco.Output_Mode("CURR")
    Kepco.Set_Voltage_Limit(20)

def VM_Setting():

    VM.Analog_Filter_Setting(True)
    VM.Digital_Filter_Setting(Count = 10)
    VM.Select_PLC(2)
    VM.Select_Volt_Range(0.01)

def Fix_H_Scan_Freq(fix_curr:float, rf_pow:float, start_freq:float, stop_freq:float, step_freq:float = 0.1):

    # GM
    GM_Setting()

    # Kepco
    Kepco_Setting()

    # VM
    VM_Setting()

    # RF
    RF.Power_Output(Switch = True)
    RF.Set_Power_Level(Lev = 14)

    Freq_array = np.arange(start_freq, stop_freq + step_freq, step_freq)
    data = np.zeros(np.size(Freq_array))

    for curr in np.arange(0, fix_curr + 0.1, 0.1):
        Kepco.Set_Current_Output(curr)
        sleep(1)

    for i in range(len(Freq_array)):
        RF.Set_CW_Freq(Freq_array[i], 3)
        sleep(1)

        data[i] = VM.Sense_Volt(10) * 1e6
    
    for curr in np.arange(fix_curr, 0, 0.1 * np.sign(-fix_curr)):
        Kepco.Set_Current_Output(curr)
        sleep(1)

    plt.plot(Freq_array ,data, 'o')
    plt.show()

def Fix_Freq_Scan_H(curr_max:float, curr_step:float, rf_pow:float, fix_freq:float):
    
    # GM
    GM_Setting()

    # Kepco
    Kepco_Setting()

    # VM
    VM_Setting()

    # RF
    RF.Power_Output(Switch = True)
    RF.Set_CW_Freq(fix_freq, 3)
    RF.Set_Power_Level(Lev = rf_pow)

    # curr_max = 4
    Curr_array = np.arange(curr_max, -curr_max, -curr_step)
    Field = np.zeros(np.size(Curr_array))
    data = np.zeros(np.size(Curr_array))

    for curr in np.arange(0, curr_max + 0.1, 0.1):
        Kepco.Set_Current_Output(curr)
        sleep(1)

    # Kepco.Set_Current_Output(1)
    # sleep(5)

    for i in range(len(Curr_array)):    
        # Kepco.Set_Current_Output(float(Curr_array[i]))
        Kepco.Set_Current_Output(Curr_array[i])
        sleep(1)
        # print(i)
        # print(i, Curr_array[i])
        Field[i] = GM.Read_Field()
        data[i] = VM.Sense_Volt(10) * 1e6

        plt.figure(1)
        plt.clf()
        plt.plot(Field[:i + 1], data[:i + 1], 'o')
        plt.xlabel("H (Oe)")
        plt.ylabel("V (uV)")
        plt.draw()
        plt.pause(0.1)
    
    for curr in np.arange(-curr_max, 0.1, 0.1):
        Kepco.Set_Current_Output(curr)
        print(round(curr, 2))
        # Kepco.Clear()
        sleep(1)

    plt.figure(2)
    plt.plot(Field ,data, 'o')
    plt.xlabel("H (Oe)")
    plt.ylabel("V (uV)")
    plt.show()

if __name__ == "__main__":
    # Fix_H_Scan_Freq()
    Fix_Freq_Scan_H(4, 0.01, 15, 9)