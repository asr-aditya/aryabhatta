import os
import re
import platform
import json
import cv2
import sys
i = 0
channel_no = 0
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
            cv2.putText(frame, "Press q to close screen", (20,40), cv2.FONT_HERSHEY_COMPLEX, 1, (0,), 3)
            cv2.putText(frame, "Press q to close screen", (20,40), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,200), 1)
            cv2.imshow('frame', frame)
            print(">>>Don\'t worry your rtsp is correct")
        except Exception as error :
            print('.................................................................\n\n###The entered RTSP url is invalid !! Please recheck your username password and try again###\n\n...................................................................')
            extract_rtsp(i)
            break


        k = cv2.waitKey(0) & 0xFF
        if k == ord('q') :
            #self.calib_switch = False
            cv2.destroyWindow('frame')
            break

#get ips and mac addresses
f=open("ip_mac.txt", "r")
if f.mode == 'r':
    #ip addresses
    contents =f.read()
    RE1 = '(?:\d{1,3}\.)+(?:\d{1,3})'
    RE2 = '(?<!-)(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?!-)'

    p = re.compile('('+RE2+'|'+RE1+')');
    matches = p.findall(contents)

    print(matches)
    print(len(matches))


#ip or dvr
cam_type = input("Is your camera a 'dvr' or 'ip' : ").strip()

#check all ips and mac addresses
for i in range(len(matches)):

    #defining the function
    def extract_rtsp(j):
        #print('Current Loop value is..........', j)
        check_mac = matches[j]

        check_mac = check_mac[0:8]

        with open('testing.json', 'r') as file:
            jdata = json.load(file)
            isit = check_mac in jdata
            if isit == True:
                camera_ip =matches[j-1]
                camera_mac = matches[j]


                print('>>>The mac address for the camera ',jdata[check_mac],' is : ',camera_mac)
                print('>>>The ip address for the camera ',jdata[check_mac],' is', camera_ip)
                rtsp_url = 'rtsp://'+jdata[jdata[check_mac]]['user_name']+':'+jdata[jdata[check_mac]]['user_password']+'@'+camera_ip
                print('>>>The defaulf username for ',jdata[check_mac],' is :',jdata[jdata[check_mac]]['user_name'])
                print('>>>The default password for ',jdata[check_mac],' is :',jdata[jdata[check_mac]]['user_password'])

                #ask for channel no for the dvr
                if cam_type == 'dvr':
                    channel_no = 0
                    channel_no = input('### Enter a channel number (default=0) : ')


                #hard code for various companies need to be updated as per need
                #hardcoded for axis
                if jdata[check_mac] == 'AxisComm Axis Communications AB':
                    rtsp_url = rtsp_url + '/axis-media/media.amp'
                    if cam_type == 'dvr':
                        rtsp_url = rtsp_url + '/cam/realmonitor?channel='+channel_no+'&subtype=0'


                #hard code for cp plus dvr
                if jdata[check_mac] == "CP Plus":
                    if cam_type == 'dvr':
                        rtsp_url = rtsp_url + '/cam/realmonitor?channel='+channel_no+'&subtype=0'
                #for hikvisio
                if jdata[check_mac] == "Hikvision":
                    if cam_type == 'dvr':
                        rtsp_url = rtsp_url + '/cam/realmonitor?channel='+channel_no+'&subtype=0'


                #finally print the collected rtsp
                print('>>>The expected rtsp url for ',jdata[check_mac],' is : ','\n###',rtsp_url)
                if cam_type == 'dvr':
                    print('>>>Press y to save the above rtsp for ',jdata[check_mac], ' with channel\"',channel_no,'\", or :')
                else:
                    print('>>>Press y to save the above rtsp for ',jdata[check_mac],', or :')
                print('>>>Press n to enter details manually, or :')
                print('>>>Press d to stream the video for above rtsp :')

                satisfied = input('>>>').strip()
                if satisfied == 'y' :
                    print(">>>You have selected the below rtsp for your system","\n###",rtsp_url)
                    #since the user have saved the url means he is satisfied with it
                    keyx = input('>>>Press x to save the above rtsp exit the program or press r to retry:')
                    if keyx == 'x':
                        sys.exit()
                    if keyx == 'r':
                        extract_rtsp(i)
                #if user wants to check the stream
                elif satisfied =='d':
                    check_vid(rtsp_url)

                    if cam_type == 'dvr':
                        more = input('>>>Press \'y\' to check for more channels else \'x\' to exit program: ')
                        if more == 'y':
                            extract_rtsp(i)
                        elif more == 'x':
                            print('>>>The above rtsp have been saved')
                            sys.exit()



                else:
                    usr_name = input("###Enter Username: ").strip()
                    usr_pass = input("###Enter password: ").strip()
                    rtsp_url = 'rtsp://'+usr_name+':'+usr_pass+'@'+camera_ip
                    print('>>>rtsp url of camera',jdata[check_mac],' is : \n###', rtsp_url)
                    print(">>>Press y to check the stream for entered details else press x to save the above rtsp and exit")
                    anykey = input(">>>y or x : ").strip()


                    if anykey == 'y':
                        check_vid(rtsp_url)
                        if cam_type == 'dvr':
                            more = input('>>>Press y to check for more channels else x to exit :')
                            if more == 'y':
                                extract_rtsp(i)
                            elif more == 'x':
                                print('>>>The above rtsp have been saved')
                                sys.exit()





    #calling the funct
    extract_rtsp(i)
