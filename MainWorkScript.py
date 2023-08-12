import cv2
import numpy as np
import serial
import time
import math
from FunctionForProject import *

# Video stream source
url = r'http://192.168.61.136:4747/video'

# Capture video stream from camera
cap = cv2.VideoCapture(0)#'TestVideos/11.mp4')

# Connect to Arduino

try:
    ser = serial.Serial('COM11', 9600)
except Exception as e:
    ser = None
    print('Bluetooth модуль не найден, перевод в тестирующий режим...')

# Global variables
is_ball_left = False
is_ball_right = False
is_ball_detected = False
prev_position = [False, False]
ball_not_detected = False
buffer_zone_in = 20
buffer_zone_out = 80
alpha = 0.4
timeSt = 0.0
timeGo = 0.0

cv2.namedWindow('Out')
cv2.createTrackbar('DedLineHight', 'Out', 475, 475, lambda x: None)

StartModel('VisualModel/BestNano.pt')

while True:
    # Capture a frame from video stream
    ret, frame = cap.read()
    
    if not ret:
        continue

    frame = cv2.resize(frame,(640, 480))

    middle_of_screen = len(frame[0]) / 2
    DedLineHeight = cv2.getTrackbarPos('DedLineHight', 'Out')

    #When convert tensor to int tensor remove(if tensor contain real variable)
    pos, probability = DetectBall(frame)
    
    # Ball tracking system 
    if (pos is not None):

        center = [int(pos[0]+(pos[2]-pos[0]) / 2), int(pos[1]+(pos[3]-pos[1]) / 2)]
        if (center[1] > DedLineHeight): break
        del pos

        timeGo = time.time() - timeSt
        if (timeGo > 0.5):
        # Determine if ball is inside zone
            color = (104, 76, 2)

            is_ball_left = False
            is_ball_right = False

            if ((center[0] >= middle_of_screen - buffer_zone_in) and (center[0] <= middle_of_screen + buffer_zone_in)):
                is_ball_detected = True

            if (center[0] // middle_of_screen > 0) and (not is_ball_detected):
                is_ball_left = True
            elif (not is_ball_detected):
                is_ball_right = True
            else:
                color = (0, 86, 166)

            # Only send movement command once per buffer zone transition
            if (prev_position != [is_ball_left, is_ball_right]) and (center[1] <= DedLineHeight):
                if is_ball_left:
                    Move('L', ser)
                    print("Robot should move left")
                elif is_ball_right:
                    Move('R', ser)
                    print("Robot should move right")
                else:
                    Move('S', ser)
                    print("Robot should move straight")
                prev_position = [is_ball_left, is_ball_right]

            if (center[0] < middle_of_screen - buffer_zone_out) or (center[0] > middle_of_screen + buffer_zone_out):
                is_ball_detected = False

            ball_not_detected = True

            #Display ball position
            cv2.line(frame, (center[0], 0), (center[0], len(frame)), color, 1)
            cv2.line(frame, (0, center[1]), (len(frame[0]), center[1]), color, 1)
            cv2.circle(frame, center, 10, color, 1)
            cv2.circle(frame, center, 2, (0, 0, 0), -1)
            img = frame.copy()
            cv2.rectangle(img, (center[0] + 15, center[1] - 15), (center[0] + 60, center[1] - 5), (100, 100, 100), -1)
            frame = cv2.addWeighted(img, 0.6, frame, 0.4, 0)
            frame = cv2.putText(frame, str(round(float(probability) * 100, 1)) + '%', (center[0] + 15, center[1] - 5), cv2.FONT_HERSHEY_PLAIN, 1, (34, 255, 94), 2)
            del img 

    # If ball is not detected, print movement command to steer robot towards ball
    else:
        timeSt = time.time()
        if ball_not_detected:
            Move('O', ser)
            print("Ball not detected")
            ball_not_detected = False
        prev_position = None

    # Display modified frame
    img = frame.copy()
    cv2.rectangle(img, (len(frame[0]) // 2 - buffer_zone_out, 0), (len(frame[0]) // 2 + buffer_zone_out,DedLineHeight), (0, 0, 200), -1)
    cv2.rectangle(img, (len(frame[0]) // 2 - buffer_zone_in, 0), (len(frame[0]) // 2 + buffer_zone_in, DedLineHeight), (0, 200, 0), -1)
    cv2.rectangle(img, (0, DedLineHeight), (len(frame[0]), DedLineHeight + 5), (200, 200, 0), -1)
    frame = cv2.addWeighted(img, alpha, frame, 1 - alpha, 0)
    del img

    cv2.imshow("Out", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        Move('O', ser)
        print("Script is Over")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

