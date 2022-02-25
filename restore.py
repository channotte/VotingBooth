from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
from PIL import Image
import random
import string

import VotingBooth_functions as vbf  # for additional functions
import hashlib  # for encrypting QR codes

im = Image.open("static/merci.jpg")

# We store all results in a file on the local system
file = open('data.csv', 'a+')

# We set parameters for hand detector
detector = vbf.handDetector(detectionCon=0.90)

# For the tipIds, we take the tip of each finger
# figure 2.21 in https://google.github.io/mediapipe/solutions/hands.html
tipIds = [4, 8, 12, 16, 20]

# We get the video capture running
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(3, 1024)  # 3 = width
camera.set(4, 768)  # 4 = height

global capture, rec_frame, grey, switch, neg, face, rec, out
capture = 0
grey = 0
neg = 0
face = 0
switch = 1
rec = 0

# make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

# instatiate flask app
app = Flask(__name__, template_folder='./templates')


def record(out):
    global rec_frame
    while (rec):
        time.sleep(0.05)
        out.write(rec_frame)


def detect_face(frame):
    return frame


def ifnull(var, val):
    if var is None:
        return val
    return var


def gen_frames():  # generate frame by frame from camera
    global out, capture, rec_frame
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame, 1)

        if success:

            try:
                # hand = detector.findHandedness(frame)
                nbHands = detector.findNumberofHand(frame)
                frame = detector.findHands(frame)
                # lmList = detector.findPosition(frame, draw=False)

                # We count the number of fingers showing on the video frame
                # totalFingers = vbf.fingerCount(lmList, tipIds, hand)
                totalFingers = vbf.fingerCountBothHands(frame, tipIds, detector)

                # We clearly state that there is no vote until a QR Code is scanned
                color = [62, 62, 62]

                NumFingers = str(totalFingers)
                if NumFingers == 'None':
                    NumFingers = '0'

                cv2.putText(frame, NumFingers, (50, 100), cv2.FONT_HERSHEY_DUPLEX, 2, color, 5)
                top, bottom, left, right = [10] * 4
                frame = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
                frame = cv2.putText(frame, 'Vote non pris en compte, montrez vos 10 doigts pour commencer', (25, 50),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.75, color, 1)

                # We test each frame for the presence of a QR Code
                # frame, barcode_info = vbf.read_barcodes(frame)

                # We store the result of each frame into the file (encrypted QR Code, datetime, number of fingers showing)
                # file.write(
                #   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ','
                #    + 'NoVote' + ','
                #    + hand + ','
                #    + str(totalFingers) + '\n')

                identite_recupere = False

                ordre_main = detector.findindexesHands(frame)
                identity = vbf.indentifyHands(frame, tipIds, detector.findPositionMultiHand(frame))

                if nbHands == 2 and totalFingers == 10:
                    code_main = vbf.code_hand(identity, ordre_main)

                    if isinstance(code_main[0], list) and isinstance(code_main[1], list):
                        identite_recupere = True

                # letters = string.ascii_letters
                # code_main2 = str(codemain)_.join(random.choice(letters) for i in range(5))
                # If a QR Code is found with a valid http address
                if identite_recupere:

                    # hashed_code_main = str(code_main)
                    hashed_code_main = hashlib.sha256(str(code_main).encode())
                    print(f"Identité des mains : {hashed_code_main} récupérée")

                    # We set a 10 seconds timer to vote
                    t_end = time.time() + 10

                    # ***************************
                    # We start the voting process
                    # ***************************

                    while time.time() < t_end:

                        success, frame = camera.read()
                        frame = cv2.flip(frame, 1)

                        # Adding border and text to highlight voting period
                        seconds_left_to_vote = str(int(t_end - time.time()))
                        color = [10, 150, 10]
                        top, bottom, left, right = [10] * 4
                        frame = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                                   value=color)

                        hand = detector.findHandedness(frame)
                        # if hand == "Gauche":
                        #    frame = cv2.flip(frame, 1)

                        frame = cv2.putText(frame, 'Vote en cours...' + seconds_left_to_vote + 's restantes',
                                            (25, 50),
                                            cv2.FONT_HERSHEY_DUPLEX, 1, color, 1)

                        # We find the hand
                        frame = detector.findHands(frame)
                        lmList = detector.findPosition(frame, draw=False)

                        # We count the number of fingers showing on the video frame
                        totalFingers = vbf.fingerCount(lmList, tipIds, hand)

                        NumFingers = str(totalFingers)
                        if NumFingers == 'None':
                            NumFingers = '0'

                        cv2.putText(frame, NumFingers, (50, 100), cv2.FONT_HERSHEY_DUPLEX, 2, color, 5)

                        # CODE EN ERREUR #
                        # We store the result of each frame into the file (encrypted QR Code, datetime, number of fingers showing)
                        file.write(
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ','
                            + hashed_code_main.hexdigest() + ','
                            + hand + ','
                            + str(totalFingers) + '\n')

                        # We show the frames (voting process)
                        ret, buffer = cv2.imencode('.jpg', frame)
                        frame = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                    # We set a 10 seconds timer to vote
                    t_end_thanks = time.time() + 5

                    in_vote = False
                    while time.time() < t_end_thanks:
                        frame = im
                        ret, buffer = cv2.imencode('.jpg', frame)
                        frame = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                # We show the frames (non-voting process)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            pass


@app.route('/')
def index():
    return render_template('index_qcm.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/requests',methods=['POST','GET'])
# def tasks():
#     global switch,camera
#     if request.method == 'POST':
#         if request.form.get('click') == 'Capture':
#             global capture
#             capture=1
#         elif  request.form.get('grey') == 'Grey':
#             global grey
#             grey=not grey
#         elif  request.form.get('neg') == 'Negative':
#             global neg
#             neg=not neg
#         elif  request.form.get('face') == 'Face Only':
#             global face
#             face=not face
#             if(face):
#                 time.sleep(4)
#         elif  request.form.get('stop') == 'Stop/Start':
#
#             if(switch==1):
#                 switch=0
#                 camera.release()
#                 cv2.destroyAllWindows()
#
#             else:
#                 camera = cv2.VideoCapture(0)
#                 switch=1
#         elif  request.form.get('rec') == 'Start/Stop Recording':
#             global rec, out
#             rec= not rec
#             if(rec):
#                 now=datetime.datetime.now()
#                 fourcc = cv2.VideoWriter_fourcc(*'XVID')
#                 out = cv2.VideoWriter('vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
#                 #Start new thread for recording the video
#                 thread = Thread(target = record, args=[out,])
#                 thread.start()
#             elif(rec==False):
#                 out.release()
#
#
#     elif request.method=='GET':
#         return render_template('index.html')
#     return render_template('index.html')

if __name__ == '__main__':
    app.run()

def code_hand(id, ordre_main):
    list_ratio_both = []
    for id_hand, hand_identity in enumerate(id):
        main = ordre_main[id_hand]
        sorted_id = sorted(hand_identity)
        list_ratio = []
        counter = 0
        for index in range(0, len(sorted_id), 3):
            ratio1 = round(sorted_id[index][1] / sorted_id[index + 1][1], 3)
            ratio2 = round(sorted_id[index][1] / sorted_id[index + 2][1], 3)
            list_ratio.append([main + '_' + str(counter), ratio1, ratio2])
            counter += 1
        list_ratio_both.append(list_ratio)

    return list_ratio_both