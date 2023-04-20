import cv2
import math
import mediapipe as mp
import numpy as np

class HandsTracking():

    def __init__(self, mode=False, max_hands = 1, complexity=1, detection_con = 0.8, tracking_con = 0.8):
        self.last_gesture = None
        self.mode = mode
        self.max_hands = max_hands
        self.complexity = complexity
        self.detection_con = detection_con
        self.tracking_con = tracking_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.complexity, self.detection_con, self.tracking_con)
        self.draw_mark = mp.solutions.drawing_utils

        self.finger_pose = []
        self.lms = [0, 0, 0, 0, 0]
        self.vector_len_volume = 0
        self.vector_len_bar = 0
        self.detected = False

    def find_hands(self, img, border=()):

        if len(border) != 0:
            cropped_img = img[0:border[1], 0:border[0]]
            imgRGB = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
        else:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.imgGBR = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            self.detected = True
            for hand_lms in self.results.multi_hand_landmarks:
                if len(border) != 0:
                    self.draw_mark.draw_landmarks(img[0:border[1], 0:border[0]], hand_lms, self.mp_hands.HAND_CONNECTIONS)
                else:
                    self.draw_mark.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                    
                # print(self.lms, self.vector_len_volume)
        else:
            self.detected = False
            
    def find_position(self, img):
        self.lm_lst = []

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(hand_lms.landmark):
                    ox, oy = int(self.imgGBR.shape[1] * lm.x), int(self.imgGBR.shape[0]*lm.y)
                    self.lm_lst.append([id, ox, oy])

            if self.lm_lst != 0:
                if self.lm_lst[4][1] > self.lm_lst[2][1]:
                    self.lms[0] = 1
                else:
                    self.lms[0] = 0
                if self.lm_lst[8][2] < self.lm_lst[5][2]:
                    self.lms[1] = 1
                else:
                    self.lms[1] = 0
                if self.lm_lst[12][2] < self.lm_lst[9][2]:
                    self.lms[2] = 1
                else:
                    self.lms[2] = 0
                if self.lm_lst[16][2] < self.lm_lst[13][2]:
                    self.lms[3] = 1
                else:
                    self.lms[3] = 0
                if self.lm_lst[20][2] < self.lm_lst[18][2]:
                    self.lms[4] = 1
                else:
                    self.lms[4] = 0

    def manual_config(self, img):

        cv2.line(img, (self.lm_lst[4][1], self.lm_lst[4][2]), (self.lm_lst[8][1], self.lm_lst[8][2]), (255, 0, 255), thickness = 3)
        cv2.circle(img, (self.lm_lst[4][1], self.lm_lst[4][2]), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (self.lm_lst[8][1], self.lm_lst[8][2]), 8, (255, 0, 255), cv2.FILLED)

        vector_len = math.hypot((self.lm_lst[8][1] - self.lm_lst[4][1]), (self.lm_lst[8][2] - self.lm_lst[4][2]))
        self.vector_len_volume = int(np.interp(vector_len, [15, 150], [0, 100]))
        self.vector_len_bar = int(np.interp(vector_len, [15, 150], [480, 225]))

        smoothness = 1
        self.vector_len_volume = smoothness * round(self.vector_len_volume/smoothness)

    def draw_border_and_bar(self, img, border):
        cv2.rectangle(img, (0, 0), border, (255, 0, 0), thickness = 3)
        cv2.rectangle(img, (587, 225), (img.shape[1]-2, img.shape[0]-2), (255, 0, 0), thickness = 3)
        if self.vector_len_volume != 0 and self.last_gesture != '':
            cv2.rectangle(img, (590, self.vector_len_bar+3), (img.shape[1] - 5, img.shape[0] - 5), (255, 10, 255), thickness = cv2.FILLED)
        if self.vector_len_volume == 100:
            cv2.putText(img, str(self.vector_len_volume), (587 , 210), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
        else:
            cv2.putText(img, str(self.vector_len_volume), (595 , 210), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
