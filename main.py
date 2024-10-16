import cv2
from contourpy.array import concat_offsets
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone

# Webcam
cap = cv2.VideoCapture(1)
cap.set(3,  1280)
cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Find Function
# x is the distance, y is the value in cm
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 70, 80, 85, 90, 95, 100]
coff= np.polyfit(x, y, 2) #y = Ax^2 + Bx + C



# Loop
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        x1, y1 = lmList[5][:2]
        x2, y2 = lmList[17][:2]

        distance = int(math.sqrt( (y2-y1)**2 + (x2-x1)**2))
        A, B, C = coff
        distanceCM = A*distance**2 + B*distance + C

        #print (distanceCM, distance)
        cvzone.putTextRect(img,f'{int (distanceCM)} cm', (x+5, y-100))

    cv2.imshow("Image",img)
    cv2.waitKey(1)