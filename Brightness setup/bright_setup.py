import cv2
import numpy as np
from PIL import Image, ImageEnhance
import json

with open('testing.json', 'r') as file:
        config_data = json.load(file)
        std_b_sc1 = config_data['b_timeslot1']
        std_b_sc2 = config_data['b_timeslot2']
        std_b_sc3 = config_data['b_timeslot3']
        std_b_sc4 = config_data['b_timeslot4']
        std_b_sc5 = config_data['b_timeslot5']
        std_b_sc6 = config_data['b_timeslot6']
edited_sc = 100 ##reference level

print("std b score of slot1",std_b_sc1)

print("In which time slot do you want to setup ")
slot = input('''
1) 0600 - 0900
2) 0900 - 1200
3) 1200 - 1500
4) 1500 - 1800
5) 1800 - 2100
6) 2100 - 0600
Enter a value between 1-6
''')
print("slot------",slot)
if slot == '1':
    timeslot = "b_timeslot1"
    std_b_sc = std_b_sc1
elif slot == '2':
    timeslot = "b_timeslot2"
    std_b_sc = std_b_sc2
elif slot == '3':
    timeslot = "b_timeslot3"
    std_b_sc = std_b_sc3
elif slot == '4':
    timeslot = "b_timeslot4"
    std_b_sc = std_b_sc4
elif slot == '5':
    timeslot = "b_timeslot5"
    std_b_sc = std_b_sc5
elif slot =='6':
    timeslot = "b_timeslot6"
    std_b_sc = std_b_sc6

print("timeslot", timeslot)
print("std_b_sc", std_b_sc)

#intake stream
cap = cv2.VideoCapture('croma3_1_Juhu_am_1139_27052019.mp4')
ret,frame = cap.read()

(x,y,w,h)= cv2.selectROI(frame)

print("(x,y,w,h) : ", x,y,w,h)


def brigt_score(imag):
    a = list(imag.getdata())
    b = np.array(a)
    b_score = np.mean(b)
    #print("score:", b_score)
    return b_score

def Y_value(std_score, bright_score):
    if abs(std_b_sc - bright_score) > 10:
        EV = (std_score - bright_score )/10**(abs(std_score - bright_score)/3)
        if EV >=0:
            EV = 1+EV -0.40
        else:
            EV=EV -0.3
        #print("EV:", EV)
    else:
        EV=0
    
    return EV


def img_process(img, EV_get):
    
    #Gamma fuct
    def gamma1(pixel):
        return pow(2, EV_get)*pixel

    processed_im = img.point(gamma1)
    
    return processed_im

def inc_bright(std_b, timeslot): 
    std_b = std_b + 10
    with open('testing.json', 'r') as file:
        json_data = json.load(file)
        json_data[timeslot] = std_b
    with open('testing.json', 'w') as file:
        json.dump(json_data, file, indent=2)
    return std_b

def dec_bright(std_b, timeslot):
    std_b = std_b - 10
    with open('testing.json', 'r') as file:
        json_data = json.load(file)
        json_data[timeslot] = std_b
    with open('testing.json', 'w') as file:
        json.dump(json_data, file, indent=2)
    return std_b

    
while True:
    ret,frame = cap.read()
    if not(ret):
        continue
    cropped = frame[y:y+h, x:x+w]
    im = cropped
    cv2.imshow("cropped",cropped)
    cv2.waitKey(3)
    #cv2 to PIL
    im = Image.fromarray(im)


    #iteration 1
    b_score1 = brigt_score(im)
    EV1 = Y_value(edited_sc, b_score1)
    new_img1 = img_process(im, EV1)
    b_score2 = brigt_score(new_img1)
    
    #iteration2
    if abs(b_score1- b_score2) > 12:
        EV2 = Y_value(edited_sc, b_score2)
        new_img2 = img_process(new_img1, EV2)
        b_score3 = brigt_score(new_img2)
        new_img2.save("processed_img.png")
        
        #iteration3
        if abs(b_score3- b_score2) > 12:
            EV3 = Y_value(edited_sc, b_score3)
            new_img3 = img_process(new_img2, EV3)
            b_score4 = brigt_score(new_img3)
            new_img3.save("processed_img.png")
            img = np.array(new_img3)
        
        else:
            new_img2.save('processed_img.png')
            img = np.array(new_img2)
            
    else:
        new_img1.save('processed_img.png')
        
        img = np.array(new_img1)

        
    #cv2.putText(img, "Increse brightness press: 'i'", (0,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5 ,(0,230,230), 2)
    #cv2.putText(img, "Decrease brightness press: 'd'", (0,24), cv2.FONT_HERSHEY_SIMPLEX, 0.5 ,(0,225,225), 2)
    cv2.putText(img, "Increse brightness press 'i'", (0,10), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0,), 3)
    cv2.putText(img, "Increse brightness press 'i'", (0,10), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0,0,200), 1)
    cv2.putText(img, "Decrease brightness press 'd'", (0,20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0,), 3)
    cv2.putText(img, "Decrease brightness press 'd'", (0,20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0,0,200), 1)

    cv2.imshow('iteration', img)
    
    
    k = cv2.waitKey(3) & 0xFF
    if k == ord('i'):
        print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
        edited_sc = inc_bright(edited_sc, timeslot) 
    
    elif k == ord('d'):
        print('ddddddd')
        edited_sc = dec_bright(edited_sc, timeslot)
    elif k == ord('k'):
        print('breakkkkkkkkk')
        break
    if k == ord('q') :
        self.calib_switch = False
        cv2.destroyAllWindow()
                








