from machine import Pin
from time import sleep

inbutt = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP) 
d2 = Pin(20, Pin.OUT)
d1 = Pin(21, Pin.OUT)
d0 = Pin(22, Pin.OUT)

current_num = 0
leds = [d0, d1, d2]
numToBit = {
    0: [],
    1: [d0],
    2: [d1],
    3: [d0, d1],
    4: [d2],
    5: [d2, d0],
    6: [d2, d1],
    7: [d2, d1, d0]
    }

while True:
    sleep(0.5)
    if inbutt.value() != 1:
        if current_num < 7:
            current_num += 1
        else:
            current_num = 0
        
        for i in leds:
            if i in numToBit[current_num]:
                i.on()
            else:
                i.off()
        
        