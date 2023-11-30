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
import shutil
UsrName = subprocess.check_output('whoami')
UsrName = UsrName.decode().strip()
parser = argparse.ArgumentParser() 
# parser.add_argument('--name', type=str, default="") 

# args = parser.parse_args() 

# i= args.name
platform=input("1) 6490 or 2)  4490 ? " )

ans=input("please input your image file path : ")
ans = ans.replace('/','\\')
with open('ImagePath.txt', 'w') as f:
    f.write(ans)

parser.add_argument('--s', nargs=3, help="Do stuff with all three arguments.")
  # https://docs.python.org/3/library/argparse.html#nargs
args = parser.parse_args()
with open(f'/home/{UsrName}/Desktop/IMAGE/Mutli_flashing/ImagePath.txt','r') as f:
    ImagePath = f.read()
# if args.s:
#     print(len(args.s), "arguments:")
#     print(args.s) # will contain a list
#     print(args.s[0])
newpath=ImagePath.replace("\\","/").strip()
print(newpath)
print("platfoerm="+str(platform))
if platform=="1":
    os.system('cp /home/logo113/Desktop/IMAGE/Mutli_flashing/6490/install_Athena_1vN.sh '+ newpath+'/install_Athena_1vN.sh') 
    print("copy 6490 tool done")
if platform=="2":
    os.system('cp /home/logo113/Desktop/IMAGE/Mutli_flashing/4490/install_Nemesis_1VN.sh '+ newpath+'/install_Nemesis_1VN.sh') 
    print("copy 4490 tool done")
# os.chdir(ImagePath.replace("\\","/").strip())
# shutil.copyfile('/home/logo113/Desktop/IMAGE/Mutli_flashing/4490/install_Nemesis_1VN.sh', newpath+'/')





