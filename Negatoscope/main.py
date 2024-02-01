import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from time import sleep

# Camera settings
cap = cv.VideoCapture(0)
detector = HandDetector()

# Color
green = (0,255,0)
dark = (0,0,0)
white = (255,255,255)
red = (255,0,255)


p0, p1 = (0, 720), (1280, 0)

handtxt = (10,30) # position du text descriptif des actions


# Images
image = cv.imread("radiologie_pouce.jpg")
ishape = image.shape
ix,iy = ishape[1], ishape[0]

nsize = (ix//4,iy//4)
image = cv.resize(image,nsize, interpolation=cv.INTER_CUBIC)
ox,oy = 50,50

def pointer():
    cv.circle(img,(lmList[8][0],lmList[8][1]),10,green,cv.FILLED)

while True:
    _,img = cap.read()
    img = cv.flip(img, 1)
    hands, img = detector.findHands(img, draw=True)

    h,w, _= image.shape
    img[oy:oy+h,ox:ox+w] = image
    
    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        
        # l'index pour pointer
        if detector.fingersUp(hands[0])==[0,1,0,0,0]:
            pointer()

            cv.line(img,(0,0),(0,0),green, thickness=1)
            cv.putText(img,f'Pointer', handtxt, cv.FONT_HERSHEY_DUPLEX, 0.8,green,1)
            print("pointer")

        # Dux doigt pour doigts pour deplacer (le second  et le troisième doigt)
        elif detector.fingersUp(hands[0])==[0,1,1,0,0]:
            if ox < cursor[0] < ox+w and oy < cursor[1] < oy+h:
                ox,oy = cursor[0]-w//2,cursor[1]-h//2
            cv.putText(img,f'Grab', handtxt, cv.FONT_HERSHEY_DUPLEX, 0.8,green,1)
            print("grab")
    
        # Quatre doigts pour Zoomer (le second le troisième le quatrieme et le cinquieme doigt)
        elif detector.fingersUp(hands[0])==[0,1,1,1,1]:
            scale = 4
            
            if detector.fingersUp(hands[0])==[0,1,1,1,1]:
                scaleUp = scale - 1 
                newH, newW = ix//scaleUp, iy//scaleUp
                image = cv.resize(image, (newH,newW))
                print("Zoomed!!!!")
                cv.putText(img,f'Zoom In', handtxt, cv.FONT_HERSHEY_DUPLEX, 0.8,green,1)

        # Trois doigts pour deZoomer (le second le troisième et le quatrieme doigt)
        elif detector.fingersUp(hands[0])==[0,1,1,1,0]:
            newH, newW = ix//5, iy//5
            image = cv.resize(image, (newH,newW))
            print("Zoom --")
            cv.putText(img,f'Zoom Out', handtxt, cv.FONT_HERSHEY_DUPLEX, 0.8,green,1)

        
        # Trois doigts pour Stoper (le troisième le quatrieme et le cinquieme doigt)
        elif detector.fingersUp(hands[0])==[0,0,1,1,1]:
            print("Stoping....")
            cv.putText(img,f'Stoping:...', handtxt, cv.FONT_HERSHEY_DUPLEX, 0.8,green,1)
            sleep(5)
            cv.rectangle(img, p0, p1, white, cv.FILLED)
            sleep(2)
            break
            

        else:
            print('waiting....')
    else:
        print("No hand(s) detected")
        

    cv.imshow("", img)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('Q'):
        break

cap.release()
cv.destroyAllWindowsWindows()
