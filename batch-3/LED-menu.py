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

class Cursor:
	def __init__(self, rot_entity, pos_indx=1):
		self.indx = pos_indx
		self.position = 10 
		
		### basic cursor
		self.cursor = "}"	
		
		### LED1
		self.LED1 = PWM(
		    Pin(22, Pin.OUT), 
		    freq = 100, 
		    duty_u16=0
		)
		### LED2
		self.LED2 = PWM(
		    Pin(21, Pin.OUT), 
		    freq = 100, 
		    duty_u16=0
		)
		### LED3
		self.LED3 = PWM(
		    Pin(20, Pin.OUT), 
		    freq = 100, 
		    duty_u16=0
		)
		self.rot_entity = rot_entity	
		self.LED1_state = False
		self.LED2_state = False
		self.LED3_state = False
		
		self.led_basic_on = "OK"
		self.led_basic_off= "NAH"	
	
	def led_states(self):

		oled.fill_rect(55, 0, 128, 64, 0)	
		
		if self.LED1_state:
			self.LED1.duty_u16(1000)
			oled.text(self.led_basic_on, 55, 10)
		else:
			self.LED1.duty_u16(0)
			oled.text(self.led_basic_off, 55, 10)
		if self.LED2_state:
			self.LED2.duty_u16(1000)
			oled.text(self.led_basic_on, 55, 28)
		else:
			self.LED2.duty_u16(0)
			oled.text(self.led_basic_off, 55, 28)
		if self.LED3_state:
			self.LED3.duty_u16(1000)
			oled.text(self.led_basic_on, 55, 46)
		else:
			self.LED3.duty_u16(0)
			oled.text(self.led_basic_off, 55, 46)
		# oled.show()
		return

	def show_cursor(self):
		oled.fill_rect(0, 0, 10, 63, 0)
		oled.text(self.cursor, 2, self.position, 1)
		oled.show()	
		return
		
	def menu_controller(self, feed):
		oled.text("LED 1", 10 ,10)	
		oled.text("LED 2", 10, 28)
		oled.text("LED 3", 10, 46)
		
		self.led_states()	
		encoder_butt = self.rot_entity.interrupt_handler("STRING")
		time.sleep(0.005)	
		if encoder_butt:
			if self.indx == 1:
				self.LED1_state = not self.LED1_state
			elif self.indx == 2:
				self.LED2_state = not self.LED2_state
			elif self.indx == 3:
				self.LED3_state = not self.LED3_state
		
		oled.show()
		return
	
	def move_cursor(self, rot_entity):
		
		if rot_entity.fifo.has_data():
			self.indx += rot_entity.fifo.get()
			if self.indx > 3:
				self.indx = 3
			elif self.indx < 1:
				self.indx = 1

		#if data > 0 and self.indx < 3:
		#	self.indx += 1
		#elif data < 0 and self.indx > 0:
		#	self.indx -= 1
		
		
		if self.indx == 1:
			self.position = 10
		elif self.indx == 2:
			self.position = 28
		elif self.indx == 3:
			self.position = 46
		return	
	


rot = Encoder(10, 11, 12)
curs= Cursor(rot)

print("__")
while True:
	
	curs.menu_controller("STRING")
	# curs.show_cursor()
	curs.move_cursor(rot)
	curs.show_cursor()
	
