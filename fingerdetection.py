import cv2
import time
import os
import HandTrackingModule as htm
#import objectdetct as od

def fingerdetect():
	wCam , hCam = 640 , 480
	cap = cv2.VideoCapture(0)
	cap.set(3 ,wCam)
	cap.set(4,hCam)
	# folderPath = "fingerimage"
	# myList = os.listdir(folderPath)
	# print(myList)
	# overlayList = []
	# for imPath in myList:
	# 	image = cv2.imread(f'{folderPath}/{imPath}')
	# 	overlayList.append(image)
	#
	# print(len(overlayList))
	#   pTime = 0

	detector = htm.handDetector(detectionCon=0.75)

	tipIds = [4 ,8 ,12,16,20]
	while True :
		success , img = cap.read()
		img = detector.findHands(img)
		lmList = detector.findPosition(img,draw=False)
		#print(lmList)
		if len(lmList) !=0:
			finger =[]

			if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
				finger.append(1)
			else:
				finger.append(0)
			for id in range(1,5):
				if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
					finger.append(1)
				else:
					finger.append(0)

			totalFinger = finger.count(1)
			print(totalFinger)


		cv2.imshow("image", img)
		cv2.waitKey(1)
fingerdetect()