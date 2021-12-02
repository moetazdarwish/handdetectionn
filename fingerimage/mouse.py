import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
###################
wCam , hCam = 640,480
frameR = 100
smoothening = 10
###################
plocX , plocY = 0,0
clocX , clocY =0,0
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetector(maxHands=1)
wScr , hScr = autopy.screen.size()

while True:
    #### 1. Find hand Landmarkes
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)

    # get the tip of index and middle Fingure
    if len(lmlist) != 0:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]

   ### check which finger up
        fingers = detector.fingersUp()

        # only index finger moving mode
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 0), 2)
        if fingers[1]==1 and fingers[2]==0:
        #convert coordicates

            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(x1,(frameR,hCam-frameR),(0,hScr))
            # smoothen values
            clocX = plocX + (x3 -plocX) / smoothening
            clocY = plocY + (y3 -plocY) / smoothening


            # move mouse
            autopy.mouse.move(wScr-clocX,hScr-clocY)
            cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
            plocX , plocY = clocX, clocY


        # both index and middile finger up : clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            length , img , lineinfo =detector.findDistance(8,12,img)
            print(length)
            if length < 30:
                cv2.circle(img,(lineinfo[4],lineinfo[5]),
                           10,(0,255,0),cv2.FILLED)
                autopy.mouse.click()


    # find distance between finger

    # click mouse if distance short

    # frame rate

    # display

    cv2.imshow("image" , img)
    cv2.waitKey(1)

