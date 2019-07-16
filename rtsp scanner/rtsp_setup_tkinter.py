import os
import re
import platform
import json
import cv2
from tkinter import*

working_os = platform.system()

if working_os == 'Linux':
    os.system("sudo arp-scan -l > ip_mac.txt")
elif working_os == 'Windows':
    os.system("arp.exe -a > ip_mac.txt")
elif working_os == 'Darwin':
    os.system("arp -a > ip_mac.txt")

#play video
def check_vid(rtsp):
    cap = cv2.VideoCapture(rtsp)
    while True:
        ret,frame = cap.read()
        cv2.imshow('frame', frame)
        k = cv2.waitKey(3) & 0xFF
        if k == ord('q') :
            self.calib_switch = False
            cv2.destroyAllWindow()

#take channel no
def get_ch_no(event=None):
    channel_no =entry_ch.get().strip()
    rtsp_url = rtsp_url + '/cam/realmonitor?channel='+channel_no+'&subtype=1'



f=open("ip_mac.txt", "r")
if f.mode == 'r':
    #ip addresses
    contents =f.read()
    RE1 = '(?:\d{1,3}\.)+(?:\d{1,3})'
    RE2 = '(?<!-)(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?!-)'

    p = re.compile('('+RE2+'|'+RE1+')');
    matches = p.findall(contents)
    print(matches)
    root = Tk()
    root.geometry("1000x600")
    root.title("rtsp setup")


    for i in range(len(matches)):
        check_mac = matches[i]
        #check_mac = re.sub(r'[^\w\s]','',check_mac)
        check_mac = check_mac[0:8]
        with open('testing.json', 'r') as file:
            jdata = json.load(file)
            isit = check_mac in jdata
            if isit == True:
                camera_ip =matches[i-1]
                camera_mac = matches[i]
                rtsp_url = 'rtsp://'+jdata[jdata[check_mac]]['user_name']+':'+jdata[jdata[check_mac]]['user_password']+'@'+camera_ip
                line1 = 'The mac address for the camera ',jdata[check_mac],' is : ',camera_mac
                line2 = 'The ip address for the camera ',jdata[check_mac],' is', camera_ip
                label1 = Label(root, text=line1)
                label2 = Label(root, text=line2)
                label1.pack()
                label2.pack()
                print("hellooo")

                #hardcoded for axis
                if jdata[check_mac] == 'AxisComm Axis Communications AB':
                    rtsp_url = rtsp_url + '/axis-media/media.amp'
                #hardcode for cp plus
                if jdata[check_mac] == "CP Plus":
                    label_ch = Label(root, text='Enter Chanel no for the camera')
                    label_ch.pack()
                    entry_ch = Entry(root)
                    entry_ch.pack()
                    button_ch = Button(root, text='Enter',command=get_ch_no)
                    button_ch.pack()


                else:
                    line3 = 'The expected rtsp url for '+ jdata[check_mac] +' is : '+ rtsp_url
                    line4 = 'Is the above rtsp for '+jdata[check_mac]+' correct ? If yes press y else press no. If you aren\'t sure, press d to check stream'
                    label3 = Label(root, text=line3)
                    label4 = Label(root, text=line4)
                    label3.pack()
                    label4.pack()
                    entry1 = Entry(root)
                    entry1.pack()



                    def check_status(event=None):
                        answer = entry1.get().strip().lower()

                        if answer == 'y' :

                            print("Go on with above details.....")


                        elif answer =='d':
                            check_vid(rtsp_url)


                        else:
                            label5 = Label(root,text="Enter Username: ")
                            label5.pack()
                            entry2 = Entry(root)
                            entry2.pack()
                            label6 = Label(root,text="Enter Password: ")
                            label6.pack()
                            entry3 = Entry(root)
                            entry3.pack()

                            def get_rtsp(event = None):
                                user_name = entry2.get().strip().lower()
                                user_pass = entry3.get().strip().lower()
                                rtsp_url = 'rtsp://'+user_name+':'+user_pass+'@'+camera_ip
                                #hardcoded for axis
                                if jdata[check_mac] == 'AxisComm Axis Communications AB':
                                    rtsp_url = rtsp_url + '/axis-media/media.amp'
                                line5 = 'rtsp url of camera'+jdata[check_mac]+' is ::'+ rtsp_url
                                line6 = "Do you wish to check this stream. Press y to check else press n"
                                label7 = Label(root, text=line5)
                                label7.pack()
                                label8 = Label(root, text=line6)
                                label8.pack()
                                entry4 = Entry(root)
                                entry4.pack()

                                def stream_vid(event=None):
                                    ans = entry4.get().strip().lower()
                                    if ans == 'y':
                                        check_vid(rtsp_url)

                                button3 = Button(root, text="Enter",command=stream_vid)
                                button3.pack()

                            button2 = Button(root, text='Enter', command=get_rtsp)
                            button2.pack()



                entry1.bind('<Return>', check_status)
                button1 = Button(root, text='Enter', command=check_status)
                button1.pack()
                root.mainloop()
