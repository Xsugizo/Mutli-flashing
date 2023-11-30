#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################################################
import os
import time
import subprocess
def test():
    os.system('fastboot devices')
    os.system('fastboot devices |  cut -sf 1 | xargs -IX fastboot -s X oem sku')
    os.system('fastboot devices |  cut -sf 1 | xargs -IX fastboot -s X getvar msmserialno')
    os.system('fastboot devices |  cut -sf 1 | xargs -IX fastboot -s X reboot')
    #time.sleep(30)
#test()
#make a string to add behind setup.py

def device_str():
    try:
        de_str =[]
        device = os.popen('fastboot devices').read()
        device = device.split()
        for i in range(len(device)):
            if(i>=0 and i%2 ==0):
                de_str.append(device[i])
        return de_str
    except:
        print("error to make devices string")
str_de1 = device_str()

# print(str_de1)

def device_str1():
    try:
        de_str =[]
        device = os.popen('fastboot devices |  cut -sf 1 | xargs -IX fastboot -s X oem sku 2>&1').read()
        device = device.split()
        for i in range(len(device)):
            if (i>=4 and (i-4)%12 == 0):
                de_str.append(device[i])
        return de_str
    except:
        print("error to make devices string")
str_de2 = device_str1()

# print(str_de2)

def device_str2():
    try:
        de_str =[]  
        device = os.popen('fastboot devices |  cut -sf 1 | xargs -IX fastboot -s X getvar msmserialno 2>&1 ').read()
        device = device.split()
        for i in range(len(device)):
            if(i>=1 and (i-1)%6==0):
                de_str.append(device[i])
        return de_str
    except:
        print("error to make devices string")
str_de3 = device_str2()

# print(str_de3)
adb_devices= subprocess.check_output(["fastboot", "devices"])
#print(adb_devices)
device=[]
for i in adb_devices.split(b"\tdevice"):
    for ii in i.split(b"\n"):
        if  ii !="" and ii not in "List of devices attached" :
            device.append(ii)
coun=int(len(device))



for i in range(coun):
    print(str_de1[i])
    print(str_de2[i])
    print(str_de3[i])
    

