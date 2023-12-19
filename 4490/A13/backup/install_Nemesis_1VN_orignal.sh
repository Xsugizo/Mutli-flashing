#!/bin/bash
# Copyright (c) 2023 Zebra Technologies Corporation and/or its affiliates. All rights reserved.
# Nemesis Install Script

function check_adb_id {
    adb devices -l > devices.txt
    sed -i '1d' devices.txt

    device=`cat devices.txt`
    IFS=$'\n'
    a=($device)
    echo "device number: ${#a[@]}"
    let i=0
    while [ $i -lt ${#a[@]} ]
    do
        dd=${a[$i]##*transport_id:}
        m=`adb -t $dd shell getprop ro.boot.msmserialno` 
		
        if [ `echo $1 | awk -v msn=$m '{print($1==msn)? "1": "0"}'` -eq "1" ]; then
            echo "target device id: $dd"
            break;
        fi

        let i++
    done
	
    if [ $i -eq ${#a[@]} ]; then
        dd=999999999
        echo "Can't find the target id"
    fi
}


function install_image_real {
	image=`ls $2.*`
	if [ ! -s "$image" ]; then
		echo "***********************"
		echo "  Invalid file $image"
		echo "***********************"
		exit -1
	fi

	echo "***********************"
	echo " Installing $2"
	echo "***********************"

	fastboot -s $device_sn flash -S 250M --unbuffered $1 $image 2>&1 | tee install.txt | grep "Sending"

	e='grep FAILED install.txt'
	if [ $? -ne 0 ]; then
		echo "***********************"
		echo " Install $2 Failed"
		echo "***********************"
		exit -1
	fi
}

function install_image {
	if [ $# == 1 ]; then
		p=$1
	else
		p=$2
	fi
	install_image_real $1 $p
}

function install_ab_image {
	if [ $# == 1 ]; then
		p=$1
	else
		p=$2
	fi
	install_image_real $1_a $p
	install_image_real $1_b $p
}

function install_chipcode_image {
	if [ "$answer" != "y" ];then
		echo
		echo "******************************"
		echo "Skip flashing Non-HLOS images."
		echo "******************************"
		return
	fi

	echo
	echo "************************************************************"
	echo "Flashing Non-HLOS images start in 3 secs(Ctrl+c to break)..."
	echo "************************************************************"
	sleep 3

	echo "***********************"
	echo " Installing Secured FW"
	echo "***********************"

	for image_name in abl cpucp featenabler imagefv shrm tz xbl_config devcfg aop qweslicstore recovery
	do
		install_ab_image $image_name
	done

	for image_name in rtice storsec uefi
	do
		install_image $image_name
	done

	install_ab_image xbl xbl_s
	install_ab_image xbl_ramdump XblRamdump
	install_ab_image aop_config aop_devcfg
	install_ab_image dsp dspso
	install_ab_image hyp hypvm
	install_ab_image multiimgoem multi_image
	install_ab_image qupfw qupv3fw
	install_ab_image uefisecapp uefi_sec
	install_ab_image keymaster keymint
	install_image toolsfv tools
	install_image logfs logfs_ufs_8mb

	# install modem
	Modem=NON-HLOS-WAN
	grep QCS variant.txt > /dev/null
	if [ $? -eq 0 ]; then
		Modem=NON-HLOS-WLAN
	fi

	echo "using $Modem as Modem"

	install_ab_image modem $Modem
}

function install_android_image {
	echo "***********************"
	echo " Installing Android FW"
	echo "***********************"

	for image_name in vbmeta vbmeta_system vendor_boot boot dtbo
	do
		install_ab_image $image_name
	done

	for image_name in super enterprise
	do
		install_image $image_name
	done

	fastboot -s $device_sn erase userdata
	fastboot -s $device_sn erase metadata
	fastboot --set-act=a
}


function check_secureboot {
	echo "Checking secure boot state..."
	secure_state=$(fastboot getvar secure 2>&1)
	secure_state=${secure_state#*: }
	secure_state=${secure_state%%finish*}
	secure_state=$(echo $secure_state)
	echo "Is Secure Boot enabled? $secure_state"
}

if [ `echo $1 | awk -v temp=0 '{print($1>temp)? "1": "0"}'` -eq "1" ]; then
    device_sn="$1"
    echo "SN: $device_sn"
fi
[ $2 -ne 0 ]&&sku_id="$2"||sku_id="0"
echo "  sku: $sku_id  "
#[ $3 -ne 0 ]&&msmserialno="$3"||msmserialno="0"
msmserialno="$3"
echo "  msmserialno: $msmserialno  "

answer="y"
adb devices > devices.txt
d=`grep device devices.txt -c`
if [ $d -ge 1 ]; then
	echo "***********************"
	echo "   Device in adb mode  "
	echo "***********************"

	platform_value=$(adb -s $device_sn shell getprop ro.boot.device.platform | tr -d '\r')
	if [ "$platform_value" != "4490" ];then
		echo "**************************"
		echo "   Wrong platform : $platform_value  "
		echo "**************************"
		exit -1
	fi
	product_check="pass"
	adb -s $device_sn reboot bootloader
	echo "Rebooting to fastboot, wait for 10 seconds..."
	sleep 10
fi

fastboot devices > devices.txt
d=`grep fastboot devices.txt -c`
if [ $d -ge 1 ]; then
	echo "***********************"
	echo "Device in fastboot mode"
	echo "***********************"
else
	echo "***********************"
	echo "Check device connection"
	echo "***********************"
	exit -1
fi

if [ "$product_check" != "pass" ];then
	echo "Checking Nemesis product..."
	product=$(fastboot -s $device_sn getvar product 2>&1)
	product=${product#*: }
	product=${product:0:6}
	echo "Product : $product"

	if [ "$product" != "parrot" ];then
		echo "**************************"
		echo "   Wrong product : $product  "
		echo "**************************"
		exit -1
	fi
fi

check_secureboot
if [ "$secure_state" = "yes" ];then
	echo
	echo "--00000000000----00000000000----00000000000----00-------00"
	echo "--00-------------00-------------00-------------00-------00"
	echo "--00-------------00-------------00-------------00-------00"
	echo "--00000000000----00000000000----00-------------00-------00"
	echo "-----------00----00-------------00-------------00-------00"
	echo "--00-------00----00-------------00-------------00-------00"
	echo "--00000000000----00000000000----00000000000----00000000000"
	echo

	answer="n"
	read -t 10 -p "Flash the Non-HLOS images?(Y/y + [ENTER] to flash,timout in 10s)?" answer
	case $answer in
	        [Yy]* )  answer="y";;
	        * ) echo;echo "Flasing only HLOS images in 3 secs(Ctrl+c to break)...";sleep 3;;
	esac
fi
echo "***********************"
echo "Installing Nemesis Image"
echo "***********************"

fastboot -s $device_sn oem SYS_SN 2> devinfo.txt
# check sku id before install
e=`grep "SYS_SN: S" devinfo.txt`
if [ $? -ne 0 ]; then
	echo "***********************"
	echo "    Install Aborted    "
	echo "     SN is missing     "
	echo "***********************"
	exit -1
else
	sys_sn=`cat devinfo.txt | grep SYS_SN | cut -d ":" -f 2`
fi

fastboot -s $device_sn oem device-info 2> devinfo.txt
# check sku id before install
e=`grep "SKU: 0" devinfo.txt`
if [ $? -eq 0 ]; then
	echo "***********************"
	echo "    Install Aborted    "
	echo "   SKU ID is missing   "
	echo "***********************"
	exit -1
else
	sku=`cat devinfo.txt | grep SKU | cut -d ":" -f 2 | tr -d '\r'`
fi

echo "***********************"
echo "    SKU ID is $sku"
echo "***********************"

fastboot -s $device_sn getvar all 2> variant.txt


if [ $# -gt 0 ]; then
	flash_all=$1
else
	flash_all=all
fi

install_android_image

if [ x"$flash_all" == x"all" ]; then
	install_chipcode_image
fi

unlock_state=$(fastboot -s $device_sn oem device-info 2>&1 | grep "Device unlocked" | tr -d '\r')
unlock_state=${unlock_state#*: }
critical_unlock_state=$(fastboot -s $device_sn oem device-info 2>&1 | grep "Device critical unlocked" | tr -d '\r')
critical_unlock_state=${critical_unlock_state#*: }
echo "********************************"
echo "unlock state : $unlock_state"
echo "Critical unlock state : $critical_unlock_state"
echo "********************************"

if [ "$unlock_state" == "true" ];then
        if [ "$critical_unlock_state"  == "true" ];then
                echo "*********************************"
                echo "     Do fastboot oem lock_all"
                echo "*********************************"
                # fastboot oem lock_all > /dev/null 2>&1
				fastboot -s $device_sn reboot
        else
                echo "*********************************"
                echo "    Do fastboot flashing lock"
                echo "*********************************"
                fastboot flashing lock > /dev/null 2>&1
        fi
else
        if [ "$critical_unlock_state" == "true" ];then
                echo "****************************************"
                echo "   Do fastboot flashing lock_critical"
                echo "****************************************"
                fastboot flashing lock_critical > /dev/null 2>&1
        else
                echo "****************************************"
                echo "   deivice is fully locked already!"
                echo "****************************************"
                fastboot -s $device_sn reboot
        fi
fi

if [ $? -ne 0 ];then
        echo "***********************************"
        echo "    Lock deice failed   "
        echo "***********************************"
else
	echo "--00000000000-------0000--------00000000000----00000000000"
	echo "--00-------00------00---00------00-------00----00-------00"
	echo "--00-------00-----00-----00-----00-------------00---------"
	echo "--00000000000----00-------00----00000000000----00000000000"
	echo "--00-------------00000000000-------------00-------------00"
	echo "--00-------------00-------00----00-------00----00-------00"
	echo "--00-------------00-------00----00000000000----00000000000"
fi
