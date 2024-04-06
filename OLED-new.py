# OLED
import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

std0 = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)
std1 = Pin(9, mode=Pin.IN, pull=Pin.PULL_UP)


class Symbol:
    def __init__(self, input1, input2):
        ### Starting position coordinates.
        self.position_x = 50
        self.position_y = 55
        ### Borders
        self.border_x = 127
        self.border_y = 63
        ###
        self.symbol = "<=>"
        ### Movement step
        self.step = 2
        '''
        Movement step defines how many pixels will be skipped on button press.
        '''
        ### Inputs >
        self.in_1 = input1
        self.in_2 = input2
    
    def execute(self):
        self.printer()
        self.check_border()
        self.check_input()
    
    def printer(self):
        oled.fill(0)
        oled.text(self.symbol, self.position_x, self.position_y, 1)
        oled.show()
        return
        
    def check_border(self):
        if self.position_x >= self.border_x or self.position_x <= 0 or self.position_y >= self.border_y or self.position_y >= 0:
            if self.position_x > 105:
                self.position_x = 105
            elif self.position_x < 0:
                self.position_x = 0
        else:
            print("BORDERS OK")
        return
    
    def check_input(self):
        print("CHECKING INPUT")
        print(self.in_1, self.in_2)
        self.in_1 = std0.value()
        self.in_2 = std1.value()
        
        if self.in_1 == 0:
            self.move_R()
        elif self.in_2 == 0:
            self.move_L()
        
        return
    
    def move_R(self):
        self.position_x += self.step
        
        self.check_border()
        
        print(self.position_x, self.position_y)
        return
    
    def move_L(self):
        self.position_x -= self.step
        
        self.check_border()
        
        print(self.position_x, self.position_y)
        return

ufo = Symbol(std0, std1)

while True:
    ufo.execute()
    time.sleep(0.05)
    