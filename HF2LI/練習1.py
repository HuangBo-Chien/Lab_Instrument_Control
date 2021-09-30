import time
import numpy as np
import zhinst.utils as zu
import matplotlib.pyplot as plt
from zhinst.ziPython import ziListEnum as zLE

class HF2LI():

    def __init__(self):
        self.dev_ID = r"dev1580" #我們儀器的代號

        self.apilevel = 6 #目前不知道幹嘛用的

        (self.daq, self.device, _) = zu.create_api_session(self.dev_ID, self.apilevel) #宣告一個session給儀器
        zu.api_server_version_chech(self.daq) #檢查儀器驅動程式的版本

    def demod_setting(self, channel):
        self.signal_paths = [] #宣告一個list來記錄要取的data的清單
        for ch in channel:
            demod_path = f"/{device}/demods/{ch}/sample" #宣告一個前綴字串，表示等下要取第{ch + 1}個demodulator的data
            self.signal_paths.append(demod_path + ".x") #記錄第一個demod的x分量
            self.signal_paths.append(demod_path + ".y") # .. y分量
    
    def measure_setting(self):
        self.total_duration = 5 #單位:秒。宣告總共量測的時間
        self.sampling_rate = 30000 #單位:次/秒。宣告取樣頻率
        self.burst_duration = 0.2 #單位:秒。宣告每段擷取時間長度
        self.num_cols = int(np.ceil(sampling_rate * burst_duration)) #每段有{取樣頻率*擷取時間}個data
        self.num_bursts = int(np.ceil(total_duration / burst_duration)) #共有{總共量測時間/每段擷取時間}次

    def daq_module_setting(self):
        self.daq_mod = self.daq.dataAcquisitionModule() #宣告daq物件
        self.dap_mod.set("device", self.device) #選擇我們的儀器
        '''
        'type' - 設定擷取資料的形式

        0 = continuous 表示在時間內會不斷的擷取。
        '''
        self.daq_mod.set("type", 0)
        '''
        'grid/mode' - 設定data的內插方式

        1 = Nearest 表示擷取上一次的結果來當讀值回傳

        2 = Linear 表示擷取上一次和下一次的結果，做線性內插來得到讀值

        4 = Exact 表示擷取當下的讀值。在此模式下，取樣時間是儀器決定，使用者無法設定取樣時間
        '''
        self.daq_mod.set("grid/mode", 2)
        self.daq_mod.set("count", self.num_bursts) #設定daq module擷取的次數
        self.daq_mod.set("duration", self.burst_duration) #設定daq module每段的擷取時間
        self.daq_mod.set("grid/cols", num_cols) #設定daq module要取幾段

    def data_saving_setting(self, filename = None):
        if filename is not None:
            '''
            'save/fileformat' - 存檔的格式
            0 = Matlab
            1 = CSV
            '''
            self.daq_mod.set("save/fileformat", 1)
            self.daq_mod.set("save/filename", filename)
            self.daq_mod.set("save/saveonread", 1) # automatically save the data to file as soon as read() is called.

    def subscrbe_signal(self):
        self.data = {}
        for path in self.signal_paths:
            print(f"{path} is subscribed!")
            self.daq_mod.subscribe(path)
            data[path] = []

    def read_data(self):
        clockbase = float(self.daq.getInt(f"/{device}/clockbase")) #取得儀器時脈
        ts0 = np.nan
        data_read = self.daq_mod.read(True) #儀器開始擷取
        returned_paths = [path.lower() for path in data_read.keys()]
        progress = self.daq_mod.progress()[0]

        for path in self.signal_paths:
            if path.lower() in returned_paths:
                for  index, signal_burst in enumerate(data_read[path.lower()]):
                    # index表示第index次擷取
                    #signal_burst回傳
                    if np.any(np.isnan(ts0)):
                        ts0 = signal_burst["timestamp"][0, 0]
##                    t = (signal_burst["timestamp"][0, :] - ts0) / clockbase
##                    value = signal_burst["value"][0, :] 
                    num_samples = len(signal_burst["value"][0, :])
                    dt = (signal_burst["timestamp"][0, -1] - signal_burst["timestamp"][0, 0]) / clockbase #時間過多久
                    data[path].append(signal_burst) #加到data裡面
                    print(
                        f"Read: {read_count}, progress: {100 * progress: .2f}%.",
                        f"Burst {index}: {path}: {path} contains {num_samples} spanning {dt: .2f} s."
                    )
        return data, ts0

    def saving(self):
        timeout = 1.5 * self.total_duration
        t0 = time.time()
        while self.daq_mod.getInt("save/save") != 0:
            time.sleep(0.1)
            if time.time() - t0 > timeout:
                raise Exception(f"Timeout after {timeout} s before data save completed.")
        

if __name__ == "__main__":
    lock_in = HF2LI()
