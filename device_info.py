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
import subprocess
from subprocess import call
devices = []
output_build_number=[]
#device_re = re.compile("device")

adb_devices= subprocess.check_output(["adb", "devices"])
#print(adb_devices)
for i in adb_devices.split(b"\tdevice"):
    for ii in i.split(b"\n"):
        if  ii !="" and ii not in "List of devices attached" :
            devices.append(ii)
for i in devices:
     print(i)