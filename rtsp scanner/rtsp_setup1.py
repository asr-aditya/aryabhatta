import os
import re
import platform
import json
import cv2
i = 0
working_os = platform.system()

if working_os == 'Linux':
    os.system("sudo arp-scan -l > ip_mac.txt")
elif working_os == 'Windows':
    os.system("arp.exe -a > ip_mac.txt")
elif working_os == 'Darwin':
    os.system("arp -a > ip_mac.txt")

#check via video stream
def check_vid(rtsp):   
    cap = cv2.VideoCapture(rtsp)                
    while True:
        ret,frame = cap.read()
        try :
            cv2.imshow('frame', frame)
            print("Don\'t worry your rtsp is correct")
        except Exception as error :
            print('The entered RTSP url is invalid !!')
            extract_rtsp(i)
            break
            
       
        k = cv2.waitKey(0) & 0xFF
        if k == ord('q') :
            #self.calib_switch = False
            cv2.destroyWindow('frame')
            break
#dump rtsp
def dump_rtsp(rtsp):
    print(rtsp,'.............................................................................')
    with open('config.json','r') as con_file:
        data = json.load(con_file)
        data['rtsp_url']=rtsp

    print(data)
    with open('config.json','w') as con_file1:
        json.dump(data, con_file1)

    
    

        
#get ips and mac addresses
f=open("ip_mac.txt", "r")
if f.mode == 'r':
    #ip addresses
    contents =f.read()
    ips = re.findall(r'(?:\d{1,3}\.)+(?:\d{1,3})',contents)
    
    #mac addresses
    p = re.compile(r'(?<!-)(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?!-)', re.IGNORECASE)
    macs = p.findall(contents)
    

#ip or dvr
cam_type = input("Is your camera a 'dvr' or 'ip' : ").strip()

#check all ips and mac addresses
for i in range(len(macs)):


    #defining the function
    def extract_rtsp(j):
        #print('Current Loop value is..........', j)
        check_mac = macs[j]
        check_mac = check_mac[0:8]
        with open('testing.json', 'r') as file:
            jdata = json.load(file)
            isit = check_mac in jdata
            if isit == True:
                camera_ip =ips[j+1]
                camera_mac = macs[j]

                
                print('The mac address for the camera ',jdata[check_mac],' is : ',camera_mac)
                print('The ip address for the camera ',jdata[check_mac],' is', camera_ip)
                rtsp_url = 'rtsp://'+jdata[jdata[check_mac]]['user_name']+':'+jdata[jdata[check_mac]]['user_password']+'@'+camera_ip
                #hardcoded for axis
                if jdata[check_mac] == 'AxisComm Axis Communications AB':
                    rtsp_url = rtsp_url + '/axis-media/media.amp'


            
                if cam_type == 'dvr':
                    channel_no = input('Please input the channel number you want to proceed with : ')

                #hard code for cp plus dvr
                if cam_type == 'dvr':
                    if jdata[check_mac] == "CP Plus":
                        rtsp_url = rtsp_url + '/cam/realmonitor?channel='+channel_no+'&subtype=0'



                print('The expected rtsp url for ',jdata[check_mac],' is : ',rtsp_url)
                print('Is the above rtsp for ',jdata[check_mac],' correct ? If yes press y else press no. If you aren\'t sure, press d to check stream')
                satisfied = input('Press the desired key y/no/d : ').strip()
                if satisfied == 'y' :
                    print("Go on with above details.....")
                    dec = input('Do you want to dump this rtsp url ? y or n :')
                    if dec == 'y':
                        dump_rtsp(rtsp_url)
                    if cam_type == 'dvr':
                        more = input('Do wish to check for more channels: y or n : ')
                        if more == 'y':
                            extract_rtsp(i)


                elif satisfied =='d':
                    check_vid(rtsp_url)
                    dec = input('Do you want to dump this rtsp url ? y or n :')
                    if dec == 'y':
                        dump_rtsp(rtsp_url)
                    
                    if cam_type == 'dvr':
                        more = input('Do wish to check for more channels: y or n : ')
                        if more == 'y':
                            extract_rtsp(i)

                        

                else:
                    usr_name = input("Enter Username: ").strip()
                    usr_pass = input("Enter password: ").strip()
                    rtsp_url = 'rtsp://'+usr_name+':'+usr_pass+'@'+camera_ip
                    print('rtsp url of camera',jdata[check_mac],' is ::', rtsp_url)
                    print("Do you wish to check this stream. Press y to check else press n")
                    anykey = input("y or n : ").strip()
                    
                    
                    if anykey == 'y':
                        check_vid(rtsp_url)
                        dec = input('Do you want to dump this rtsp url ? y or n :')
                        if dec == 'y':
                            dump_rtsp(rtsp_url)
                    
                        
                        if cam_type == 'dvr':
                            more = input('Do wish to check for more channels: y or n :')
                            if more == 'y':
                                extract_rtsp(i)


        
        
    #calling the funct
    extract_rtsp(i)       
            







 

