import cv2 as cv
import time
import cvzone
from cvzone.HandTrackingModule import HandDetector
from math import sqrt

# Camera settings
cap = cv.VideoCapture(0)
cap_w = 1280
cap_h = 720
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector()

# Color 

green = (0,255,0)
dark = (0,0,0)
white = (255,255,255)
red = (255,0,255)

# Hand text postion
handtxt = (1070,30)

pTime = 0
cTime = 0
image = cv.imread("radiologie_pouce.jpg")


ishape = image.shape
ix,iy = ishape[1], ishape[0]

nsize = (ix//3,iy//3)
image = cv.resize(image,nsize, interpolation=cv.INTER_CUBIC)

ox,oy = 50,50

t0 = 1 
t1 = 2

pointsList = []


# Display
while True:
    _, img = cap.read()
    img = cv.flip(img,1)
    hands, img = detector.findHands(img, flipType=False, draw=True)
   

    # Corner rect

    # Horizontal line
    xh_left = cv.line(img,(50,10),(20,10),white,t0)
    yh_left = cv.line(img,(50,680),(20,680),white,t0)
    xh_right = cv.line(img,(1215,680),(1250,680),white,t0)
    yh_right = cv.line(img,(1215,10),(1250,10),white,t0)
    # Vertical line
    xv_left = cv.line(img,(20,10),(20,35),white,t0)
    yv_left = cv.line(img,(20,655),(20,680),white,t0)
    xv_right = cv.line(img,(1250,655),(1250,680),white,t0)
    yv_right = cv.line(img,(1250,10),(1250,35),white,t0)

    h,w, _= image.shape
    

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        rect = cv.rectangle(img,(20,680),(1250,10),white,0)

        cv.circle(img,(lmList[8][0],lmList[8][1]),10,green,cv.FILLED)

        #========================Image rect==============================#

        if ox < cursor[0] < ox+w and oy < cursor[1] < oy+h:
            ox,oy = cursor[0]-w//2,cursor[1]-h//2

        if cursor in rect:
            # Horizontal line
            xh_left = cv.line(img,(50,10),(20,10),green,t1)
            yh_left = cv.line(img,(50,680),(20,680),green,t1)
            xh_right = cv.line(img,(1215,680),(1250,680),green,t1)
            yh_right = cv.line(img,(1215,10),(1250,10),green,t1)

            # Vertical line
            xv_left = cv.line(img,(20,10),(20,35),green,t1)
            yv_left = cv.line(img,(20,655),(20,680),green,t1)
            xv_right = cv.line(img,(1250,655),(1250,680),green,t1)
            yv_right = cv.line(img,(1250,10),(1250,35),green,t1)

            if len(hands)==2:
                cv.putText(img,f'0{len(hands)} hand(s) detected', handtxt, cv.FONT_HERSHEY_DUPLEX, 0.5,green,1)
            elif len(hands)==1:
                cv.putText(img,f'0{len(hands)} hand detected', handtxt, cv.FONT_HERSHEY_DUPLEX, 0.5,green,1)
            else :
                cv.putText(img,f'0{len(hands)} hand(s) detected', handtxt, cv.FONT_HERSHEY_DUPLEX, 0.5,red,1)

    else:
        cv.putText(img,'No hand(s) detected', handtxt, cv.FONT_HERSHEY_DUPLEX, 0.5,red,1)

    img[oy:oy+h,ox:ox+w] = image
    

    # Fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


    # Display image
    cv.imshow(f'X-er! Powered by FILEUS', img)
    # Break
    key = cv.waitKey(1) & 0xFF
    if key == ord("q") or key == ord("Q"):
        break

cap.release()
cv.destroyAllWindows()