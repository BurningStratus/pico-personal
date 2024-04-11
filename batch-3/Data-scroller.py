import time
from machine import Pin, PWM, UART, I2C, Timer, ADC
from fifo import Fifo
from filefifo import Filefifo
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

import micropython
micropython.alloc_emergency_exception_buf(200)


class Encoder:
	def __init__(self, rot_a, rot_b, intrrpt):
		self.a = Pin(
		     rot_a, 
		     mode = Pin.IN, 
		     pull = Pin.PULL_UP
		)
		self.b = Pin(
		     rot_b, 
		     mode = Pin.IN, 
		     pull = Pin.PULL_UP
		)
		self.fifo = Fifo(30, typecode = 'i')
		self.a.irq(
		     handler = self.handler, 
		     trigger = Pin.IRQ_RISING, 
		     hard = True
		)

		self.interrupt = Pin(intrrpt, 
		     mode = Pin.IN, 
		     pull = Pin.PULL_UP
		)
		
		self.interrupt.irq(
		     handler = self.interrupt_handler,
		     trigger = self.interrupt.IRQ_FALLING, 
		     hard = True
		)
		self.condition = False	
		self.last_stamp = 0
		
	def interrupt_handler(self, pin):
		if not self.interrupt.value() and not self.condition:
					
			if time.ticks_ms() - self.last_stamp < 55:
				self.condition = False 
			else:
				self.condition = True 
		else:
			self.condition = False

		self.last_stamp = time.ticks_ms()

		return self.condition
	
	def handler(self, pin):
		if self.fifo.has_data():
			self.fifo.get()
		else:
			pass
		
		if self.b():
			self.fifo.put(1)
		else:
			self.fifo.put(-1)
		return

class DataHandler:
	def __init__(self, rot_entity):
		self.min = 65535
		self.max = 0
		self.curr_pos = 0
		self.curr_rec = 0
		self.rotary = rot_entity
	
	def check_min_max(self, data: list):		
		if not data:
			print("No data found.")
			return
		if data > self.max:
			self.max = data
		else:
			pass
		
		if data < self.min:
			self.min = data
		else:
			pass
		
		return
	
	def scroller(self, data):
		if self.rotary.fifo.has_data():

			x = self.rotary.get()
			if x > 0:
				self.position += 10
				self.add_to_buf(data.get())
		else:
			pass
		return
	
	def add_to_buf(self, data):
		# oled.text(str(data), 2, self.curr_pos, 1)
		
		print(self.curr_pos)	

		if self.curr_pos % 6 == 0 and self.curr_pos > 30:
			self.curr_pos -= 10
			oled.scroll(0, -10)
			oled.fill_rect(0, 50, 128, 70, 0)
		
		oled.text(str(data), 2, self.curr_pos, 1)
		oled.show()
		
		self.curr_pos += 10
		self.curr_rec += 1
		return


rot = Encoder(10, 11, 12)
data= Filefifo(10, name = 'capture_250Hz_01.txt')
data_handler = DataHandler(rot)
for i in range(250):
	data_handler.check_min_max(data.get())

print("__")
while True:
	data_peaks = data.get()
	data_handler.add_to_buf(data_peaks)
	time.sleep(0.5)
	
