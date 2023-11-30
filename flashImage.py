#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import re
import sys
import os
import time
import subprocess
from subprocess import call
import argparse

UsrName = subprocess.check_output('whoami')
UsrName = UsrName.decode().strip()
parser = argparse.ArgumentParser()
CurrPath=os.getcwd()
ParetPath=os.path.dirname(CurrPath)
# parser.add_argument('--name', type=str, default="") 

# args = parser.parse_args() 

# i= args.name 




parser.add_argument('--s', nargs=3, help="Do stuff with all three arguments.")
  # https://docs.python.org/3/library/argparse.html#nargs
args = parser.parse_args()
with open(f'{CurrPath}/FlashImagePath.txt','r') as f:
    ImagePath = f.read()
with open(f'{CurrPath}/FlashToolPath.txt','r') as f:
    FlashToolPath = f.read()
file_name = os.path.basename(FlashToolPath)
FlashToolname=os.path.splitext(file_name)[0]+".sh"
print("FlashToolname="+os.path.splitext(file_name)[0])
# if args.s:
#     print(len(args.s), "arguments:")
#     print(args.s) # will contain a list
#     print(args.s[0])

i=args.s[0]+" "+args.s[1]+" "+args.s[2]






newpath=ImagePath.replace("\\","/").strip()
print(newpath)
if os.path.isfile(newpath+FlashToolname):
   print("flash Tool "+FlashToolname+" exit")
else:
  print("Copy "+FlashToolname+" To " +ImagePath)
  os.system(f'cp '+FlashToolPath+" "+newpath+'/'+FlashToolname) 
print("i="+i)
print("ImagePath="+ImagePath.replace("\\","/"))
os.chdir(ImagePath.replace("\\","/").strip())
# os.system ('cd /home/logo113/Desktop/IMAGE/Mutli_flashing/0914_6490/athena_A14_user_GMS_RelKey_2023-09-13-1649_14u_SE/Images && ls')
os.system ('pwd')
print (FlashToolname+i)
# os.system ("gnome-terminal -- 'ls'")
os.system ('gnome-terminal -- ./'+FlashToolname+" "+ i)
