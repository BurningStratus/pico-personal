from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

'''
oled.pixel(x,y,c):
Draw a pixel at position x,y and uses c to set the color of the pixel, with 1 being lit, 0 being off. Example:
oled.pixel(10,10,1)


oled.hline(x,y,w,c):
Draw a horizontal line from point x,y that has a set width (w) in pixels, and color ( c ). Example: 
oled.hline(2,3,4,1)


oled.vline(x,y,h,c):
Draw a vertical line from point x,y that has a set height (h) in pixels, and color ( c ). Example:
oled.vline(0, 0, 64, 1)

oled.line(x1,y1,x2,y2,1):
Draw a diagonal line from points x1, y1 to x2, y2 with the color ( c ). Example:
oled.line(0, 0, 128, 64, 1)

oled.rect(x,y,w,h,c):
Draw a rectangle starting at point x.y and for a set width (w) and height(h).
Use ( c ) to set the color of the pixels. For example:
oled.rect(0, 0, 64, 32, 1)

oled.fill_rect(x,y,w,h,c):
Draw a filled rectangle starting at point x.y and
for a set width (w) and height(h) use ( c ) to set the color of the pixels. For example:
oled.fill_rect(0, 0, 64, 32, 1)

'''
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

gpio10 = Pin(10, Pin.IN)
#gpio11 = Pin(11, Pin.IN)


def pix(x, y, c=1):
    oled.pixel(x, y, c)
    return str(x) + ":" + str(y)

def hline(x, y, w=1, c=1):
    oled.hline(x, y, w, c)
    return str(x) + ":" + str(y) + "C" + ":" + str(c)

def vline(x, y, h, c=1):
    oled.vline(x, y, h, c)
    return str(x) + ":" + str(y) + "C" + ":" + str(c)

def line(x, y, x1, y1, c = 1):
    oled.line(x, y, x1, y1, c)
    return str(x) + ":" + str(y)


menu = {
    1: "ok",
    2: "bruh",
    3: "dang it"
    }

def show_menu():
    oled.text("ok", 4, 10)
    oled.text("bruh", 4, 30)
    oled.text("dang it", 4, 50)
    oled.show()
    return

def knob(pin):
    return

show_menu()
oled.show()

while True:
    time.sleep(0.5)
#    print(gpio12.value())
    print(gpio10.value())


