import random
from itertools import cycle
import cv2
import webcam
from PIL.ImageChops import offset
from contourpy.array import concat_offsets
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import time

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

# Game Variables
cx, cy = 250, 250
color = (255, 0, 255)
counter = 0
score = 0
timeStart = time.time()
totalTime = 30


# Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if time.time()-timeStart < totalTime:
        hands, img = detector.findHands(img)

        if hands:
            lmList = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']
            x1, y1 = lmList[5][:2]
            x2, y2 = lmList[17][:2]

            distance = int(math.sqrt( (y2-y1)**2 + (x2-x1)**2))
            A, B, C = coff
            distanceCM = A*distance**2 + B*distance + C

            if distanceCM < 40:
                if x < cx < x + w and y < cy < y + h:
                    counter  = 1


            #print (distanceCM, distance)
            cvzone.putTextRect(img,f'{int (distanceCM)} cm', (x+5, y-100))
        if counter:
            counter += 1
            color = (0, 255, 0)
            if counter == 3:
                cx = random.randint(100, 1100)
                cy = random.randint(100, 600)
                color = (255, 0, 255)
                score +=1
                counter = 0



        # Draw Button
        cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)
        cv2.circle(img, (cx, cy), 30, (50, 50, 50), 2)

        # Game HUD
        cvzone.putTextRect(img, f'Time: {int (totalTime - (time.time() - timeStart))}',
                           (1000, 75), scale = 3, offset=15)
        cvzone.putTextRect(img, f'Score: {str (score).zfill(2)}', (60, 75), scale = 3, offset=15)

    else:
        cvzone.putTextRect(img, 'Game Over', (400, 400), scale = 5, offset = 30, thickness = 7)
        cvzone.putTextRect(img, f'Your score: {score}', (450, 500), scale = 3, offset = 20)
        cvzone.putTextRect(img, f'Press R to restart:' , (460, 575), scale = 2, offset = 10)





    cv2.imshow("Image",img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        timeStart = time.time()
        score = 0
