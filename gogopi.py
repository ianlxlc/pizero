#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
#from waveshare_epd import epd2in13_V2
from epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import socket
import json

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V2 Demo")
    
    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    print("epd.init done")
    epd.Clear(0xFF)
    
    # Drawing on the image
    print("picdir = ", picdir)
    #font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    #font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font15 = ImageFont.truetype(os.path.join(picdir, 'DejaVuSans.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'sss.ttf'), 24)
    
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    dimension = "H: " + str(epd.height) + " " + "W: " + str( epd.width)

    # routes = json.loads(os.popen("ip -j -4 route").read()
    ip_val = "Not Found"
    routes = json.loads(os.popen("ip -j -4 route").read())
    for r in routes:
        if r.get("dev") == "wlan0" and r.get("prefsrc"):
            ip_val = r['prefsrc']
            continue

    # hostname = socket.gethostname()
    # ip_val = socket.gethostbyname(hostname)
    ip_disp = "IP : " + ip_val
    # draw.rectangle([(0,0),(50,50)],outline = 0)
    # draw.rectangle([(0,0),(50,50)],outline = 0)
    draw.text((0, 0), dimension, font = font15, fill = 0)
    draw.text((0, 30), ip_disp, font = font15, fill = 0)
    draw.text((120, 60), 'ALOHA!!', font = font15, fill = 0)
    #draw.text((120, 60), 'e-Paper demo', font = font15, fill = 0)
    draw.text((110, 90), u'你是小叮当', font = font24, fill = 0)
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
