import gc
import os
import inky_frame
import jpegdec
import sdcard
from random import choice
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY
from machine import Pin, SPI

gc.collect()

# variables
dir_path        = r'sd/'
update_interval = 10 # minutes
photos          = []

# set up the display
graphics = PicoGraphics(DISPLAY)
gc.collect()

# set up the SD card
sd_spi = SPI(0, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT), miso=Pin(16, Pin.OUT))
sd = sdcard.SDCard(sd_spi, Pin(22))
os.mount(sd, "/sd")
gc.collect()

# create a new JPEG decoder for our PicoGraphics
j = jpegdec.JPEG(graphics)
gc.collect()

# function to display an image
def display_image(filename):
  j.open_file(filename)
  j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
  graphics.update()

# count and choose a photo to display
for file in os.listdir(dir_path):
  if not file.startswith(".") and file.endswith(".jpg"):
    photos.append(file)

while True:
  # display image
  display_image("sd/" + choice(photos))

  # go to sleep and wake up after "update_interval" minutes
  inky_frame.sleep_for(update_interval)
  print("ZzzzZzz going to sleep")
