import cv2
import mediapipe as mp
import time

class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon = 0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.pTime = 0

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                     self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def getPosition(self, img):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y*h)
                lmList.append([id, cx, cy])
        return lmList

    def showFps(self, img):
        cTime = time.time()
        print(cTime, self.pTime)
        fbs = 1 / (cTime - self.pTime)
        pTime = cTime
        cv2.putText(img, str(int(fbs)), (70, 80), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

def main():
    wCam, hCam = 640, 480
    # cap = cv2.VideoCapture('videos/body.mp4')
    detector = poseDetector()
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        # print(lmList)
        detector.showFps(img)
        cv2.imshow("Image", img)
        cv2.waitKey(12)


if __name__ == "__main__":
    main()