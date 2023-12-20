#!/bin/bash

#run unclock tool
# echo "run unlock reboot tool"
# cd ~/Desktop/unlock\ tool/
# python3 ./unlocktool_fastboot.py


# source ./progress-bar.sh
# progress-bar 90
# # run times setting
# # python3 ./newUI.py
# echo "GTS"
# cd ~/Desktop/IMAGE/workspace/Pipeline_Testing_Gts

#-------------------------------------------
# python3 ./copyfile.py
#------------------------------------------------

# # read adb device number

device_num=0
devices=$(./device_info_new.py 2>&1)
device_num=$(./device_num_new.py 2>&1)
mode=($device_num)
status=${mode[1]}
devicenum=${mode[0]}
# mode=$(echo $device_num | awk '{print $2}')
echo ${mode[0]}
# switch to fastboot mode
if [ "$status" = "adb" ];then
for x in $devices
do
    adb -s $x reboot bootloader &
 
done
wait
sleep 30
fi

# get fastboot parameter for flash image
f_info=$(./get_fastboot_info.py 2>&1)




my_array=$(echo $f_info | tr "," "\n")
echo "$my_array"

if [ "$status" = "adb" ];then
fastboot devices |  cut -sf 1 | xargs -IX fastboot -s X reboot

echo "waiting for " $devicenum "devices finishing rebooting"
# echo "current has "   $device_num  "devices"
coun=0
while [ $coun != $devicenum ]
do
    
    coun=$(./device_num.py 2>&1)
    # echo "right now has " $coun "devices" 
done
fi
# echo "sleep 100 sec waiting for devices finishing rebooting"

# source ./progress-bar.sh
# progress-bar 100
# sleep 60

# multiple devices flash image in parallel
echo "multiple devices flash image in parallel"
for x in $devices
do

    f1="$(echo "$my_array" | cut -d' ' -f1)"
    f2="$(echo "$my_array" | cut -d' ' -f2)"
    f3="$(echo "$my_array" | cut -d' ' -f3)"
    # f4="$(echo "$my_array" | cut -d' ' -f4)"
    my_array=$(echo $my_array | sed "s/$f1 //1")
    my_array=$(echo $my_array | sed "s/$f2 //1")
    my_array=$(echo $my_array | sed "s/$f3 //1")
    # my_array=$(echo $my_array | sed "s/$f4 //1")
    echo "$f1"
    echo "$f2"
    echo "$f3"
    # echo "$f4"
    echo "wait for 3 sec then $x will flash image"
    source ./progress-bar.sh
    progress-bar 3
    # gnome-terminal -- bash -e 'StrictHostKeyChecking=no ./flashImage1.sh $f1 $f2 $f3 &; exec bash'   
    # StrictHostKeyChecking=no ./flashImage1.sh $f1 $f2 $f3 &
      python3 ./flashImage.py --s $f1 $f2 $f3 &
    # gnome-terminal -e "bash -c command;bash"
    # ./flashImage1.sh $f1 $f2 $f3 &
done
wait
# echo "sleep 30 secs waiting for next steps "
# # progress-bar 900
# source ./progress-bar.sh
# progress-bar 20
# sleep 30


# # set up


# echo "devices set up for gts testing "
# sleep 5
# python3 ./multi_session_device_setup.py


# # for x in $devices
# #     do
# #         echo "CBN check device info "
# #         (./CBN.py --name $x 
# #         # python3 ./multi_devices_setup3.py $x
# #         # echo "devices set up for gts testing "

# #         # echo "sleep 5 sec"
# #         # sleep 5
# #         # # python3 ./multi_devices_setup_A13.py $x
# #         # python3 ./multi_devices_setup_A13_gts.py $x
# #         # # python3 ./multi_devices_setup_A13_terminal.py $x

# #         # echo "sleep 5 sec"
# #         # sleep 5

# #         # echo "set up chrome "
# #         # python3 ./cts_device_setup_for_chrome_Jonathan.py $x


# #         # echo "push media "
# #         # ./CAD_test.py --name $x
# #         )&
        
# #         # echo "sleep 10 sec"
# #         # sleep 10

        
# #         # )&

# #     done

#     # wait




# echo "Ready to run after 40s "
# source ./progress-bar.sh
# progress-bar 40

# ## GTS test
# # python3 ./newpytest.py
# python3 ./newpytest_cmd.py


device_num=$(./device_num_new.py 2>&1)
mode=($device_num)
status=${mode[1]}


while [ "$status" == "adb" ]
do
    device_num=$(./device_num_new.py 2>&1)
    mode=($device_num)
    status=${mode[1]}

    if  [ "$status" != "adb" ];then
        echo "get in fastbootmode"
    fi
    # devcoun=$(./device_num.py 2>&1)
    # echo "right now has " $coun "devices" 
done

echo "waiting for " $devicenum "devices finishing flashing Image"
# echo "current has "   $device_num  "devices"
devcoun=0
echo "devcoun=" $devcoun "devicenum=" $devicenum
while [ $devcoun != $devicenum ]
do
    
    devcoun=$(./device_num.py 2>&1)
    # echo "right now has " $devcoun "devices" 
done

echo "sleep 90 secs waiting for next steps "
# progress-bar 900
source ./progress-bar.sh
progress-bar 90

# sleep 60

if  grep -q Turkish RecordOption.txt ; then
    echo "Enable Turkish"

    # echo "sleep 90 secs waiting for next steps "
    # # progress-bar 900
    # source ./progress-bar.sh
    # progress-bar 90
    ./Enable_trukey.py


fi
if  grep -q dis_turkish RecordOption.txt; then
    echo "Disable Turkish"

    # echo "sleep 90 secs waiting for next steps "
    # # progress-bar 900
    # source ./progress-bar.sh
    # progress-bar 90
    ./Disable_trukey.py

fi
