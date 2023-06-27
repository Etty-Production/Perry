import os
import re
import numpy
import cv2

folder = r'C:/Users/Etty.DESKTOP-B1CTQ9J/Desktop/ImagesForXML/n'

def TransformImage(Image, Folder, file):
	Image = cv2.resize(Image, (126,126))
	cv2.imwrite(Folder+'/'+file, Image)

for f in os.listdir(folder):
	try:
		image = cv2.imread(folder + '/' + f)
		TransformImage(image, folder, f)
	except Exception as e:
		print(f,' Not Image! Dolboeb!')
