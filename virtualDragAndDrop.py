import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

detector = HandDetector(detectionCon=0.8)
colorR = (0, 255, 255)
# cx, cy, w, h = 100, 100, 200, 200

class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        x1, y1, x2, y2 = cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2
        if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
            # colorR = (0, 255, 0)
            self.posCenter = cursor

rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:
        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        if l < 30:
            cursor = lmList[8]
            for rect in rectList:
                rect.update(cursor)
    # Drag solid
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size
    #     x1, y1, x2, y2 = cx-w//2, cy-h//2, cx+w//2, cy+h//2
    #     cv2.rectangle(img, (x1, y1), (x2, y2), colorR, cv2.FILLED)
        # cvzone.cornerRect(img, (cx-w//2, cy-h//2, w, h), 20, rt=0)

    ## Draw Transperency
    imgNew = np.zeros_like(img)
    count = 0
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        x1, y1, x2, y2 = cx-w//2, cy-h//2, cx+w//2, cy+h//2
        cv2.rectangle(imgNew, (x1, y1), (x2, y2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx-w//2, cy-h//2, w, h), 20, rt=0)
        myName = ["A", "A", "K", "N", "N"]
        cv2.putText(imgNew, myName[count], (x1+60, y2-60), cv2.FONT_HERSHEY_SIMPLEX, 5, (36, 255, 12), 5)
        count = count + 1

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Image", out)
    cv2.waitKey(1)