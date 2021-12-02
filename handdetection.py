import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hand = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


while True:
	success, img = cap.read()
	hello = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	print(hello)
	results = hand.process(hello)

	#if results.multi_hand_landmarks:
		#for handLms in results.multi_hand_landmarks:
		#	mpDraw.draw_landmarks(img, handLms)



	cv2.imshow("image" , img)
	cv2.waitKey(1)
