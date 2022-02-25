# DevFest 2021
# Project "Borne à dons"

import cv2 # for video capture
import time # for counting seconds to vote
import VotingBooth_functions as vbf # for additional functions
import datetime # for tagging dates on votes
import hashlib # for encrypting QR codes

# We store all results in a file on the local system
file = open('data.csv', 'a+')

# We set parameters for hand detector
detector = vbf.handDetector(detectionCon=0.75)

# For the tipIds, we take the tip of each finger
# figure 2.21 in https://google.github.io/mediapipe/solutions/hands.html
tipIds = [4, 8, 12, 16, 20]

# We get the video capture running
camera = cv2.VideoCapture(0)
camera.set(3,1024) # 3 = width
camera.set(4,768) # 4 = height

# Continuous analysis of the video stream
while True:
    # While in this loop, there is no vote.
    # This is just to play with the system.
    # The border of the video is set to blue with a specific line,
    # explaining that there is no vote until the person scans its QR Code
    ret, img = camera.read()

    img_display = img

    hand = detector.findHandedness(img)
    if hand == "Gauche":
        img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    # We count the number of fingers showing on the video frame
    totalFingers = vbf.fingerCount(lmList, tipIds, hand)

    if hand == "Gauche":
        img = cv2.flip(img, 1)

    # We clearly state that there is no vote until a QR Code is scanned
    cv2.putText(img, str(totalFingers), (50, 100), cv2.FONT_HERSHEY_DUPLEX, 2, (223, 162, 0),5)
    color = [255, 0, 0]
    top, bottom, left, right = [10]*4
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    img = cv2.putText(img, 'Vote non pris en compte, scannez votre QR Code', (25, 50), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 0, 0),1)

    # We test each frame for the presence of a QR Code
    img, barcode_info = vbf.read_barcodes(img)

    # We display the frames
    cv2.imshow('Borne', img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    # If a QR Code is found with a valid http address
    if barcode_info[:4]=='http':

        # We encrypt the QR Code to anonymize the vote
        hashed_barcode = hashlib.sha1(barcode_info.encode('utf-8'))
        print('QRCode found : ',barcode_info,', hashed value: ', hashed_barcode.hexdigest())

        # We set a 10 seconds timer
        t_end = time.time() + 10

        # We start the voting process
        while time.time() < t_end:
            ret, img = camera.read()

            # Adding border and text to highlight voting period
            seconds_left_to_vote = str(int(t_end-time.time()))
            color = [0, 0, 255]
            top, bottom, left, right = [10]*4
            img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

            hand = detector.findHandedness(img)
            if hand == "Gauche":
                img = cv2.flip(img, 1)

            img = cv2.putText(img, 'Vote en cours...' + seconds_left_to_vote + 's restantes', (25, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255),1)

            # We find the hand
            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)

            # We count the number of fingers showing on the video frame
            totalFingers = vbf.fingerCount(lmList, tipIds, hand)

            #cv2.rectangle(img, (40, 40), (100, 100), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (50, 100), cv2.FONT_HERSHEY_DUPLEX, 2, (223, 162, 0),5)

            #We store the result of each frame into the file (encrypted QR Code, datetime, number of fingers showing)
            file.write(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+','
                    +hashed_barcode.hexdigest()+','
                    +hand+','
                    +str(totalFingers)+'\n')

            # We display the frame along with any hand/finger information found
            cv2.imshow('Borne', img)

            if cv2.waitKey(1) & 0xFF == 27:
                break

camera.release()
cv2.destroyAllWindows()