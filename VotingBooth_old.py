import threading

import pandas as pd
from flask import Flask, render_template, Response, request
import cv2
import os, sys
from PIL import Image
from turbo_flask import Turbo
import connexion_mongodb as mongof

pd.options.plotting.backend = "plotly"
import VotingBooth_functions as vbf  # for additional functions
import hashlib  # for encrypting QR codes
import math
# import matplotlib
# matplotlib.use("Qt5Agg")
# import multiprocessing
import time
from datetime import datetime

im = Image.open("static/merci.jpg")

# We store all results in a file on the local system
# file = open('data.csv', 'a+')

# We set parameters for hand detector
detector = vbf.handDetector(detectionCon=0.75)

# For the tipIds, we take the tip of each finger
# figure 2.21 in https://google.github.io/mediapipe/solutions/hands.html
tipIds = [4, 8, 12, 16, 20]

# We get the video capture running
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(3, 1024)  # 3 = width
camera.set(4, 768)  # 4 = height

global collection_inauguration, request

collection_inauguration = mongof.connect_db()
# request = [{'$group': {'_id': '$Hash', 'Vote1': {'$sum': {'$cond': [{'$eq': ['$Vote', '1']}, 1, 0]}},
#                        'Vote2': {'$sum': {'$cond': [{'$eq': ['$Vote', '2']}, 1, 0]}},
#                        'Vote3': {'$sum': {'$cond': [{'$eq': ['$Vote', '3']}, 1, 0]}},
#                        'Vote4': {'$sum': {'$cond': [{'$eq': ['$Vote', '4']}, 1, 0]}},
#                        'Vote5': {'$sum': {'$cond': [{'$eq': ['$Vote', '5']}, 1, 0]}}}}]
request = [{'$group': {'_id': '$Hash', 'Vote1': {'$sum': {'$cond': [{'$eq': ['$Vote', '1']}, 1, 0]}},
                       'Vote2': {'$sum': {'$cond': [{'$eq': ['$Vote', '2']}, 1, 0]}},
                       'Vote3': {'$sum': {'$cond': [{'$eq': ['$Vote', '3']}, 1, 0]}},
                       'Vote4': {'$sum': {'$cond': [{'$eq': ['$Vote', '4']}, 1, 0]}},
                       'Vote5': {'$sum': {'$cond': [{'$eq': ['$Vote', '5']}, 1, 0]}}}},
           {'$addFields': {'Votemax': {'$max': ['$Vote1', '$Vote2', '$Vote3', '$Vote4', '$Vote5']}}},
           {'$addFields': {'VoteValue': {'$cond': [{'$eq': ['$Votemax', '$Vote1']}, 'Vote1', {
               '$cond': [{'$eq': ['$Votemax', '$Vote2']}, 'Vote2',
                         {'$cond': [{'$eq': ['$Votemax', '$Vote3']}, 'Vote3', {
                             '$cond': [{'$eq': ['$Votemax', '$Vote4']}, 'Vote4',
                                       {'$cond': [{'$eq': ['$Votemax', '$Vote5']}, 'Vote5', 'Vote0']}]}]}]}]}}}]

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

