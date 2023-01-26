import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone


cap = cv2.VideoCapture(0)                               #to open the camera
cap.set(3, 1280)                                        # to set the width and height , 3-width
cap.set(4, 720)                                         # 4-height
detector = HandDetector(detectionCon=0.8)               # default detection value is 0.5 but we need better detection Confidence
colorR = 150, 1, 150
cx, cy, w, h = 100, 100, 200, 200

class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # if the finger tip is in rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            colorR = 0, 250, 0
            self.posCenter = cursor


rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150, 150]))
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)                       # find the hands inside the image
    lmList, _ = detector.findPosition(img)              # identify the finger tips

    if lmList:
        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        print(l)
        if l < 30:
            cursor = lmList[8]
            for rect in rectList:
                rect.update(cursor)

    # to draw the rectangle
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
       # cvzone.cornerRect(img, (cx - w // 2, cy - h // 2), w, h), 20, rt=0)

    cv2.imshow('Image', img)
    cv2.waitKey(1)


