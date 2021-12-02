import cv2
import os
import mediapipe as mp
import HandTrackingModule as htm


class handDetector():
	def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
		self.mode = mode
		self.maxHands = maxHands
		self.detectionCon = detectionCon
		self.trackCon = trackCon

		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(self.mode, self.maxHands,
										self.detectionCon, self.trackCon)
		self.mpDraw = mp.solutions.drawing_utils

	def findHands(self, img, draw=True):
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(imgRGB)
		# print(results.multi_hand_landmarks)

		if self.results.multi_hand_landmarks:
			for handLms in self.results.multi_hand_landmarks:
				if draw:
					self.mpDraw.draw_landmarks(img, handLms,
											   self.mpHands.HAND_CONNECTIONS)
		return img

	def findPosition(self, img, handNo=0, draw=True):
		lmList = []
		if self.results.multi_hand_landmarks:
			myHand = self.results.multi_hand_landmarks[handNo]
			for id, lm in enumerate(myHand.landmark):
				# print(id, lm)
				h, w, c = img.shape
				cx, cy = int(lm.x * w), int(lm.y * h)
				#print(id)
				lmList.append([id, cx, cy])
				if draw:
					cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

		return lmList

	def FingerDetect(self,img):
		tipIds = [4, 8, 12, 16, 20]
		lmList = self.findPosition(img,draw=False)
		if len(lmList) != 0:
			finger = []

			if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
				finger.append(1)
			else:
				finger.append(0)
			for id in range(1, 5):
				if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
					finger.append(1)
				else:
					finger.append(0)

			totalFinger = finger.count(1)
			return totalFinger

def main():
	wCam, hCam = 640, 480
	cap = cv2.VideoCapture(0)
	cap.set(3, wCam)
	cap.set(4, hCam)
	detector = handDetector(detectionCon=0.75)
	#tipIds = [4, 8, 12, 16, 20]

	while True:
		success, img = cap.read()
		img=detector.findHands(img)
		lmList = detector.findPosition(img,draw=False)
		finger = detector.FingerDetect(img)



		cv2.imshow("image", img)
		cv2.waitKey(1)


if __name__=="__main__":
	main()