
#pip install mediapipe==0.8.7
import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone #Version: 1.4.1
import numpy as np
import time


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8)
colorR=(255,0,255)
cx, cy, w, h = 100, 100, 200, 200
pTime=0



class DragRect():
    def __init__(self,posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size =size

    def update(self,cursor):
        cx,cy=self.posCenter
        w,h = self.size
           # when finger goes into that rectangle region
                #x coord          #y coord
        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
         
            self.posCenter=cursor


rectList =[]
for x in range(10):
    rectList.append(DragRect([x*250+150,x*250+150]))
        


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:

      
       

       

        l,_,_ = detector.findDistance(8 ,12 ,img,draw=False)# 8 is index and 12 is middle finger
        print(l)
        


        #(if length between the fingers<30 the block can be moved)
        if l<30:

            #x and y of the tip
            cursor=lmList[8] #8 is index fingertip
            #calling the cursor
            for rect in rectList:
                rect.update(cursor)

            # # when finger goes into that region
            #     #x coord          #y coord
            # if cx-w//2 <cursor[0] < cx+w//2 and cy-h//2 <cursor[1]< cy+h//2:
            #     colorR = 0,255,0 #green
            #     cx,cy=cursor

            # else:
            #     colorR=(255,0,255) #purple





    # draw solid Rectangle
    for rect in rectList:
        cx,cy=rect.posCenter
        w,h = rect.size
        cv2.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), colorR, cv2.FILLED)

     
        cvzone.cornerRect(img, (cx-w//2,cy-h//2,w,h ),20,rt=0)
        




 # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)



    #display
    cv2.imshow("Virtual Drag and Drop",img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
