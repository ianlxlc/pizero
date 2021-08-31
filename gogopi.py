#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
fntdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
#from waveshare_epd import epd2in13_V2
from epd import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from datetime import datetime
import pytz
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

    heading_type_1 = ImageFont.truetype(os.path.join(fntdir, 'Nexa Bold.otf'), 15)
    heading_type_2 = ImageFont.truetype(os.path.join(fntdir, 'Nexa Light.otf'), 12)
    heading_type_3 = ImageFont.truetype(os.path.join(fntdir, 'digitmono.ttf'), 10)
    
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    dimension = "H: " + str(epd.height) + " " + "W: " + str( epd.width)

    # get wifi ip address
    ip_val = "Not Found"
    routes = json.loads(os.popen("ip -j -4 route").read())
    for r in routes:
        if r.get("dev") == "wlan0" and r.get("prefsrc"):
            ip_val = r['prefsrc']
            continue

    # get local time    
    tz_LA = pytz.timezone('America/Los_Angeles') 
    datetime_LA = datetime.now(tz_LA)
    time_only = datetime_LA.strftime("%H:%M:%S")
    time_disp = "Seattle time:" + time_only

    # print("Seattle time:", datetime_LA.strftime("%H:%M:%S"))

    # hostname = socket.gethostname()
    # ip_val = socket.gethostbyname(hostname)
    ip_disp = "IP : " + ip_val
    # draw.rectangle([(0,0),(50,50)],outline = 0)
    # draw.rectangle([(0,0),(50,50)],outline = 0)

    # 背景斜线
    # (right, down)
    i = -122
    while(i<=250):
        start_r = i
        start_d = -1
        end_r = 122+i
        end_d = 122

        draw.line([(start_r,start_d),(end_r,end_d)], fill = 0,width = 2)

        i += 10

    width = 122
    height = 250
    draw.rectangle([(14,6),(height-6,width-14)],outline = 0,fill = 200)
    draw.rectangle([(6,14),(height-14,width-6)],outline = 0,fill = 255)

    ref_r = 6
    ref_d = 14

    ref_width = width - 20
    ref_height = height - 20


    # font15 = ImageFont.truetype(os.path.join(picdir, 'DejaVuSans.ttc'), 15)
    draw.text((ref_r+10, ref_d+10), 'PINK', font = heading_type_1, fill = 0)
    draw.rectangle([(ref_r+10, ref_d+15),(height-15,width-7)],fill = 255)
    draw.text((ref_r+10, ref_d+15), 'PINK', font = heading_type_1, fill = 0)
    draw.rectangle([(ref_r+10, ref_d+20),(height-15,width-7)],fill = 255)
    draw.text((ref_r+10, ref_d+20), 'PINK', font = heading_type_1, fill = 0)




    # draw.text((ref_r+10, 100), ip_disp + " " + time_disp, font = heading_type_2, fill = 0)
    draw.text((ref_r+10, 80), time_only, font = heading_type_2, fill = 0)
    draw.text((ref_r+10, 100), ip_disp, font = heading_type_2, fill = 0)




    space_img = Image.open(os.path.join(picdir, 'space_talk_s.jpg'))
    space_img_r = ref_r + ref_height - 65
    space_img_d = ref_d + ref_width - 60
    image.paste(space_img,(space_img_r,space_img_d))
    draw.rectangle([(space_img_r+3,space_img_d+3),(space_img_r+62-3,space_img_d+56-3)],outline = 255)


    epd.display(epd.getbuffer(image))
    time.sleep(2)


    # test partial refresh
    # epd.init(epd.PART_UPDATE)
    # testImage = Image.open(os.path.join(picdir, 'space_talk_s.jpg'))
    # epd.displayPartial(epd.getbuffer(testImage))
    epd.init(epd.PART_UPDATE)
    testImage = Image.open(os.path.join(picdir, 'space_talk_s.jpg'))
    test_space_img_r = ref_r + 60
    test_space_img_d = ref_d + ref_width - 100
    draw.rectangle((test_space_img_r, test_space_img_d, test_space_img_r+63, test_space_img_d+56), fill = 255)
    image.paste(testImage,(test_space_img_r,test_space_img_d))
    epd.displayPartial(epd.getbuffer(image))


    # epd.init(epd.PART_UPDATE)
    # num = 0
    # while (True):
    #     draw.rectangle((120, 80, 220, 105), fill = 255)
    #     draw.text((120, 80), time.strftime('%H:%M:%S'), font = heading_type_1, fill = 0)
    #     epd.displayPartial(epd.getbuffer(image))
    #     num = num + 1
    #     if(num == 10):
    #         break


    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
