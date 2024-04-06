import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

std0 = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)
std1 = Pin(9, mode=Pin.IN, pull=Pin.PULL_UP)

pos = 0
row = -10

while True:
    string = input("~input$> ")
    
    if row >= 55:
        row = 55
        pos = -11
    else:
        row += 11
    
    oled.scroll(0, pos)
    oled.fill_rect(0, 55, 127, 66, 0)
    oled.text(string, 0, row, 1)
    print(row, pos)
    oled.show()
