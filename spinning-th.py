
import time
from machine import Pin, PWM, UART, I2C, Timer, ADC
from fifo import Fifo
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

import micropython
micropython.alloc_emergency_exception_buf(200)

class Daemon:
	def __init__(self, pin):
		self.interrupt_pin = Pin(pin, mode = Pin.IN)
		self.runner = False 
		print("runner alloc")
		
		self.interrupt_pin.irq(
		    handler = self.handler_, 
		    trigger = Pin.IRQ_FALLING, 
		    hard = True
		)
	
	def handler_(self, pin):
		print("INTERRUPTED", pin)
		self.spinning_th
		return

	def spinning_th(x=0, y=55, time_sec=0.05):
	
		def fill_r():
			time.sleep(time_sec)
			oled.fill_rect(x, y, x + 10, y + 10, 0)
			return
	
	# fill_r = oled.fill_rect(0, 55, 10, 63, 0)
	
		fill_r()	
		oled.text("/", x, y)
		oled.show()
		########## --
		fill_r()
		oled.text("-", x, y)
		oled.show()
		########## \
		fill_r()
		oled.text("\\", x, y)
		oled.show()
		##########
		fill_r()
		oled.text("|", x, y)
		oled.show()
		##########
		fill_r()
		oled.text("/", x, y)
		oled.show()
		##########
		fill_r()
		oled.text("-", x, y)
		oled.show()
		##########
		fill_r()
		oled.text("\\", x, y)
		oled.show()
		##########
		fill_r()
		oled.text("|", x, y)
		oled.show()
	
		return
print("__")
daemon = Daemon(2)

while True:
	#spinning_th()
	oled.text("sending nudes", 10, 55)	
	#spinning_th(x=115, y=55, time_sec=0.05)
	oled.show()
	
