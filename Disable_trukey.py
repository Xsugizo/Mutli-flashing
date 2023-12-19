#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import bs4   #BeautifulSoup 3 has been replaced

# # load the file
# with open("/home/logo007/Desktop/IMAGE/workspace/project_test_pipeline/11_r10/android-cts-11_r10-linux_x86-arm/android-cts/results/latest_test_result.html",encoding='UTF-8') as inf:
#     txt = inf.read()
#     soup = bs4.BeautifulSoup(txt)

# # create new link
# new_link = soup.new_tag("link", rel="stylesheet", href="/home/logo007/Desktop/IMAGE/workspace/project_test_pipeline/11_r10/android-cts-11_r10-linux_x86-arm/android-cts/results/compatibility_result.css")
# # insert it into the document
# soup.head.append(new_link)

# # save the file again
# with open("/home/logo007/Desktop/IMAGE/workspace/project_test_pipeline/11_r10/android-cts-11_r10-linux_x86-arm/android-cts/results/latest_test_result.html", "w",encoding='UTF-8') as outf:
#     outf.write(str(soup))

# soup = bs4.BeautifulSoup(open("/home/logo007/Desktop/IMAGE/workspace/project_test_pipeline/11_r10/android-cts-11_r10-linux_x86-arm/android-cts/results/latest_test_result.html",encoding='UTF-8').read())
# stylesheets = soup.findAll("link", {"rel": "stylesheet"})
# for s in stylesheets:
#     t = soup.new_tag('style')
#     c = bs4.element.NavigableString(open(s["href"]).read())
#     t.insert(0,c)
#     t['type'] = 'text/css'
#     s.replaceWith(t)
# open("/home/logo007/Desktop/IMAGE/workspace/project_test_pipeline/11_r10/android-cts-11_r10-linux_x86-arm/android-cts/results/output.html", "w",encoding='UTF-8').write(str(soup))


import re
import sys
import os
import time
from time import sleep
import subprocess
from subprocess import call
devices = []
output_build_number=[]
CurrPath=os.getcwd()
ParetPath=os.path.dirname(CurrPath)
#device_re = re.compile("device")

adb_devices= subprocess.check_output(["adb", "devices"])
# print(adb_devices)
for i in adb_devices.split("\tdevice"):
    for ii in i.split(b"\n"):
        if  ii !="" and ii not in "List of devices attached" :
            devices.append(ii)
coun=str(len(devices))
number = 0

def get_device_num():
    devices_num = []
    adb_devices= subprocess.check_output(["adb", "devices"])
    # print(adb_devices)
    for i in adb_devices.split("\tdevice"):
        for ii in i.split(b"\n"):
            if  ii !="" and ii not in "List of devices attached" :
                devices_num.append(ii)
    coun=str(len(devices_num))
    return coun
print("dev_num="+str(coun))
for i in devices:
    # adb root, adb disable-verity, adb reboot, adb remount
    # adb push /home/logo113/Desktop/IMAGE/Mutli_flashing/turkish/turkish.ini /mnt/vendor/persist/
    # adb chmod 644 /mnt/vendor/persist/turkish.ini
    # adb reboot
    # os.system ('gnome-terminal -- ./'+FlashToolname+" "+ i)
    print("device id="+i)
    os.system('adb -s '+i+' root')
    sleep (5)
    # os.system('adb -s '+i+' disable-verity')
    # sleep (5)
    # os.system('adb -s '+i+' reboot')
    # sleep (5)

    # while number != coun:
        
    #     number = get_device_num()
    #     if number==coun:
    #         print('reboot complete')
    # os.system('adb -s '+i+' root')
    # sleep (10)
    # os.system('adb -s '+i+' remount')
    # sleep (5) 
    # # os.system('adb -s '+i+' push '+CurrPath+'/turkish/turkish.ini /mnt/vendor/persist/')
    # # sleep (2) 
    os.system('adb -s '+i+' shell rm /odm/zpersist/turkish.ini')
    sleep (2) 
    os.system('adb -s '+i+' reboot')
    sleep (5)
    number = 0
    while number != coun:
        number = get_device_num()
        if number==coun:
            print('reboot complete') 
    os.system('adb -s '+i+' reboot')
    sleep (5)
    number = 0
    while number != coun:
        number = get_device_num()
        if number==coun:
            print('reboot complete') 