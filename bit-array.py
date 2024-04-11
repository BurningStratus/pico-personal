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


def bit_screen():
	pos_x = 0
	pos_y = 0
	from random import randint
	oled.fill(0)
	for i in range(98):	
		oled.text(str(randint(0, 1)), pos_x, pos_y)
		pos_x += 9
		if pos_x == 126:
			pos_x = 0
			pos_y += 9
	oled.show()
	return

def bit_clear():

	pos_x = 0
	pos_y = 0
	for i in range(0, 126, 9):
		for ii in range(0, 63, 9):
			oled.fill_rect(i, ii, i + 9, ii + 9, 0)
			oled.text(str(1), i, ii)
		oled.show()		
		time.sleep(0.1)
		pos_x += 9
	
	time.sleep(2)
	for x in range(129):
		oled.hline(0, x, 128, 1)
		oled.hline(0, x - 1, 128, 0)
		#oled.vline(x, 0, 63, 1)
		#oled.vline(x-1, 0, 63, 0)
		oled.show()				
	return	
	

for i in range(50):
	time.sleep(0.05)
	bit_screen()

bit_clear()
