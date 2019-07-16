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



f=open("ip_mac.txt", "r")
if f.mode == 'r':
    #ip addresses
    contents =f.read()
    RE1 = '(?:\d{1,3}\.)+(?:\d{1,3})'
    RE2 = '(?<!-)(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?!-)'

    p = re.compile('('+RE2+'|'+RE1+')');
    matches = p.findall(contents)
    print(matches)
    master = Tk()
    master.geometry("1000x600")
    master.title("rtsp setup")



#select Camera
Label1= Label(master, text="Select Your Camera Type :")
Label1.grid(row=1,columnspan = 5, sticky=W)
var1 = IntVar()
Checkbutton(master, text="DVR", variable=var1).grid(row=2,column=0, sticky=W)
var2 = IntVar()
Checkbutton(master, text="IP", variable=var2).grid(row=2,column=1, sticky=W)
var3 = IntVar()
button1 = Button(master, text='Go', command=lambda: var3.set(1) and camera_type)
button1.grid(row=2,column=3, sticky=E, pady=4)
button1.wait_variable(var3)

#DVR or IP
if var1.get()==1:
    cam_type='dvr'
elif var2.get()==1:
    cam_type='ip'
print(cam_type,".............................")


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


                # print('>>>The mac address for the camera ',jdata[check_mac],' is : ',camera_mac)
                # print('>>>The ip address for the camera ',jdata[check_mac],' is', camera_ip)
                rtsp_url = 'rtsp://'+jdata[jdata[check_mac]]['user_name']+':'+jdata[jdata[check_mac]]['user_password']+'@'+camera_ip
                # print('>>>The defaulf username for ',jdata[check_mac],' is :',jdata[jdata[check_mac]]['user_name'])
                # print('>>>The default password for ',jdata[check_mac],' is :',jdata[jdata[check_mac]]['user_password'])

                Label2 = Label(master, text="Camera :")
                Label2.grid(row=4,column=0,sticky=E)
                Label3 = Label(master, text=jdata[check_mac])
                Label3.grid(row=4,column=1,sticky=W)

                Label4 = Label(master, text="IP :")
                Label4.grid(row=5,column=0,sticky=E)
                Label5 = Label(master, text=camera_ip)
                Label5.grid(row=5,column=1,columnspan=2,sticky=W)

                Label6 = Label(master, text="Username :")
                Label6.grid(row=6,column=0,sticky=E)
                Label7 = Label(master, text=jdata[jdata[check_mac]]['user_name'])
                Label7.grid(row=6,column=1,sticky=W)

                def edit1():
                    entry1 = Entry(master)
                    entry1.grid(row=6, column=4, columnspan=2)
                    def get_edit1():
                        global edited_user
                        edited_user = entry1.get()
                    buttone1 = Button(master, text = "Enter",command=get_edit1)
                    buttone1.grid(row=6, column=6)
                button2 = Button(master, text="Edit", command=edit1)
                button2.grid(row=6, column=3, sticky=E)


                Label8 = Label(master, text="Password :")
                Label8.grid(row=7,column=0,sticky=E)
                Label9 = Label(master, text=jdata[jdata[check_mac]]['user_password'])
                Label9.grid(row=7,column=1,sticky=W)

                def edit2():
                    entry2 = Entry(master)
                    entry2.grid(row=7, column=4, columnspan=2)
                    def get_edit2():
                        global edited_pass
                        edited_pass = entry2.get()
                    buttone2 = Button(master, text = "Enter",command=get_edit2)
                    buttone2.grid(row=7, column=6)
                button2 = Button(master, text="Edit", command=edit2)
                button2.grid(row=7, column=3, sticky=E)


                button3 = Button(master, text="Edit", command=edit2)
                button3.grid(row=7, column=3, sticky=E)


                #ask for channel no for the dvr
                #take channel no
                def get_ch_no(event=None):
                    channel_no =entry_ch.get().strip()



                if cam_type == 'dvr':
                    channel_no = '0'
                    Label10 = Label(master, text="Channel Number :")
                    Label10.grid(row=8, column=0)
                    entry_ch = Entry(master)
                    entry_ch.grid(row=8, column=1)
                    button_ch = Button(master, text="Enter", command = get_ch_no)

                    #channel_no = input('### Enter a channel number (default=0) : ')


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
                #adding cannel input
                if cam_type == 'dvr':
                    rtsp_url = rtsp_url + '/cam/realmonitor?channel='+channel_no+'&subtype=1'
                #finally print the collected rtsp
                label11 = Label(master, text="RTSP :")
                label11.grid(row=10, column=0)
                label12 = Label(master, text= rtsp_url)
                label12.grid(row=10, column=1, columnspan=12)




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



master.mainloop()
