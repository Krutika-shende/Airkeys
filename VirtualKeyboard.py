import cv2 as cv
from HandTrackingModule import *
from pynput.keyboard import Controller, Key
from baseMain import *

wCam = 640
hCam = 480
frameR = int(wCam/10) 
wTotal = wCam - 2*(frameR) 
size = int(wCam / 16) 
space = int((wTotal - 10*size)/10) 

capsX=0
capsX1=0
capsY=0
capsY1=0
spaceX=0
spaceX1=0
spaceY=0
spaceY1=0
exitX=0
exitX1=0
exitY=0
exitY1=0
enterKeyX=0
enterKeyX1=0
enterKeyY=0
enterKeyY1=0
backspaceX=0
backspaceX1=0
backspaceY=0
backspaceY1=0
click =0

caps = False 
close = False

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
keysLOW = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
        ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]]


class KEY:
    def __init__(self,pos,size,text):
        self.pos = pos
        self.text = text
        self.size = size

def keyClass(keys):
    global size
    global space
    Buttons = []
    for row in range(len(keys)):
        y1 = frameR +((row)*(size+space))
        for i, keyALPHA in enumerate(keys[row]):
            x1=frameR +((i)*(size+space))
            Buttons.append(KEY([x1,y1],[x1+size,y1+size],keyALPHA))

    return Buttons

def DrawKey(img1 , buttons1):
    global capsX, capsX1, capsY, capsY1
    global spaceX, spaceX1, spaceY, spaceY1
    global exitX, exitX1, exitY, exitY1
    global enterKeyX, enterKeyX1, enterKeyY, enterKeyY1
    global backspaceX, backspaceX1, backspaceY, backspaceY1

    for button1 in buttons1:
        x,y = button1.pos
        key2 = button1.text
        w,h = button1.size
        cv.rectangle(img1, (x,y), (w,h), (255, 0, 0), cv.FILLED)
        cv.putText(img1,key2,(x+int((size/2)-(size/4)),y+int((size/2)+(size/4))),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),thickness=4)

    cv.rectangle(img1,(frameR-int(size/6),frameR-int(size/6)),(frameR +((10)*(size+space)+int(size/6)-space),frameR +((3)*(size+space)-space)+int(size/6)),(20,60,70),thickness=2)

    # SPECIAL BUTTONS

    # row coordinates
    step = size + space

    row1Y = frameR + 3 * step 
    row1Y1 = row1Y + size  

    row2Y = row1Y + step 
    row2Y1 = row2Y + size

    # CAPS

    capsX = frameR
    capsY = row1Y

    capsX1 = capsX + (2 * (size + space)) - space
    capsY1 = row1Y1

    cv.rectangle(img1, (capsX, capsY),
                (capsX1, capsY1),
                (255, 0, 0), cv.FILLED)

    cv.putText(
        img1,
        "Caps",
        (capsX + 18, capsY + 33),
        cv.FONT_ITALIC,
        0.8,
        (255, 255, 255),
        2
    )

    # SPACE

    spaceX = capsX1 + space
    spaceY = row1Y

    spaceX1 = spaceX + (3 * (size + space)) - space
    spaceY1 = row1Y1

    cv.rectangle(img1, (spaceX, spaceY),
                (spaceX1, spaceY1),
                (255, 0, 0), cv.FILLED)

    cv.putText(
        img1,
        "Space",
        (spaceX + 35, spaceY + 33),
        cv.FONT_ITALIC,
        0.8,
        (255, 255, 255),
        2
    )

    # ENTER

    enterKeyX = spaceX1 + space
    enterKeyY = row1Y

    enterKeyX1 = enterKeyX + (2 * (size + space)) - space
    enterKeyY1 = row1Y1

    cv.rectangle(img1, (enterKeyX, enterKeyY),
                (enterKeyX1, enterKeyY1),
                (255, 0, 0), cv.FILLED)

    cv.putText(
        img1,
        "Enter",
        (enterKeyX + 18, enterKeyY + 33),
        cv.FONT_ITALIC,
        0.8,
        (255, 255, 255),
        2
    )

    # BACKSPACE

    backspaceX = enterKeyX1 + space
    backspaceY = row1Y

    backspaceX1 = backspaceX + (3 * (size + space)) - space
    backspaceY1 = row1Y1

    cv.rectangle(img1, (backspaceX, backspaceY),
                (backspaceX1, backspaceY1),
                (255, 0, 0), cv.FILLED)

    cv.putText(
        img1,
        "Backspace",
        (backspaceX + 8, backspaceY + 33),
        cv.FONT_ITALIC,
        0.7,
        (255, 255, 255),
        2
    )

    # EXIT

    exitX = frameR + 4 * (size + space) + 12
    exitY = row2Y

    exitX1 = exitX + (2 * (size + space)) - space
    exitY1 = row2Y1

    cv.rectangle(img1, (exitX, exitY),
                (exitX1, exitY1),
                (255, 0, 0), cv.FILLED)

    cv.putText(
        img1,
        "Exit",
        (exitX + 20, exitY + 33),
        cv.FONT_ITALIC,
        0.8,
        (255,255,255),
        2
    )
    return img1


