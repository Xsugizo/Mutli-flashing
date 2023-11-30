import os
print('Update/Upgrade')
os.system('sudo apt-get update')
os.system('sudo apt-get upgrade')

print('Download python3.9')
os.system('sudo apt install software-properties-common')
os.system('sudo add-apt-repository ppa:deadsnakes/ppa')
os.system('sudo apt-get install python3.9')
os.system('sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1')

print('Download pip3')
os.system('curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py')
os.system('sudo python3.9 get-pip.py')

# print('Download setuptools')
# os.system('sudo pip3 install --upgrade pip setuptools')

# print('Download UI2')
# os.system('sudo pip3 install --no-cache-dir uiautomator2')

# print('Download alive_progress')
# os.system('sudo pip3 install alive_progress')

# print('Download GUI')
# os.system('sudo pip3 install --force-reinstall pyautogui')

# print('Download tkinter')
# os.system('sudo apt install python3-tk')

# print('Download tqdm')
# os.system('sudo apt install python3-tqdm')

print('All download done')