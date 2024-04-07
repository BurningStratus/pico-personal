
from filefifo import Filefifo
from time import sleep

prev_peak = 0
count = 0
counter_bool = False

def count_peaks(data):
    print("FREQ:", 0.744 * data)
    return

for i in range(3):
    data = Filefifo(10, name = f'capture_250Hz_0{i + 1}.txt')
    counter_bool = False
    
    
    for i in range(100):
        peak = data.get()
        slope = peak - prev_peak
        # print(slope)
        
        if slope <= 0:
            counter_bool = True
        
        if counter_bool:
            count += 1
        
        prev_peak = peak
    
    count_peaks(count)
    # print(count)