def run_keyboard(img, buttonsUP, buttonsLOW, detector):
    keyboard = Controller()
    global close
    global click
    global caps
    global enterKeyX, enterKeyX1, enterKeyY, enterKeyY1
    global backspaceX, backspaceX1, backspaceY, backspaceY1

    imgCopy = img.copy()
    if caps :
        imgKEY = DrawKey(img,buttonsUP)
        buttons = buttonsUP
    else:
        imgKEY = DrawKey(img, buttonsLOW)
        buttons = buttonsLOW

    detector.findhands(imgCopy)
    lmlist , bbox = detector.findPosition(imgCopy)

    img3 = cv.bitwise_and(imgKEY, imgCopy)

    if len(lmlist)!=0:
        fingers = detector.fingersUp()
        if fingers[1]==1:
            xIndex , yIndex = lmlist[8][1],lmlist[8][2]

            # space
            if spaceX < xIndex < spaceX1 and spaceY < yIndex < spaceY1:
                cv.rectangle(img3, (spaceX, spaceY),(spaceX1, spaceY1),(200, 255, 0), cv.FILLED)

                cv.putText(
                    img3,
                    "Space",
                    (spaceX + 35, spaceY + 33),
                    cv.FONT_ITALIC,
                    0.8,
                    (255, 255, 255),
                    2
                )

                if fingers[2] == 1:
                    l, b = detector.findDistance(8, 12, imgCopy)
                    if l < 50:
                        click = 1
                    if click:
                        click += 1
                        cv.rectangle(img3, (spaceX, spaceY),
                                    (spaceX1, spaceY1),
                                    (0, 255, 0), cv.FILLED)

                        cv.putText(
                            img3,
                            "Space",
                            (spaceX + 35, spaceY + 33),
                            cv.FONT_ITALIC,
                            0.8,
                            (255, 255, 255),
                            2
                        )

                    if click >= 3 and l > 50:
                        keyboard.press(" ")
                        click = 0

            # capslock
            if capsX < xIndex < capsX1 and capsY < yIndex < capsY1:
                cv.rectangle(img3, (capsX, capsY),
                            (capsX1, capsY1),
                            (200, 255, 0), cv.FILLED)

                cv.putText(
                    img3,
                    "Caps",
                    (capsX + 18, capsY + 33),
                    cv.FONT_ITALIC,
                    0.8,
                    (255, 255, 255),
                    2
                )
                if fingers[2] == 1:
                    l, b = detector.findDistance(8, 12, imgCopy)
                    if l < 50:
                        click = 1
                    if click:
                        click += 1
                        cv.rectangle(img3, (capsX, capsY),
                                    (capsX1, capsY1),
                                    (0, 255, 0), cv.FILLED)

                        cv.putText(
                            img3,
                            "Caps",
                            (capsX + 18, capsY + 33),
                            cv.FONT_ITALIC,
                            0.8,
                            (255, 255, 255),
                            2
                        )
                    if click >= 3 and l > 50:
                        click = 0
                        if caps:
                            caps = False
                        else:
                            caps = True

            # exit
            if exitX < xIndex < exitX1 and exitY < yIndex < exitY1:
                cv.rectangle(img3, (exitX, exitY),
                (exitX1, exitY1),
                (200, 255, 0), cv.FILLED)

                cv.putText(
                    img3,
                    "Exit",
                    (exitX + 20, exitY + 33),
                    cv.FONT_ITALIC,
                    0.8,
                    (200, 255, 0),
                    2
                )
                if fingers[2] == 1:
                    l, b = detector.findDistance(8, 12, imgCopy)
                    if l < 50:
                        click = 1
                    if click:
                        click += 1
                        cv.rectangle(img3, (exitX, exitY),
                                        (exitX1, exitY1),
                                        (0, 255, 0), cv.FILLED)

                        cv.putText(
                            img3,
                            "Exit",
                            (exitX + 20, exitY + 33),
                            cv.FONT_ITALIC,
                            0.8,
                            (255,255,255),
                            2
                        )
                    if click >= 3 and l > 50:
                        close = True
                        click = 0
                        return img3, "menu"

            # enter
            if enterKeyX < xIndex < enterKeyX1 and enterKeyY < yIndex < enterKeyY1:
                cv.rectangle(img3, (enterKeyX, enterKeyY),
                            (enterKeyX1, enterKeyY1),
                            (200, 255, 0), cv.FILLED)

                cv.putText(
                    img3,
                    "Enter",
                    (enterKeyX + 18, enterKeyY + 33),
                    cv.FONT_ITALIC,
                    0.8,
                    (255, 255, 255),
                    2
                )
                if fingers[2] == 1:
                    l, b = detector.findDistance(8, 12, imgCopy)
                    if l < 50:
                        click = 1
                    if click:
                        click += 1
                        cv.rectangle(img3, (enterKeyX, enterKeyY),
                                    (enterKeyX1, enterKeyY1),
                                    (0, 255, 0), cv.FILLED)

                        cv.putText(
                            img3,
                            "Enter",
                            (enterKeyX + 18, enterKeyY + 33),
                            cv.FONT_ITALIC,
                            0.8,
                            (255, 255, 255),
                            2
                        )
                    if click >= 3 and l > 50:
                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)
                        click = 0

            # backspace
            if backspaceX < xIndex < backspaceX1 and backspaceY < yIndex < backspaceY1:
                cv.rectangle(img3, (backspaceX, backspaceY),
                            (backspaceX1, backspaceY1),
                            (200, 255, 0), cv.FILLED)

                cv.putText(
                    img3,
                    "Backspace",
                    (backspaceX + 8, backspaceY + 33),
                    cv.FONT_ITALIC,
                    0.7,
                    (255, 255, 255),
                    2
                )
                if fingers[2] == 1:
                    l, b = detector.findDistance(8, 12, imgCopy)
                    if l < 50:
                        click = 1
                    if click:
                        click += 1
                        cv.rectangle(img3, (backspaceX, backspaceY),
                                    (backspaceX1, backspaceY1),
                                    (0, 255, 0), cv.FILLED)

                        cv.putText(
                            img3,
                            "Backspace",
                            (backspaceX + 8, backspaceY + 33),
                            cv.FONT_ITALIC,
                            0.7,
                            (255, 255, 255),
                            2
                        )
                    if click >= 3 and l > 50:
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                        click = 0

            # alpha keys
            for button in buttons:
                x,y = button.pos
                w,h = button.size
                key = button.text

                if x<xIndex<w and y<yIndex<h:
                    cv.rectangle(img3, (x-int(space/4), y-int(space/4)), (w+int(space/4), h+int(space/4)), (200, 255, 0), cv.FILLED)
                    cv.putText(img3, key, (x + int(space), y + int(3*space)), cv.FONT_ITALIC, 1, (255, 255, 255), thickness=3)
                    if fingers[2]==1:
                        l , b = detector.findDistance(8,12,imgCopy)
                        if l<50 :
                            click =1
                        if click:
                            click +=1
                            cv.rectangle(img3, (x - int(space / 4)-int(space/3), y - int(space / 4)-int(space/3)),(w + int(space / 4) + int(space/3), h + int(space / 4)+ int(space/3)), (0, 255, 0), cv.FILLED)
                            cv.putText(img3, key, (x + int(space), y + int(3 * space)), cv.FONT_ITALIC, 1,(255, 255, 255), thickness=3)
                        if click>=3 and l>50:
                            keyboard.press(key)
                            keyboard.release(key)
                            click=0

    return img3, "keyboard"