# instantiate flask app
app = Flask(__name__, template_folder='./templates')
turbo = Turbo(app)
app.config['SERVER_NAME'] = "127.0.0.1:5000"


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


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def gen_frames():  # generate frame by frame from camera
    global out, capture, rec_frame
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame, 1)

        if success:

            try:
                hand = detector.findHandedness(frame)
                nbHands = detector.findNumberofHand(frame)
                frame = detector.findHands(frame)

                # We count the number of fingers showing on the video frame
                totalFingers = vbf.fingerCountBothHands(frame, tipIds, detector)

                color = [62, 62, 62]
                color_white = [226, 225, 227]
                color_black = [154, 153, 157]

                NumFingers = str(totalFingers)
                if NumFingers == 'None':
                    NumFingers = '0'

                cv2.putText(frame, NumFingers, (51, 121), cv2.FONT_HERSHEY_SIMPLEX, 2, color_black, 5)
                cv2.putText(frame, NumFingers, (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, color_white, 5)

                top, bottom, left, right = [5] * 4
                frame = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

                frame = cv2.putText(frame, 'Vote non pris en compte, montrez vos 10 doigts pour commencer', (26, 51),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_black, 2)

                frame = cv2.putText(frame, 'Vote non pris en compte, montrez vos 10 doigts pour commencer', (25, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_white, 2)

                mongof.write_db(collection_inauguration, totalFingers, hand)

                identite_recupere = False

                if nbHands == 2 and totalFingers == 10:

                    seuil_nbr_frame = 150
                    ordre_main = detector.findindexesHands(frame)
                    identity = vbf.indentifyHands(frame, tipIds, detector.findPositionMultiHand(frame))

                    liste_code_main = []
                    code_main = vbf.code_hand(identity, ordre_main)

                    while len(liste_code_main) < seuil_nbr_frame:
                        if len(code_main) == 10:
                            code_main = vbf.code_hand(identity, ordre_main)
                            liste_code_main.append(code_main)

                    mean_code_main = vbf.aggregate_dicts(liste_code_main, operation=vbf.mean_no_none)
                    print(mean_code_main)
                    identite_recupere = True

                if identite_recupere:

                    hashed_code_main = hashlib.sha256(str(mean_code_main).encode())
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

                        color = [231, 170, 61]
                        color_white = [241, 226, 139]
                        top, bottom, left, right = [5] * 4
                        frame = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                                   value=color)

                        hand = detector.findHandedness(frame)

                        frame = cv2.putText(frame, 'Vote en cours...' + seconds_left_to_vote + 's restantes',
                                            (26, 51),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

                        frame = cv2.putText(frame, 'Vote en cours...' + seconds_left_to_vote + 's restantes',
                                            (25, 50),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, color_white, 2)

                        # We find the hand
                        frame = detector.findHands(frame)
                        lmList = detector.findPosition(frame, draw=False)

                        # We count the number of fingers showing on the video frame
                        totalFingers = vbf.fingerCount(lmList, tipIds, hand)

                        NumFingers = str(totalFingers)
                        if NumFingers == 'None':
                            NumFingers = '0'

                        cv2.putText(frame, NumFingers, (51, 121), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 5)
                        cv2.putText(frame, NumFingers, (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, color_white, 5)

                        mongof.write_db(collection_inauguration, totalFingers, hand, hashed_code_main.hexdigest())

                        # We show the frames (voting process)
                        ret, buffer = cv2.imencode('.jpg', frame)
                        frame = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                    # We set a 10 seconds timer to vote
                    t_end_thanks = time.time() + 5

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


def update_load():
    with app.app_context():
        while True:
            time.sleep(10)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))


@app.route('/')
def index():
    return render_template('index_qcm.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.context_processor
def inject_load():
    refresh = datetime.now(tz=None).strftime("%a %d %b %H:%M:%S")
    df_vote = mongof.make_request(collection_inauguration, request)
    df_votants = mongof.retrieve_votants(df_vote)
    number_frame = 0 if collection_inauguration.count_documents(
        {}) is None else collection_inauguration.count_documents({})
    nb_gauche = collection_inauguration.count_documents({'hand': 'Gauche'})
    nb_droite = collection_inauguration.count_documents({'hand': 'Droite'})
    taux_utilisation = str(0 if number_frame == 0 else round_up(100 * (nb_droite + nb_gauche) / number_frame, 2))
    str_nbframe = format(number_frame, ',d').replace(',', ' ')

    data = {"vote": df_votants.to_list(), "Valeurs": ['Authenticité', "Ouverture", "Elégance", "Engagement", "Courage"]}
    data_main = {"vote": [nb_gauche, nb_droite], "Valeurs": ['Main Gauche', "Main Droite"], 'stack': [0, 0]}

    mongof.draw_horizontal_bar_plotly_opt2(pd.DataFrame(data), filename='static/repartition.png',
                                           title="Répartition des votes")
    encoded_repartition = mongof.encode_image('static/repartition.png')

    mongof.draw_bar_hands(pd.DataFrame(data_main), filename='static/test.png', title="Main utilisée pour le vote")
    encoded_img_data = mongof.encode_image("static/test.png")

    return {'vote1': df_votants[0], 'vote2': df_votants[1], 'vote3': df_votants[2], 'vote4': df_votants[3],
            'vote5': df_votants[4], 'nbframe': str_nbframe, 'tauxutil': taux_utilisation, 'img_data': encoded_img_data,
            'img_repartition': encoded_repartition, 'refresh': refresh}


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()
    # multiprocessing.Process(target=update_load, args=()).start()


if __name__ == '__main__':
    app.run()
