### rotary
from time import sleep
from machine import Pin, PWM
from fifo import Fifo

import micropython
micropython.alloc_emergency_exception_buf(200)

print("__")

class Encoder:
    def __init__(self, rot_a, rot_b, intrrpt):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
        self.led = PWM(Pin(20, Pin.OUT), freq=140, duty_u16=0)
        self.condition = False 

        self.analog = 0
        
        self.interrupt = Pin(intrrpt, mode = Pin.IN, pull = Pin.PULL_UP)
        self.interrupt.irq(handler = self.interrupt_handler, trigger = self.interrupt.IRQ_RISING, hard = True)
        
    def bounce_filter(self):
	

	if self.condition:
		sleep(0.05)
		if self.condition:
			return True	
		else:
			return False
	else:
		return False
	
    def interrupt_handler(self, pin):
	self.condition = not self.condition
	
        return
    
    def handler(self, pin):      
        if self.fifo.has_data():
            self.fifo.get()
        elif self.fifo.empty():
            pass
        
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)
        return
    
    def rotary_handler(self):
        if self.fifo.has_data():
            x = self.fifo.get()

            if self.condition:
                if x == 1 and self.analog < 1000:
                    self.analog += 100
                elif x == -1 and self.analog > 100:
                    self.analog -= 100
            else:
                pass

        return
    
    def led_condition(self):
        if self.condition and self.bounce_filter():
            self.led.duty_u16(self.analog)
        elif not self.condition and not self.bounce_filter():
            self.led.duty_u16(0)
        return
        
    

# Button.irq(handler = interrupt_handler, trigger = Button.IRQ_FALLING, hard = True)

    
rot = Encoder(10, 11, 12)
led = PWM(Pin(20, Pin.OUT), duty_u16=0, freq=100)

while True:
    rot.rotary_handler()
    rot.led_condition()
    
