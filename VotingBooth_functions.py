import cv2
import mediapipe as mp  # for detecting fingers
import time  # For adding time to the main file
#from pyzbar import pyzbar  # for QR Code scanning
import math

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    # cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                    mp_drawing.draw_landmarks(
                        img,
                        lm,
                        self.mpHands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
        return lmList

    def findPositionMultiHand(self, img, draw=False):

        lmList = []
        if self.results.multi_hand_landmarks:
            hands = self.results.multi_hand_landmarks

            for hand in hands:
                # print("Main ", hand)
                lmListHand = []

                for id, lm in enumerate(hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmListHand.append([id, cx, cy])
                    if draw:
                        #cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                        mp_drawing.draw_landmarks(
                            img,
                            lm,
                            self.mpHands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                # print("Liste Hand : ", lmListHand)
                lmList.append(lmListHand)

        # print("lmList :", lmList)

        return lmList

    def findHandedness(self, img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(self.results)
        Handedness = self.results.multi_handedness
        hand = ''
        # print("Handeness valeur "+str(Handedness))
        # flip result and translate in French
        if Handedness:
            if Handedness[0].classification[0].label == "Right":
                hand = "Droite"
            if Handedness[0].classification[0].label == "Left":
                hand = "Gauche"
        # print(hand)
        return hand

    def findNumberofHand(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(self.results)
        Handedness = self.results.multi_handedness
        if Handedness is None:
            return 0
        else:
            return len(Handedness)

    def findindexesHands(self, img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(self.results)
        Handedness = self.results.multi_handedness
        hand = ''
        hand0 = ''
        hand1 = ''
        # print("Handeness valeur "+str(Handedness))
        # flip result and translate in French
        if Handedness:
            if len(Handedness) < 2:
                if Handedness[0].classification[0].label == "Right":
                    hand = "Droite"
                if Handedness[0].classification[0].label == "Left":
                    hand = "Gauche"
                return [hand]
            elif len(Handedness) == 2:
                hand0 = Handedness[0].classification[0].label.replace("Right", "Droite").replace("Left", "Gauche")
                hand1 = Handedness[1].classification[0].label.replace("Right", "Droite").replace("Left", "Gauche")

                # print("Hand0 : " + hand0, "Hand 1 : " + hand1)
                return [hand0, hand1]


def fingerCount(lmList, tipIds, hand):
    if len(lmList) != 0:
        fingers = []
        totalFingers = 0

        if hand == "Gauche":
            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            totalFingers = fingers.count(1)

        if hand == "Droite":
            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(0)
            else:
                fingers.append(1)

            # 4 Fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            totalFingers = fingers.count(1)

        return totalFingers


def fingerCountBothHands(img, tipIds, handDetector):
    totalFingers = 0
    if handDetector:
        list_hand = handDetector.findindexesHands(img)
        if list_hand:
            if len(list_hand) == 2:
                lmList0 = handDetector.findPosition(img, handNo=0, draw=False)
                lmList1 = handDetector.findPosition(img, handNo=1, draw=False)
                hand0, hand1 = list_hand[0], list_hand[1]
                # print(lmList1)
                # hand0, hand1 = handDetector.findindexesHands(img)
                totalFingers = fingerCount(lmList0, tipIds, hand0) + fingerCount(lmList1, tipIds, hand1)
            else:
                lmList = handDetector.findPosition(img, handNo=0, draw=False)
                hand = list_hand[0]
                totalFingers = fingerCount(lmList, tipIds, hand)

    return totalFingers


def indentifyHands(img, tipIds, lmlist):
    identity_hands = []
    for list in lmlist:
        if len(list) == 21:
            identity_hand = []
            for nbr_transfo in range(1, 4):
                for tip in tipIds:
                    h, w, c = img.shape
                    cx = (list[tip][1] - list[tip - nbr_transfo][1]) / w
                    cy = (list[tip][2] - list[tip - nbr_transfo][2]) / h
                    long = math.sqrt(cx ** 2 + cy ** 2)
                    identity_hand.append([str(tip) + "_" + str(nbr_transfo), long])

        identity_hands.append(identity_hand)

    return identity_hands


def code_hand(id, ordre_main):
    dict_ratio_both = {}
    for id_hand, hand_identity in enumerate(id):
        main = ordre_main[id_hand]
        sorted_id = sorted(hand_identity)
        counter = 0
        for index in range(0, len(sorted_id), 3):
            ratio1 = round(sorted_id[index][1] / sorted_id[index + 1][1], 2)
            ratio2 = round(sorted_id[index][1] / sorted_id[index + 2][1], 2)
            dict_ratio_both[main + '_' + str(counter)] = [ratio1, ratio2]
            counter += 1

    return dict_ratio_both


def aggregate_dicts(dicts, operation=lambda x: sum(x) / len(x)):
    """
    Aggregate a sequence of dictionaries to a single dictionary using `operation`. `Operation` should
    reduce a list of all values with the same key. Keyrs that are not found in one dictionary will
    be mapped to `None`, `operation` can then chose how to deal with those.
    """
    all_keys = set().union(*[el.keys() for el in dicts])
    return {k: operation([dic.get(k, None) for dic in dicts]) for k in all_keys}


def mean_no_none(l):
    l_no_none_x = [el[0] for el in l if el is not None]
    l_no_none_y = [el[1] for el in l if el is not None]

    return [round(sum(l_no_none_x) / len(l_no_none_x),2), round(sum(l_no_none_y) / len(l_no_none_y),2)]


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    tipIds = [4, 8, 12, 16, 20]

    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        nbrHand = detector.findNumberofHand(img)

        if nbrHand > 0:
            if nbrHand == 2:
                ordre_main = detector.findindexesHands(img)
                identity = indentifyHands(img, tipIds, detector.findPositionMultiHand(img))
                print("id", identity)
                print(f"Identité des mains : {code_hand(identity, ordre_main)}")

        nbrFingers = fingerCountBothHands(img, tipIds, detector)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime


        cv2.putText(img, "Nbr doigts : " + str(int(nbrFingers)), (100, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 255, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
