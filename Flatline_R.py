import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)


class Line:
    def __init__(self):
        ### buttons
        self.pin_up = Pin(9, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pin_down = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pin_clear = Pin(8, mode=Pin.IN, pull=Pin.PULL_UP)
        self.pin_swap = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP) #swap == change direction.
        
        ### starting position
        self.point_y = 32
        self.point_x = 0
        
        ### step for the graph
        self.step_x = 1
        self.step = 1
        
    def execute(self):
        ### check butts
        if self.pin_up.value() == 0:
            self.plot_up()
        elif self.pin_down.value() == 0:
            self.plot_down()
        elif self.pin_clear.value() == 0:
            self.clear()
        elif self.pin_swap.value() == 0:
            self.swap_dir()
        else:
            self.plot()
        
        time.sleep(0.07)
        
        # wrapping on x
        if self.point_x >= 127:
            self.point_x = 0
        elif self.point_x < 0:
            self.point_x = 127
        # wrapping on y
        if self.point_y <= 0:
            self.point_y = 63
        elif self.point_y >= 63:
            self.point_y = 0
            
        oled.show()
    
    def plot(self):
        '''
        This function is called when there is no input,
        so it draws a straight line on current y axle
        '''
        upd_x = self.point_x + self.step_x
        oled.line(self.point_x, self.point_y, upd_x, self.point_y, 1)
        self.point_x = upd_x
    
    def plot_up(self):
        '''
        Called when the 'up' button is pressed.
        Updates xy-coordinate with self.step(for y) and self.step_x(for x)
        '''
        upd_x = self.point_x + self.step_x
        upd_y = self.point_y + self.step
        
        oled.line(self.point_x, self.point_y, upd_x, upd_y, 1)
        
        self.point_x = upd_x
        self.point_y = upd_y
        return
    
    def plot_down(self):
        '''
        Called when the 'down' button is pressed.
        Updates xy-coordinate with negative self.step(for y) and self.step_x(for x)
        '''
        upd_x = self.point_x + self.step_x
        upd_y = self.point_y - self.step
        
        oled.line(self.point_x, self.point_y, upd_x, upd_y, 1)
        
        self.point_x = upd_x
        self.point_y = upd_y
        return
    
    def clear(self):
        '''
        Called when the 'clear' button is pressed.
        Clears the screen and resets the graph to 'stock' values(stock vals are hardcoded).
        '''
        oled.fill(0)
        self.point_x = 0
        self.point_y = 32
        return
    
    def swap_dir(self):
        '''
        Called when the swap_pin is pressed.
        Negates the self.step_x, so the graph will progress in reversed direction.
        '''
        self.step_x = -(self.step_x)
        print("direction changed")
        return

line = Line()

while True:
    line.execute()