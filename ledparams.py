import wiringpi as wiringpi
from time import sleep

ic1_pin_base = 101


ic1_i2c_addr = 0x20


# initiate the wiringpi library
wiringpi.wiringPiSetup()
# enable ic1 on the mcp23017 hat
wiringpi.mcp23017Setup(ic1_pin_base,ic1_i2c_addr)


pins = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

def setup():
	for pin in pins:
		wiringpi.pinMode((pin+100),1)
def clear():
	for pin in pins:
		wiringpi.digitalWrite((pin+100),0)


setup()
