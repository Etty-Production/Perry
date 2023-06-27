import cv2
import numpy as np
import serial
import time
import math
from FunctionForProject import *

# Video stream source
url = r'http://192.168.61.136:4747/video'

# Capture video stream from camera
cap = cv2.VideoCapture(0)#url)

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
prev_position = None
ball_not_detected = False
buffer_zone_in = 20
buffer_zone_out = 80
alpha = 0.4
timeSt = 0.0
timeGo = 0.0

cv2.namedWindow('Out')
cv2.createTrackbar('DedLineHight', 'Out', 475, 475, lambda x: None)

cascade = cv2.CascadeClassifier('C:/Users/Etty.DESKTOP-B1CTQ9J/Desktop/Perry/Cascade1(2000p&2000n).xml')


while True:
    # Capture a frame from video stream
    ret, frame = cap.read()
    frame = cv2.resize(frame,(620, 480))
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    objects = cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(30, 30)
    )

    middle_of_screen = len(frame[0]) / 2
    DedLineHeight = cv2.getTrackbarPos('DedLineHight', 'Out')

    # Find the largest circle contour if any exist
    max_contour = None
    max_contour1 = None
    max_contour_area = 0
    (center, radius) = ((0,0), 0)
    for (x, y, w, h) in objects:
        radius = min(w, h) / 2
        area = w*h
        x, y = x + (w / 2), y + (h / 2)
        if area > max_contour_area:
            center = (int(x), int(y))
            if (radius > 20):
                max_contour_area = area
                max_contour = (center, int(radius))

    # Display modified frame
    img = frame.copy()
    cv2.rectangle(img, (len(frame[0]) // 2 - buffer_zone_out, 0), (len(frame[0]) // 2 + buffer_zone_out,DedLineHeight), (0, 0, 200), -1)
    cv2.rectangle(img, (len(frame[0]) // 2 - buffer_zone_in, 0), (len(frame[0]) // 2 + buffer_zone_in, DedLineHeight), (0, 200, 0), -1)
    cv2.rectangle(img, (0, DedLineHeight), (len(frame[0]), DedLineHeight + 5), (200, 200, 0), -1)
    frame = cv2.addWeighted(img, alpha, frame, 1 - alpha, 0)

    # Ball tracking system 
    if max_contour is not None:
        ((x, y), radius) = max_contour
        radius = int(radius)

        timeGo = time.time() - timeSt
        if (timeGo > 0.5):
        # Determine if ball is inside zone
            color = (0, 255, 255)

            is_ball_left = False
            is_ball_right = False

            if ((center[0] >= middle_of_screen - buffer_zone_in) and (center[0] <= middle_of_screen + buffer_zone_in)):
                is_ball_detected = True

            if (center[0] // middle_of_screen > 0) and (not is_ball_detected):
                is_ball_left = True
            elif (not is_ball_detected):
                is_ball_right = True
            else:
                color = (0, 0, 255)

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

            if (center[1] <= DedLineHeight):
                cv2.circle(frame, max_contour[0], max_contour[1], (0, 255, 255), 2)
                cv2.circle(frame, max_contour[0], 5, (0, 0, 255), -1)

    # If ball is not detected, print movement command to steer robot towards ball
    else:
        timeSt = time.time()
        if ball_not_detected:
            Move('O', ser)
            print("Ball not detected")
            ball_not_detected = False
        prev_position = None

    cv2.imshow("Out", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()