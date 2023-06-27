import cv2
import numpy as np
from pygame import time
from FunctionForProject import *

clock = time.Clock()

cv2.namedWindow('Blur')
cv2.createTrackbar('Bl', 'Blur', 1, 100, lambda x: None)
cv2.createTrackbar('Grade', 'Blur', 0, 100, lambda x: None)

NameWind1 = 'Settings'
cv2.namedWindow(NameWind1)
cv2.resizeWindow(NameWind1, 400, 500) 
cv2.createTrackbar('LMin', NameWind1, 0, 255, lambda x: None)
cv2.createTrackbar('LMax', NameWind1, 255, 255, lambda x: None)
cv2.createTrackbar('AMin', NameWind1, 0, 255, lambda x: None)
cv2.createTrackbar('AMax', NameWind1, 255, 255, lambda x: None)
cv2.createTrackbar('BMin', NameWind1, 0, 255, lambda x: None)
cv2.createTrackbar('BMax', NameWind1, 255, 255, lambda x: None)
cv2.createTrackbar('Erode', NameWind1, 0, 100, lambda x: None)
cv2.createTrackbar('Dilate', NameWind1, 0, 100, lambda x: None)
cv2.createTrackbar('Save', NameWind1, 0, 1, lambda x: None)
cv2.createTrackbar('Stop', NameWind1, 0, 1, lambda x: None)

FpsInVideo = 30
url = r'http://192.168.61.136:4747/video'
cap = cv2.VideoCapture(0)


def Save(mL,mA,mB,maL,maA,maB,erod,dil,gr,bl):
    f = open('ColorClassificatior.txt', 'a+')
    s = 'Min color diapazone [ '+str(mL)+', '+str(mA)+', '+str(mB)+' ] Max color diapazone [ '+str(maL)+', '+str(maA)+', '+str(maB)+' ] Erode '+str(erod)+' Dilate '+str(dil)+' BlurIter '+str(bl)+' BlurGrade '+str(gr)+' ), \n'
    f.write(s)
    f.close()


while True:
    clock.tick(30)
    if cv2.getTrackbarPos('Stop', NameWind1) == 0: ret, frameMain = cap.read()

    

    if ret:
        frame = frameMain.copy()
        frame = cv2.resize(frame,(620, 480))

        Lmax = cv2.getTrackbarPos('LMax', NameWind1)
        Lmin = cv2.getTrackbarPos('LMin', NameWind1)
        Amin = cv2.getTrackbarPos('AMin', NameWind1)
        Amax = cv2.getTrackbarPos('AMax', NameWind1)
        Bmin = cv2.getTrackbarPos('BMin', NameWind1)
        Bmax = cv2.getTrackbarPos('BMax', NameWind1)
        IterErode = cv2.getTrackbarPos('Erode', NameWind1)
        IterDilate = cv2.getTrackbarPos('Dilate', NameWind1)
        SaveFlag = cv2.getTrackbarPos('Save', NameWind1)
        BlurGrade = cv2.getTrackbarPos('Grade', 'Blur')
        BlurIter = cv2.getTrackbarPos('Bl', 'Blur')


        print(Lmin, Lmax)
        print(Amin, Amax)
        print(Bmin, Bmax)

        lower_color = np.array([Lmin, Amin, Bmin], dtype=np.uint8)
        upper_color = np.array([Lmax, Amax, Bmax], dtype=np.uint8)

        #frame = ConvLight(frame)
        Grade = BlurGrade if (BlurGrade % 2 == 1) else BlurGrade + 1
        frame = cv2.GaussianBlur(frame, (Grade, Grade), BlurIter)
        cv2.imshow('Blur', frame)

        if SaveFlag == 1:
            Save(Lmin, Amin, Bmin, Lmax, Amax, Bmax, IterErode, IterDilate, BlurGrade, BlurIter)
            cv2.setTrackbarPos('Save', NameWind1, 0)        

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
        cv2.imshow('Lab', hsv)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        mask = cv2.erode(mask, None, iterations=IterErode)
        mask = cv2.dilate(mask, None, iterations=IterDilate)

        mask  = cv2.bitwise_and(frame, frame, mask = mask) 

    else:

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 

    cv2.imshow('stream', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()