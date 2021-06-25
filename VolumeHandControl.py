import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDedector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
print(volume.GetVolumeRange())
# volume.SetMasterVolumeLevel(-20.0, None)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPositon(img)
    if len(lmList) != 0:
        print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        lenght = math.hypot(x2 - x1, y2 - y1)
        print(lenght)

        if lenght < 50 :
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

    cv2.imshow('Img', img)
    cv2.waitKey(1)