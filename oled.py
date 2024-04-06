import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

button = Pin(9, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

x = 0
y = 0
color = 1

def pix_shift(x_curr, y_curr):
    
    x_curr = x_curr + 1
    # y_new = y_curr + 1
    
    if x_curr == 127:
        y_curr += 1
        x_curr = 0
    if y_curr >= 63:
        y_curr = 0
        if color == 1:
            color = 0
        else:
            color = 1
    
    return [x_curr, y_curr]

def pix_control(x_new, y_new, color_int):
    if color_int == 1:
        oled.pixel(x_new, y_new, 1)
    else:
        oled.pixel(x_new, y_new, 0)
    oled.show()

while True:
    pix_control(x, y, color)
    coords = pix_shift(x, y)
    print(coords)
    x = coords[0]
    y = coords[1]
    
    