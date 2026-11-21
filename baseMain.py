import VirtualMouse
from VirtualMouse import *
import cv2 as cv
from HandTrackingModule import *
import VirtualKeyboard
from VirtualKeyboard import *
import autopy

cap =cv.VideoCapture(0)
wCamera =640 
hCamera =480
cap.set(3,wCamera)
cap.set(4,hCamera)
sucess , imgShape = cap.read()
wCamera = imgShape.shape[1]
hCamera = imgShape.shape[0]
space = int(hCamera/23)
clickc = 0

def main():
    global clickc
    global space
    global wCamera
    global hCamera
    global cap
    
    mode = "menu"
    buttonsUP = VirtualKeyboard.keyClass(VirtualKeyboard.keys)
    buttonsLOW = VirtualKeyboard.keyClass(VirtualKeyboard.keysLOW)

    detector = HandDetector(maxHand=1)
    while True:
        success , img = cap.read()
        img = cv.flip(img , 1)
        imgcopy = img.copy()

        if mode == "menu":
            cv.setWindowTitle("AirKeys - Main Menu", "AirKeys - Main Menu")
            cv.setWindowProperty("AirKeys - Main Menu", cv.WND_PROP_TOPMOST, 1)
            cv.setWindowProperty("AirKeys - Main Menu", cv.WND_PROP_TOPMOST, 0)

            # mouse
            
            cv.rectangle(img, (space, int(hCamera/4)-space), (int(wCamera/2)-space, hCamera-space), (255, 0, 0), cv.FILLED)
            cv.putText(img, "Mouse", (int(wCamera/4)-2*space, int(hCamera/2)+2*space), cv.FONT_ITALIC, 1, (255, 255, 255), thickness=3)
            
            # key
            
            cv.rectangle(img, (int(wCamera/2)+space, int(hCamera/4)-space), (wCamera-space, hCamera-space), (255, 0, 0), cv.FILLED)
            cv.putText(img, "Keyboard", (int(wCamera/2)+4*space, int(hCamera/2)+2*space), cv.FONT_ITALIC, 1, (255, 255, 255), thickness=3)
            
            # exit

            cv.rectangle(img, (space, space), (int(wCamera/2)-space, int(hCamera/6)), (255,0,0), cv.FILLED)
            cv.putText(img, "Exit", (int(wCamera/4)-2*space, int(hCamera/8)), cv.FONT_ITALIC, 1, (255,255,255), thickness=3)
            
            # instructions

            cv.rectangle(img, (int(wCamera/2)+space, space), (wCamera-space, int(hCamera/6)), (255,0,0), cv.FILLED)
            cv.putText(img, "Instructions", (int(wCamera/2)+4*space, int(hCamera/8)), cv.FONT_ITALIC, 1, (255,255,255), thickness=3)            

            detector.findhands(imgcopy)
            lmlist, bbox = detector.findPosition(imgcopy)

            if len(lmlist)!=0:
                fingers = detector.fingersUp()
                if fingers[1]==1:
                    xIndex , yIndex = lmlist[8][1],lmlist[8][2]

                    # keyboard hover color logic
                    if int(wCamera/2)+space < xIndex < wCamera-space and int(hCamera/4)-space < yIndex < hCamera-space:
                        cv.rectangle(img, (int(wCamera/2)+space, int(hCamera/4)-space), (wCamera-space, hCamera-space), (200, 255, 0), cv.FILLED)
                        cv.putText(img, "Keyboard", (int(wCamera/2)+4*space, int(hCamera/2)+2*space), cv.FONT_ITALIC, 1, (255, 255, 255), thickness=5)
                        
                        if fingers[2] == 1:
                            l, b = detector.findDistance(8, 12, imgcopy)
                            if l < 50:
                                clickc = 1

                            if clickc:
                                clickc += 1
                                cv.rectangle(img, (int(wCamera/2)+space, int(hCamera/4)-space), (wCamera-space, hCamera-space), (0, 255, 0), cv.FILLED)
                                cv.putText(img, "Keyboard", (int(wCamera/2)+4*space, int(hCamera/2)+2*space), cv.FONT_ITALIC, 1, (255, 255, 255), thickness=5)

                            if clickc >= 3 and l > 50:
                                clickc = 0
                                mode = "keyboard"

                    # mouse hover color logic
                    if space < xIndex < int(wCamera/2)-space and int(hCamera/4)-space < yIndex < hCamera-space:
                       
                        cv.rectangle(img, (space, int(hCamera/4)-space), (int(wCamera/2)-space, hCamera-space), (200, 255, 0), cv.FILLED)
                        cv.putText(img, "Mouse", (int(wCamera/4)-2*space, int(hCamera/2)+2*space), cv.FONT_ITALIC, 1, (255, 255, 255), thickness=5)
                        if fingers[2] == 1:    
                            l, b = detector.findDistance(8, 12, imgcopy)
                            if l < 50:
                                clickc = 1

                            if clickc:
                                clickc += 1
                                cv.rectangle(img, (space, int(hCamera/4)-space), (int(wCamera/2)-space, hCamera-space), (0, 255, 0), cv.FILLED)
                                cv.putText(img, "Mouse", (int(wCamera/4)-2*space, int(hCamera/2)+2*space), cv.FONT_ITALIC, 1, (255, 255, 255), thickness=5)
                            
                            if clickc >= 3 and l > 50:
                                clickc = 0
                                mode = "mouse"
                    
                    # instructions hover color logic
                    if int(wCamera/2)+space < xIndex < wCamera-space and space < yIndex < int(hCamera/6):
                        
                        cv.rectangle(img, (int(wCamera/2)+space, space), (wCamera-space, int(hCamera/6)), (200,255,0), cv.FILLED)
                        cv.putText(img, "Instructions", (int(wCamera/2)+4*space, int(hCamera/8)), cv.FONT_ITALIC, 1, (255,255,255), thickness=5)
                        
                        if fingers[2] == 1:
                            l, b = detector.findDistance(8, 12, imgcopy)
                            if l < 50:
                                clickc = 1
                            
                            if clickc:
                                clickc += 1
                                cv.rectangle(img, (int(wCamera/2)+space, space), (wCamera-space, int(hCamera/6)), (0,255,0), cv.FILLED)
                                cv.putText(img, "Instructions", (int(wCamera/2)+4*space, int(hCamera/8)), cv.FONT_ITALIC, 1, (255,255,255), thickness=5)
                            
                            if clickc >= 3 and l > 50:
                                clickc = 0
                                mode = "instructions"

                    # exit hover color and exit logic
                    if space < xIndex < int(wCamera/2)-space and space < yIndex < int(hCamera/6):
                        cv.rectangle(img, (space, space), (int(wCamera/2)-space, int(hCamera/6)), (200,255,0), cv.FILLED)
                        cv.putText(img, "Exit", (int(wCamera/4)-2*space, int(hCamera/8)), cv.FONT_ITALIC, 1, (255,255,255), thickness=5)
                        
                        if fingers[2] == 1:
                            l, b = detector.findDistance(8, 12, imgcopy)
                            if l < 50:
                                clickc = 1
                            
                            if clickc:
                                clickc += 1
                                cv.rectangle(img, (space, space), (int(wCamera/2)-space, int(hCamera/6)), (0,255,0), cv.FILLED)
                                cv.putText(img, "Exit", (int(wCamera/4)-2*space, int(hCamera/8)), cv.FONT_ITALIC, 1, (255,255,255), thickness=5)
                            
                            if clickc >= 3 and l > 50:
                                cap.release()
                                cv.destroyAllWindows()
                                return

        elif mode == "mouse":
            cv.setWindowTitle("AirKeys - Main Menu", "Virtual Mouse")
            img, mode = VirtualMouse.run_mouse(img, detector)

        elif mode == "keyboard":
            cv.setWindowTitle("AirKeys - Main Menu", "Virtual Keyboard")
            cv.setWindowProperty("AirKeys - Main Menu", cv.WND_PROP_TOPMOST, 1)
            #cv.setWindowProperty("AirKeys - Main Menu", cv.WND_PROP_TOPMOST, 0)
            if leftClickDone:
                autopy.mouse.move(lastClickX, lastClickY)
                autopy.mouse.click()
            img, mode = VirtualKeyboard.run_keyboard(img, buttonsUP, buttonsLOW, detector)

        elif mode == "instructions":
            cv.setWindowTitle("AirKeys - Main Menu", "Instructions")

            img[:] = ( 255, 255, 255)
            cv.putText(img, "MOUSE GESTURES", (60,120), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 3)
            instructions = [
                "Index finger -> Move mouse",
                "Index + middle pinch -> Left click",
                "Thumb + index pinch -> Right click",
                "4 fingers -> Scroll",
                "Closed hand / fist -> Exit",
            ]
            y = 160
            for text in instructions:
                cv.putText(img, text, (60,y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                y += 35
            
            cv.putText(img, "KEYBOARD GESTURES", (60,350), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 3)
            instructions = [
                "Index finger -> Move over Keyboard",
                "Index + middle pinch -> Click"
            ]
            y = 400
            for text in instructions:
                cv.putText(img, text, (60,y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                y += 35
            
            # BACK BUTTON
            cv.rectangle(img, (220, 20), (420, 80), (255,0,0), cv.FILLED)
            cv.putText( img, "BACK", (275,60), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
            detector.findhands(imgcopy)
            lmlist, bbox = detector.findPosition(imgcopy)
            if len(lmlist) != 0:
                fingers = detector.fingersUp()
                if fingers[1] == 1:
                    xIndex, yIndex = lmlist[8][1], lmlist[8][2]
                    # hover effect
                    if 220 < xIndex < 420 and 20 < yIndex < 80:
                        cv.rectangle( img, (220, 20), (420, 80), (200,255,0), cv.FILLED)
                        cv.putText( img, "BACK", (275,60), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
                        if fingers[2] == 1:
                            l, b = detector.findDistance(8, 12, imgcopy)
                            if l < 50:
                                clickc = 1
                            if clickc:
                                clickc += 1
                                cv.rectangle(img, (220, 20), (420, 80), (0,255,0), cv.FILLED)
                                cv.putText( img, "BACK", (275,60), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 5)
                            if clickc >= 3 and l > 50:
                                clickc = 0
                                mode = "menu"


        imgNew = cv.bitwise_and(img , imgcopy)
        cv.imshow("AirKeys - Main Menu", imgNew)
        if cv.waitKey(1) & 0xFF==ord('q'):
            break

if __name__ == "__main__":
    main()