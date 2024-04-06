# IMPORTS >##############################################

import time
from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C
from filefifo import Filefifo

import micropython
micropython.alloc_emergency_exception_buf(200)
# OLED >#################################################
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)
# DATA >#################################################
data = Filefifo(10, name = 'capture_250Hz_02.txt')

sensor = ADC(27)

# MAIN >##################################################

class Line:
    def __init__(self):
        ### buttons
        self.pin_down = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pin_clear = Pin(8, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pin_swap = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP) #swap == change direction.
        
        ### starting position
        self.point_y = 32
        self.point_x = 0
        
        ### step for the graph itself
        self.step_x = 1
        # step is for adjusting the graph.
        self.step = 500
        
        ### dynamic min/max
        # *0 means "previous" values
        self.max_val0 = 0
        self.min_val0 = 17000
        self.max_val = 0
        self.min_val = 65535
        
        # screen ceil/floor to restrict the plotter
        self.screen_ceil = 4
        self.screen_floor = 59
    
    def upd_minmax(self, value):
        '''
        Updates the min/max params dynamically.
        
        35 000/30 000
        '''
        if value > self.max_val:
            self.max_val0 = self.max_val
            self.max_val = value
            
            #### GIMMICK
            led1 = PWM(Pin(22, Pin.OUT), duty_u16=1000, freq=100)
            led1.duty_u16(1000)
            time.sleep(0.1)
            led1.duty_u16(0)
            ####
            
        else:
            pass
        if value < self.min_val:
            self.min_val0 = self.min_val
            self.min_val = value
            
            #### GIMMICK
            led2 = PWM(Pin(20, Pin.OUT), duty_u16=1000, freq=100)
            led2.duty_u16(1000)
            time.sleep(0.1)
            led2.duty_u16(0)
            ####
        else:
            pass

        
        ####### DBUG
        print(value, self.min_val, self.max_val)
        oled.fill_rect(0, 53, 42, 128, 0)
        oled.text(str(value), 0, 55, 1)
        
        ####### DBUG
            
        return
    
    def process_data(self, data_feed):
        if self.max_val == self.min_val:
            self.min_val -= 1
        
        ### y = mx + b, bc the realtion between data scale and display resolution is 
        m = -55 / (self.max_val - self.min_val)
        b = self.screen_ceil - m * self.max_val
        
        upd_x = self.point_x + self.step_x
        ### upd_y = int((-0.0055) * data_feed + 97.5)
        
        ### upd_y is a math function to define the borders of the screen
        ### so, the graph will always be inside the borders.
        upd_y = int(m * data_feed + b)
        
        self.upd_minmax(data_feed) ### try to use upd_y to define min/max
        
        oled.vline(upd_x, 0, 64, 0)
        oled.line(self.point_x, self.point_y, upd_x, upd_y, 1)
        
        ### set current x, y to updated values
        self.point_x = upd_x
        self.point_y = upd_y
        
        # wrapping on x for both directions
        if self.point_x >= 127:
            self.point_x = 0
        elif self.point_x < 0:
            self.point_x = 127
        oled.show()
        return
    
    def execute(self, feed):
        ### check butts
        if self.pin_clear.value() == 0:
            self.clear()
        elif self.pin_swap.value() == 0:
            time.sleep(0.05)
            if self.pin_swap.value() == 0: 
                self.swap_dir()
        else:
            ### main function
            self.process_data(feed)
        
        time.sleep(0.05)
        return
    
    def clear(self):
        '''
        Called when the 'clear' button is pressed.
        Clears the screen and resets the graph to 'stock' values(stock vals are hardcoded).
        '''
        self.max_val = 0
        self.min_val = 65535
        
        if self.pin_clear.value() == 0:
            oled.fill_rect(0, 53, 42, 128, 0)
            oled.text("CLEAR", 0, 55, 1)
            oled.show()
            
            time.sleep(1)
            
            if self.pin_clear.value() == 0:
                
                for i in range(oled_width + 1):
                    oled.vline(i, 0, 64, 1)
                    oled.vline(i - 1, 0, 64, 0)
                    oled.show()
                time.sleep(0.4)
                
                self.point_x = 0
                self.point_y = 32
        return
    
    def swap_dir(self):
        '''
        Called when the swap_pin is pressed.
        Negates the self.step_x, so the graph will progress in reversed direction.
        '''
        self.step_x = -(self.step_x)
        oled.fill_rect(0, 53, 75, 128, 0)
        for i in range(4):
            if i % 2 == 0:
                oled.fill_rect(0, 53, 58, 128, 0)
                oled.text("DIRECTION", 0, 55, 1)
                oled.show()
            else:
                oled.fill_rect(0, 53, 75, 128, 0)
                oled.text("SWAP", 0, 55, 1)
                oled.show()
            time.sleep(0.7)
        return


Button = Pin(9, mode=Pin.IN, pull=Pin.PULL_UP)

def interrupt_handler(pin):
    global _exec_
    _exec_ = False
    return

Button.irq(handler = interrupt_handler, trigger = Button.IRQ_FALLING, hard = True)

_exec_ = True


flatline = Line()
while True:
    peak = data.get()
    #peak = sensor.read_u16()
    if _exec_:
        flatline.execute(peak)
    else:
        print("CHECK LOGS")
        oled.fill(0)
        time.sleep(5)
        oled.fill(1)


