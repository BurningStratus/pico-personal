import time
from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

from filefifo import Filefifo


class Line:
    def __init__(self):
        print("REINIT")
        self.pin_stop = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)
        
        self.last_peak = 0
        self.counter = 0
        self.counter_bool = False
        
        self.step_x  = 1
        self.point_x = 0
        
        ### peaks ###
        self.peak_max0 = 0
        self.peak_min0 = 0
        self.peak_max  = 0
        self.peak_min  = 0
        
        ### interval ###
        self.interval = 0
        
        # previous records
        self.point_x0  = 0
        self.feed_prev = 0
        self.avg_last = 0
        
        self.dx_prev   = 0
        self.dx_prev1  = 0
    
    def save_peaks(self):
        print(self.counter, "SAVE PEAKS 1")
        self.interval = self.counter / 250
        return
    
    def print_peak2peak(self):
        print(self.interval)
        print(self.interval / 0.004)
    
    def pk2pk(self, feed):
        '''
        Peak detection.
        '''
        #################################
        self.point_x += self.step_x
        #################################
        df = feed - self.feed_prev
        #  y = mx + b ==> b = y - mx
        b = feed - df * self.point_x
        
        if feed > self.peak_max0:
            self.peak_max0 = feed
        
        sub_x = self.point_x - self.step_x / 100
        interpolated_feed = df * sub_x + b
        
        dx = (interpolated_feed - self.feed_prev)/(sub_x - self.point_x0)

        self.dx_prev = self.dx_prev1
        self.dx_prev1 = dx
        
        avg = (self.dx_prev1 + self.dx_prev + dx) / 3

        ### this is disgusting. it's a pity it works.
        if (1 > avg > -3) and (dx - self.dx_prev) <= 0:
            
            self.counter_bool = not self.counter_bool
            if not self.counter_bool:
                self.save_peaks()
                self.counter = 0
                self.counter_bool = True
            
        # print(self.counter, dx, self.dx_prev, avg, self.counter_bool)
        print(dx, self.dx_prev)
        self.avg_last = avg
        self.dx_prev = dx
        self.feed_prev = feed
        self.point_x0 = self.point_x
        return
    
    def execute(self, feed):
        ### check butts
            ### main function
            ### self.process_data(feed)
        self.pk2pk(feed)

        if self.counter_bool:
            self.counter += 1
        
        return
    

flatline = Line()


for i in range(3):
    data = Filefifo(10, name = f'capture_250Hz_0{i + 1}.txt')
    for i in range(200):
        peak = data.get()
        flatline.execute(peak)
        time.sleep(0.04)

    flatline.print_peak2peak()
    flatline = Line()
    print("NEXT ITERATION")
    
