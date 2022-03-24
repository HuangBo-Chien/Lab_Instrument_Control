import pyvisa as pv
from time import sleep

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
        self.Instr.write("APHS")

    def Auto_Sense_Range(self) -> None:
        """
        auto-set the volt range
        """
        self.Instr.write("AGAN")
    
    def Auto_Reserve(self) -> None:
        '''
        auto-reserve
        '''
        self.Instr.write("ARSV")

    def Set_Time_Const(self, Mode:int) -> None:
        '''
        Choose time constant
        Mode can be 0 ~ 19, from 10 us to 30 ks
        Except 1 us, 3 us, 100 ks, and 300 ks, {1, 3, 10, 30, 100, 300} X {us, ms, s, ks} can be chosen.
        30 ms ~ 300 ms are usually used.
        '''
        if 0 <= Mode <= 19:
            self.Instr.write("OFLT {Mode}")

    def Set_Sync_Filter(self, Switch:bool) -> None:
        '''
        Switch On/Off sync filter
        The filter is only effective when demod freq is less than 200 Hz.
        Switch == True ---> Switch on the filter
        Switch == False ---> Switch off the filter
        '''
        self.Instr.write(f"SYNC {int(Switch)}")
    
    def Set_Filter_Slope(self, Mode:int) -> None:
        '''
        Choose the slope of low pass filter.
        mode = 0 ---> 6 dB/oct
        mode = 1 ---> 12 dB/oct
        mode = 2 ---> 18 dB/oct
        mode = 3 ---> 24 dB/oct
        Larger slope attenuates noises better. In return, it costs longer time to stablize.
        24 dB/oct is still recommended.
        '''
        if 0 <= Mode <= 4:
            self.Instr.write(f"OFSL {Mode}")
    
    def Set_Reserve_Mode(self, Mode:int) -> None:
        '''
        Choose the mode
        mode = 0 ---> High Reserve
        mode = 1 ---> Normal
        mode = 2 ---> Low Noise
        High reserve is recommended.
        '''
        if 0 <= Mode <= 2:
            self.Instr.write(f"RMOD {Mode}")

    def Set_Sense_Range(self, Mode:int) -> None:
        '''
        Set sensitivity range
        Mode can be 0 ~ 26
        20 uV/pA ~ 5 mV/nA are usually used.
        Auto-gain is recommended.
        '''
        if 0 <= Mode <= 26:
            self.Instr.write(f"SENS {Mode}")
    
    def Set_Input_Config(self, Mode:int) -> None:
        '''
        set input configuration.
        mode = 0 ---> A
        mode = 1 ---> A - B
        mode = 2 ---> 1 Mohm
        mode = 3 ---> 100 Mohm
        A is always used.
        '''
        if 0 <= Mode <= 3:
            self.Instr.write(f"ISRC {Mode}")
    
    def Set_Shield_Grounding(self, Mode:int) -> None:
        '''
        set shield ground
        mode = 0 ---> float
        mode = 1 ---> ground
        float is usually used.
        '''
        if 0 <= Mode <= 1:
            self.Instr.write(f"IGND {Mode}")
    
    def Set_Input_Coupling(self, Mode:int) -> None:
        '''
        set input coupling
        mode = 0 ---> AC coupling
        mode = 1 ---> DC coupling
        AC is recommended to filter out offset voltage
        '''
        if 0 <= Mode <= 1:
            self.Instr.write(f"ICPL {Mode}")
    
    def Set_Harmonic(self, Harm:int) -> None:
        '''
        set harmonics number
        the number should be in the range from 1 to 19999
        harm number X demod freq <= 102 kHz
        Harm = 1 or 2 are usually used.
        '''
        if 1 <= Harm <= 19999:
            self.Instr.write("Harm {Harm}")
    
    def Measure(self, X:bool = False, Y:bool = False, R:bool = False, Phase:bool = False) -> dict:
        '''
        take data from SR830
        Users can use True/False to include/exclude X, Y, R, and Phase.  
        Results are returned as a dict
        '''
        quantities = []
        if X:
            quantities.append(1)
        if Y:
            quantities.append(2)
        if R:
            quantities.append(3)
        if Phase:
            quantities.append(4)
        
        table = ["X", "Y", "R", "Phase"]
        res = {}

        for quantity in quantities:
            res[table[quantity]] = self.Instr.query(f"OUTP {quantity}")
            sleep(0.1)
        
        return res

if __name__ == "__main__":
    mySR830 = SR830()
    mySR830.Auto_Sense_Range()
    mySR830.Set_Reserve_Mode(Mode = 0)
    mySR830.Auto_Phase()

    import matplotlib.pyplot as plt

    res = []
    for _ in range(20):
        res.append(mySR830.Measure(X = True, AVG = 10))
    plt.plot(res)
    plt.show()