#!/usr/bin/env python3

# interval timer from https://stackoverflow.com/questions/22498038#22498708
from threading import Event, Thread
def repeat(interval, func):
	def loop():
		while not Event().wait(interval):
			func()
	Thread(target=loop).start()


# uses https://raw.githubusercontent.com/tomstokes/python-spi/master/spi.py
from spi import SPI

spi = SPI('/dev/spidev1.0')
spi.mode = SPI.MODE_0
spi.bits_per_word = 8
spi.speed = 10 * 1000000

IODIRA = 0x00
IOCON = 0x0a
GPIOA = 0x12

# write to MCP23S17 register(s), GPIOA by default
def mcp23s17(address, values, register=GPIOA):
	global spi
	opcode = 0x40 | (address << 1)
	spi.write([opcode, register] + values)

# configure up to 5 MCP23S17
for address in range(5):
	# set Byte mode (SEQOP=1) with BANK=0 and HAEN=1
	# this makes it so that values for both ports can
	# be written at once to reduce overhead
	mcp23s17(address, [0x28], register=IOCON)

	# make all GPA and GPB pins outputs
	mcp23s17(address, [0x00, 0x00], register=IODIRA)


# now blink some LEDs

data = [0x00, 0x00]

# toggle 10101010 10101010 pattern (0xaa 0xaa) on MCP23S17 with address 0
def output():
	global data
	data[0] ^= 0xaa
	data[1] ^= 0xaa
	mcp23s17(0, data)

# output every 100ms
repeat(0.1, output)
