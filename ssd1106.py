
# SSD1106 I2C 128*64

# The MIT License (MIT)
#
# Copyright (c) 2014 Kenneth Henderick
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import machine
import time
import framebuf

# Constants
DISPLAYOFF          = 0xAE
SETCONTRAST         = 0x81
DISPLAYALLON_RESUME = 0xA4
DISPLAYALLON        = 0xA5
NORMALDISPLAY       = 0xA6
INVERTDISPLAY       = 0xA7
DISPLAYON           = 0xAF
SETDISPLAYOFFSET    = 0xD3
SETCOMPINS          = 0xDA
SETVCOMDETECT       = 0xDB
SETDISPLAYCLOCKDIV  = 0xD5
SETPRECHARGE        = 0xD9
SETMULTIPLEX        = 0xA8
SETLOWCOLUMN        = 0x00
SETHIGHCOLUMN       = 0x10
SETSTARTLINE        = 0x40
MEMORYMODE          = 0x20
COLUMNADDR          = 0x21
PAGEADDR            = 0x22
COMSCANINC          = 0xC0
COMSCANDEC          = 0xC8
SEGREMAP            = 0xA0
CHARGEPUMP          = 0x8D
EXTERNALVCC         = 0x10
SWITCHCAPVCC        = 0x20
SETPAGEADDR         = 0xB0
SETCOLADDR_LOW      = 0x00
SETCOLADDR_HIGH     = 0x10
ACTIVATE_SCROLL                      = 0x2F
DEACTIVATE_SCROLL                    = 0x2E
SET_VERTICAL_SCROLL_AREA             = 0xA3
RIGHT_HORIZONTAL_SCROLL              = 0x26
LEFT_HORIZONTAL_SCROLL               = 0x27
VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
VERTICAL_AND_LEFT_HORIZONTAL_SCROLL  = 0x2A
SETSEGMENTREMAP = 0xA1


# I2C devices are accessed through a Device ID. This is a 7-bit
# value but is sometimes expressed left-shifted by 1 as an 8-bit value.
# A pin on SSD1106 allows it to respond to ID 0x3C or 0x3D. The board
# I bought from ebay used a 0-ohm resistor to select between "0x78"
# (0x3c << 1) or "0x7a" (0x3d << 1). The default was set to "0x78"
DEVID = 0x3c

# I2C communication here is either <DEVID> <CTL_CMD> <command byte>
# or <DEVID> <CTL_DAT> <display buffer bytes> <> <> <> <>...
# These two values encode the Co (Continuation) bit as b7 and the
# D/C# (Data/Command Selection) bit as b6.
CTL_CMD = 0x00
CTL_DAT = 0x40

class SSD1106:

  def __init__(self, pin_scl=machine.Pin(22), pin_sda=machine.Pin(21), height=32, external_vcc=True, i2c_devid=DEVID):
    self.pin_scl = pin_scl
    self.pin_sda = pin_sda
    self.external_vcc = external_vcc
    self.height       = 32 if height == 32 else 64
    self.pages        = int(self.height / 8)
    self.columns      = 128

    self.i2c = machine.SoftI2C(scl=self.pin_scl, sda=self.pin_sda, freq=400000)
    self.devid = i2c_devid
    # used to reserve an extra byte in the image buffer AND as a way to
    # infer the interface type
    # I2C command buffer
    self.cbuffer = bytearray(2)
    self.cbuffer[0] = CTL_CMD
    
    self.temp = bytearray(2)
    self.widthh = 128
    self.heightt = 64
    self.pagess = self.heightt // 8
    self.bufferr = bytearray(self.pagess * self.widthh)
    self.framebuf = framebuf.FrameBuffer(self.bufferr, self.widthh, self.heightt, framebuf.MVLSB)
   
    self.poweron()
    self.init_display()


#########    
  def text(self, string, x, y, col=1):
    self.framebuf.text(string, x, y, col)
  def fill(self, col):
    self.framebuf.fill(col)
  def pixel(self, x, y, col):
    self.framebuf.pixel(x, y, col)
  def scroll(self, dx, dy):
    self.framebuf.scroll(dx, dy)
  def text(self, string, x, y, col=1):
    self.framebuf.text(string, x, y, col)
  def hline(self, x, y, w, col):
    self.framebuf.hline(x, y, w, col)
  def vline(self, x, y, h, col):
    self.framebuf.vline(x, y, h, col)
  def line(self, x1, y1, x2, y2, col):
    self.framebuf.line(x1, y1, x2, y2, col)
  def rect(self, x, y, w, h, col):
    self.framebuf.rect(x, y, w, h, col)
  def fill_rect(self, x, y, w, h, col):
    self.framebuf.fill_rect(x, y, w, h, col)
  def blit(self, fbuf, x, y):
    self.framebuf.blit(fbuf, x, y)
 
  def write_data(self, buf):
    self.temp[0] = self.devid << 1
    self.temp[1] = 0x40 # Co=0, D/C#=1
    self.i2c.writeto(self.devid, self.temp)
    self.i2c.writeto(self.devid, self.bufferr)
    #print("self.temp = ", self.temp)
    #print("self.bufferr = ", self.bufferr)
 
  def show(self):
    self.write_data(self.bufferr)
#########

 
  def clear(self):
    self.buffer = bytearray(self.pages * self.columns)
    #if self.offset == 1:
      #self.buffer[0] = CTL_DAT

  def write_command(self, command_byte):
    self.cbuffer[1] = command_byte
    self.i2c.writeto(self.devid, self.cbuffer)

  def invert_display(self, invert):
    self.write_command(INVERTDISPLAY if invert else NORMALDISPLAY)

  def display(self):
    index = 0
    prefix_buffer = bytearray(1)
    prefix_buffer[0] = CTL_DAT
    for page in range(0, 8):
      self.write_command(0xB0 + page)
      self.write_command(0x02)

      self.write_command(0x10)
      for line in range(0, 8):
        self.i2c.writeto(self.devid, prefix_buffer + self.bufferr[index:index + 16])
        index += 16

  def set_pixel(self, x, y, state):
    index = x + (int(y / 8) * self.columns)
    if state:
      self.buffer[index] |= (1 << (y & 7))
    else:
      self.buffer[index] &= ~(1 << (y & 7))

  def init_display(self):
    chargepump = 0x10 if self.external_vcc else 0x14
    precharge  = 0x22 if self.external_vcc else 0xf1
    multiplex  = 0x1f if self.height == 32 else 0x3f
    compins    = 0x02 if self.height == 32 else 0x12
    contrast   = 0xcf # 0x8f if self.height == 32 else (0x9f if self.external_vcc else 0x9f)
    data = [DISPLAYOFF,
            MEMORYMODE,
            SETHIGHCOLUMN, 0xB0, 0xC8,
            SETLOWCOLUMN, 0x10, 0x40,
            SETCONTRAST, 0x7F,
            SETSEGMENTREMAP,
            NORMALDISPLAY,
            SETMULTIPLEX, 0x3F,
            DISPLAYALLON_RESUME,
            SETDISPLAYOFFSET, 0x00,
            SETDISPLAYCLOCKDIV, 0xF0,
            SETPRECHARGE, 0x22,
            SETCOMPINS, 0x12,
            SETVCOMDETECT, 0x20,
            CHARGEPUMP, 0x14,
            DISPLAYON]
    for item in data:
      self.write_command(item)


    self.clear()
    self.display()

  def poweron(self):
    time.sleep_ms(10)

  def poweroff(self):
    self.write_command(DISPLAYOFF)

  def contrast(self, contrast):
    self.write_command(SETCONTRAST)
    self.write_command(contrast)

