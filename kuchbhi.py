# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 10:28:32 2019

@author: Aditya Singh Rathore
"""

import os
import re
import platform
import json
import cv2

working_os = platform.system()

if working_os == 'Linux':
    os.system("sudo arp-scan -l > ip_mac.txt")
elif working_os == 'Windows':
    os.system("arp.exe -a > ip_mac.txt")
elif working_os == 'Darwin':
    os.system("arp -a > ip_mac.txt")


f=open("ip_mac.txt", "r")
if f.mode == 'r':
    contents =f.read()
    p = re.compile(r'(?<!-)(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?!-)', re.IGNORECASE)
    macs = p.findall(contents)
    
    #ip addresses
    
    ips = re.findall(r'(?:\d{1,3}\.)+(?:\d{1,3})',contents)
    print(macs)
    print(ips)
    #mac addresses
for i in range(len(macs)):


    
    print('Current Loop value is..........', i)
    check_mac = macs[i]
    check_mac = check_mac[0:8]
    print(check_mac)
    with open('testing.json', 'r') as file:
        jdata = json.load(file)
        isit = check_mac in jdata
        print('...............',isit,'.............')
        if isit == True:
            camera_ip =ips[i+1]
            camera_mac = macs[i]

                
            print('The mac address for the camera ',jdata[check_mac],' is : ',camera_mac)
            print('The ip address for the camera ',jdata[check_mac],' is', camera_ip)


	 
