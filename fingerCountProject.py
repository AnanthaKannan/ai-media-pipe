import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "fingerImages"
myList = os.listdir(folderPath)
myList.sort()
# print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

detector = htm.handDedector()
tipIds = [4, 8, 12, 16, 20];

while True:
    success, img_ = cap.read()
    img = cv2.flip(img_, 1)
    img = detector.findHands(img)
    lmList = detector.findPositon(img)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)


        h, w, c = overlayList[totalFingers-1].shape
        # print(h, w, c)
        img[0:h, 0:w] = overlayList[totalFingers-1]
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    cv2.imshow("Image", img)
    cv2.waitKey(1)