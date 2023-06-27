import cv2, os
import numpy as np
from imageai.Detection import ObjectDetection
from FunctionForProject import *
import time

detector = ObjectDetection()

model_path = "C:/Users/Etty.DESKTOP-B1CTQ9J/yolov3.pt"

alpha = 0.4
stTime = 0

detector.setModelTypeAsYOLOv3()
#detector.setModelTypeAsRetinaNet()
detector.setModelPath(model_path)
detector.loadModel()

Settings = DownloadSettings('ColorClassificatior.txt')
KolListsSettings = len(Settings)

threshold = 30
cap = cv2.VideoCapture(0)

#Create output folder

CreateFolder(os.getcwd(), 'masks')


while True:
    ret, frame = cap.read()

    if ret:
        Data = None
        Data = PotokLook(frame, detector)
        frame = Data[1]
        
        #print(GetAreaImage(Data[0]), GetAreaImage(Data[1]))

        if Data[0] is not None: 
            for ind in range(KolListsSettings):
                listSet = UpdateSettings(Settings, ind)

                # Define color range for the ball
                OutFrame, maskFrame = CreateMask(listSet, frame)
                OutPice, maskPice = CreateMask(listSet, Data[0])
                cv2.imwrite('masks/Frame'+str(ind)+'.jpg', OutFrame)
                cv2.imwrite('masks/Pice'+str(ind)+'.jpg', OutPice)

                contoursFrame, _ = cv2.findContours(maskFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contoursPice, _ = cv2.findContours(maskPice.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                AreaNoizeFrame = 0
                for contF in contoursFrame:
                    AreaNoizeFrame += cv2.contourArea(contF)

                AreaContourPice = 0
                for contP in contoursPice:
                    AreaContourPice = max(cv2.contourArea(contP), AreaContourPice)

                #Output procents of filling mask 
                print('All Frame withount pice procent сompletion',int(AreaNoizeFrame/(GetAreaImage(Data[1]) - GetAreaImage(Data[0]))*100),'Pice procent сompletion', int(AreaContourPice/GetAreaImage(Data[0])*100), 'Mask number', ind)

    cv2.imshow('Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
