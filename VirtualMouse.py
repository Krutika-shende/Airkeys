import cv2 as cv
import numpy as np
import autopy
import pyautogui

wCam , hCam = 640,480
wScr , hScr = autopy.screen.size()

smootheing = 5

plocX , plocY = 0, 0
clocX , clocY = 0,0

# Click flags
rightClickDone = False
leftClickDone = False
lastClickY = 0
lastClickX = 0
prevZoomDistance = 0
frameR = int(hCam/3.2)
frameRx = frameR+int((frameR)/4)

#def Mouse(img):
def run_mouse(img, detector):
    global prevZoomDistance
    global frameR
    global smootheing
    global plocX
    global plocY
    global clocX
    global clocY
    global wScr
    global wCam
    global hScr
    global hCam
    global rightClickDone
    global leftClickDone
    global lastClickX
    global lastClickY

    detector.findhands(img)
    lmlist, bbox = detector.findPosition(img)
    cv.rectangle( img, (frameRx, frameR), (wCam - frameRx, hCam - frameR), (255, 0, 255), 2)

    if len(lmlist) != 0:
        Xindex, Yindex = lmlist[8][1], lmlist[8][2]
        Xmiddle, Ymiddle = lmlist[12][1], lmlist[12][2]
        fingers = detector.fingersUp()

        # MOVE MOUSE
        if fingers[1] == 1 and fingers[2] == 0:
            xMOUSE = np.interp(Xindex, (frameRx, wCam - frameRx), (0, wScr))
            yMOUSE = np.interp(Yindex, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (xMOUSE - plocX) / smootheing
            clocY = plocY + (yMOUSE - plocY) / smootheing
            autopy.mouse.move(clocX, clocY)
            cv.circle( img, (Xindex, Yindex), 15, (20, 180, 90), cv.FILLED)
            plocX, plocY = clocX, clocY

        # LEFT CLICK
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            length, bbox = detector.findDistance(8, 12, img)
            if length < 60 and not leftClickDone:
                autopy.mouse.click()
                lastClickX = clocX
                lastClickY = clocY
                cv.circle( img, (Xindex, Yindex), 15, (0, 255, 0), cv.FILLED)
                leftClickDone = True
        else:
            leftClickDone = False

        # RIGHT CLICK
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            rightLength, bbox = detector.findDistance(4, 8, img)
            if rightLength < 70 and not rightClickDone:
                autopy.mouse.click(button=autopy.mouse.Button.RIGHT)
                rightClickDone = True
        else:
         rightClickDone = False

        # SCROLL
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            cv.circle( img, (Xindex, Yindex), 15, (255, 0, 0), cv.FILLED)
            if Yindex < hCam // 2:
                pyautogui.scroll(50)     # scroll up
            else:
                pyautogui.scroll(-50)    # scroll down

        # EXIT
        if fingers == [0, 0, 0, 0, 0]:
            return img, "menu"

    return img, "mouse"
