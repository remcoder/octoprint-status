#!/usr/bin/env python3

import sys, os, time, datetime, urllib
import socket
import yaml

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import pcd8544, st7735, uc1701x
import PIL

serial = spi(port=0, device=0, gpio_DC=23, gpio_RST=24, bus_speed_hz=32000000)
device = st7735(serial)

from PIL import Image

# read octoprint config
with open("/home/pi/.octoprint/config.yaml", 'r') as stream:
    try:
        obj = yaml.safe_load(stream)
        server_settings = obj['server']
        port = server_settings.get('port', 5000)
        # print("port:", port) 
    except yaml.YAMLError as exc:
        print(exc)

# get ip address
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# ip = s.getsockname()[0]
# s.close()

#address = ip + ":" +  str(port)
address = "TEMP" + ":" +  str(port)
print("octoprint: " + address)

def status():
  x = 0
  while True:
    with canvas(device) as draw:
        now = datetime.datetime.now()
        formatted_time = now.strftime("%H:%M:%S")
        draw.rectangle(device.bounding_box, fill="black")
        draw.text((x, 0), "Octopi", fill="red")
        draw.text((30, 20), address, fill="white")
        draw.text((30, 40), formatted_time, fill="blue")
    x += 1
    if x > 160:
      x = 0


img = Image.open("octoprint-logo.png")

def bouncingOcto():
  print("logo", img.width, img.height)
  resized = img.resize((int(device.width/2), int(device.height/2))).convert("RGB")
  print("resized", resized.width, resized.height)

  background = Image.new("RGB", device.size, "black")
  eraser = Image.new("RGB", (1,device.size[0]), "black")

  y = 0
  x = 0
  while True:
      with canvas(device) as draw:
        # draw.bitmap((x,y), resized, "black")
        
        # background.paste(resized, (x,y))
        # background.paste(eraser, (x-1,y))
        # converted = background.convert(device.mode)
        # device.display(converted)
        # time.sleep(0.1)
        x += 1
        if x > device.width-resized.width:
          x = 0

def rotatingOcto():
  logo = img.convert("RGBA")
  fff = Image.new(logo.mode, logo.size, (255,) * 4)

  background = Image.new("RGBA", device.size, "white")
  pos = ((device.width - logo.width) // 2, 0)

  while True:
      for angle in range(0, 360, 2):
          rot = logo.rotate(angle, resample=Image.BILINEAR)
          buffer = Image.composite(rot, fff, rot)
          background.paste(buffer, pos)
          device.display(background.convert(device.mode))

rotatingOcto()
