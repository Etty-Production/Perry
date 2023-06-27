import cv2, os
import numpy as np
import re
import time

def GetLines(Path):
	f = open(Path, 'r+')
	lines = f.readlines()
	f.close()
	return lines

def GetNumb(StrInt):
	LineData = []
	PiceOfLine = []
	ind = -1
	for s in re.findall(r'\d+', StrInt):
		ind += 1
		if ind < 4: PiceOfLine.append(int(s))
		else:
			LineData.append(PiceOfLine)
			PiceOfLine = []
			ind = -1
	return LineData

def CutPiceOfImage(Image, DataPos, NameImg):
	global OutPath
	for (xIn, yIn, xOut, yOut) in DataPos:
		Pice = Image[yIn : yOut, xIn : xOut]
		Pice = cv2.resize(Pice,(64, 64))
		cv2.imwrite(OutPath+'/'+str(NameImg)+'.jpg', Pice)

def CreateOutFolder(PathToFolder, Name):
	if not os.path.isdir(PathToFolder + Name): os.mkdir(PathToFolder + Name)
	return PathToFolder + Name

PathImages = r'C:/Users/Etty.DESKTOP-B1CTQ9J/Desktop/Perry/Haar/test/'
lines = GetLines(PathImages+'_annotations.txt')

DataLines = []
for line in lines:
	line = line[::-1]
	for i in range(0,len(line)):
		if (ord(line[i])>96) and (ord(line[i])<123):
			StringPos = ''.join(reversed(line[0:i])) 
			ImgName = ''.join(reversed(line[i:len(line)]))
			DataLines.append((GetNumb(StringPos), ImgName)) 
			break

OutPath = CreateOutFolder(PathImages, 'OutFolder')

i = 0
for DataSet in DataLines:
	i += 1
	image = cv2.imread(PathImages + DataSet[1])  
	CutPiceOfImage(image, DataSet[0], DataSet[1])

cv2.waitKey(0)
cv2.destroyAllWindows()