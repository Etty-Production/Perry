import cv2
import numpy as np
from imageai.Detection import ObjectDetection
import serial
import re, os

#File meneger Functions

def DownloadSettings(Path):
    f = open(Path, 'r+')
    lines = f.readlines() 
    Settings = []
    for line in lines:
        LineData = []
        for s in re.findall(r'\d+', line):
            LineData.append(int(s))
        Settings.append(LineData)
    return(Settings)

def UpdateSettings(Settings, ind):
    ListSet = Settings[ind]
    return ([ListSet[0],ListSet[1],ListSet[2]],[ListSet[3],ListSet[4],ListSet[5]],ListSet[6],ListSet[7],ListSet[8],ListSet[9])

# Image conversion Functions

def Blur(frame, BlurGrade, Iter):
    Grade = BlurGrade if (BlurGrade % 2 == 1) else BlurGrade + 1
    frame = cv2.GaussianBlur(frame, (Grade, Grade), Iter)
    return frame

def ConvLight(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    avg_gray = int(gray.mean())
    compensation_coeff = 128 / avg_gray
    img[:, :, 0] = cv2.multiply(img[:, :, 0], compensation_coeff)
    img[:, :, 1] = cv2.multiply(img[:, :, 1], compensation_coeff)
    img[:, :, 2] = cv2.multiply(img[:, :, 2], compensation_coeff)
    return img

def CreateMask(listSet, frame):
    if listSet is not None:
        lower_color = np.array(listSet[0], dtype=np.uint8)
        upper_color = np.array(listSet[1], dtype=np.uint8)
        IterErode = listSet[2]
        IterDilate = listSet[3]
        BlurIter = listSet[4]
        BlurGrade = listSet[5]    

        frame = ConvLight(frame)
        frame = Blur(frame, BlurGrade, BlurIter)

        # Convert frame to Lab
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)

        # Create binary image to filter out pixels outside of the ball color range
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # Apply morphological transformations to remove noise and fill holes in the binary image
        mask = cv2.erode(mask, None, IterErode)
        mask = cv2.dilate(mask, None, IterDilate)

        frout = mask.copy()
        frout = cv2.bitwise_and(frame, frame, mask = mask) 
        return frout, mask
    return None

def GetAreaImage(img):
    if img is not None: return len(img)*len(img[0])

# Connect to bluetooth Function

def Move(Direction, SerCoundation):
    if SerCoundation is not None:
        SerCoundation.write(format(ord(Direction), 'b')) 

#AI detect ball Function

def PotokLook(frameForDetect, detector):
    Pice = None
    PiceForCute = frameForDetect.copy()
    #custom = detector.CustomObjects(sports_ball = True)
    detection = detector.detectObjectsFromImage( input_image=frameForDetect, minimum_percentage_probability = 0)

    eachItem = None
    for eachItem in detection:
        if eachItem['name'] == 'sports ball':

            Pice = PiceForCute[eachItem['box_points'][1] : eachItem['box_points'][3], eachItem['box_points'][0] : eachItem['box_points'][2]]
            cv2.rectangle(frameForDetect, (eachItem['box_points'][0], eachItem['box_points'][1]), (eachItem['box_points'][2], eachItem['box_points'][3]), (0, 0, 0), -1)

    return (Pice, frameForDetect)

#Other

def CreateFolder(PathToFolder, Name):
    PathToFolder = PathToFolder if (PathToFolder[::-1][0] == '/') or (PathToFolder[::-1][0] == '\\') else PathToFolder+'/'
    if not os.path.isdir(PathToFolder + '/' +Name): os.mkdir(PathToFolder + Name)
    return PathToFolder + Name
