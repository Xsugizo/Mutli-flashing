# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilenames
from tkinter import filedialog as fd
from time import sleep
from tqdm import tqdm
from alive_progress import alive_bar
import subprocess
from tkinter import messagebox

UsrName = subprocess.check_output('whoami')
UsrName = UsrName.decode().strip()
CurrPath=os.getcwd()
ParetPath=os.path.dirname(CurrPath)


# try : 
#     os.remove('path.txt')
# except:
#     print()

# Select path
def select_FlashTool():
    path = askopenfilenames(title ='Select FlashTool')
    print(path)
    # path = path.replace('/','\\')
    var1.set(path)
    with open('FlashToolPath.txt', 'w') as f:
        f.write(path[0])

def select_FlashImage():
    path = askdirectory(title ='Select FlashImage')
    # path = path.replace('/','\\')
    var11.set(path)
    if 'userdebug' in path:
        messagebox.showinfo("Warning","Ni how bun !")
    with open('FlashImagePath.txt', 'w') as f:
        f.write(path)




def start():
    with open(f'{CurrPath}/RecordOption.txt','w')as f:
        if Turkish.get()!='--':
            f.write('Turkish/')
        if dis_Turkish.get()!='--':
            f.write('dis_turkish/')

    os.system('./Muti_flashing_new.sh')


# def show():
#     # download()
#     os.system(f'python pipeline.py')
#     with alive_bar(16000) as bar:
#         for _ in range(16000):
#             time.sleep(.001)
#             bar()


def close_window():
    root.destroy()

root = tk.Tk()
root.title("WiGAS")
root.resizable(False, False)
root.geometry('690x200')
try:
    with open('FlashToolPath.txt','r') as f:
        FlashToolPath = f.read()
except:
        FlashToolPath = ""


try:
    with open('FlashImagePath.txt','r') as f:
        FlashImagePath = f.read()
except:
        FlashImagePath = ""

var1 = tk.StringVar(value=FlashToolPath)
var11 = tk.StringVar(value=FlashImagePath)



# 創建一個框架
frame = tk.Frame(root)
frame.pack()

# 創建標籤並添加到框架中
label = tk.Label(frame, text="Multiple Flash Tool", font = ('Bahnschrift',20,'bold'),pady=5)
label.pack(side=tk.TOP)

# 創建一個框架
frame2 = tk.Frame(root)
frame2.pack()


Turkish = tk.StringVar()
checkbutton1 = tk.Checkbutton(frame2, text="Enbale Turkish",variable=Turkish, onvalue='Turkish', offvalue='--',pady=1)
checkbutton1.pack(side=tk.LEFT)
checkbutton1.deselect()

dis_Turkish = tk.StringVar()
checkbutton2 = tk.Checkbutton(frame2, text="Disable Turkish",variable=dis_Turkish, onvalue='dis_turkish', offvalue='--',pady=1)
checkbutton2.pack(side=tk.LEFT)
checkbutton2.deselect()

e_path1 = tk.Entry(root, textvariable=var1, width=64)
e_path1.place(x=10, y=80)

b_select1 = tk.Button(root, text='Select Flash Tool', command=select_FlashTool, width=15)
b_select1.place(x=540, y=80)

f_path1 = tk.Entry(root, textvariable=var11, width=64)
f_path1.place(x=10, y=120)

c_select1 = tk.Button(root, text='Select Flash Image', command=select_FlashImage, width=15)
c_select1.place(x=540, y=120)


# 創建一個新的框架用於包含按鈕
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)
# 創建兩個按鈕並添加到新的框架中
button1 = tk.Button(button_frame, text="Start",command=start, width=9)
button1.pack(side=tk.LEFT)

button2 = tk.Button(button_frame, text="Quit",command=close_window, width=9)
button2.pack(side=tk.LEFT)

root.mainloop()

