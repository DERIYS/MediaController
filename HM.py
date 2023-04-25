import cv2
import math
import mediapipe as mp
import numpy as np

class HandsTracking():
    def __init__(self, mode=False, max_hands=1, complexity=1, detection_con=0.8, tracking_con=0.8):
        # Initializing needed parameters for hands recognition

        self.last_gesture = 'No hand'
        self.mode = mode
        self.max_hands = max_hands
        self.complexity = complexity
        self.detection_con = detection_con
        self.tracking_con = tracking_con

        # Initializing needed mediapipe's fields
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.complexity, self.detection_con, self.tracking_con)
        self.draw_mark = mp.solutions.drawing_utils

        # List of state of fingers
        self.lms = [0, 0, 0, 0, 0]
        # List of landmarks coordinates
        self.lm_lst = []
        # Volume
        self.volume = 0
        # Bar length
        self.bar_length = 0
        # Detected
        self.detected = False

    def find_hands(self, img, border=()):
        """
          This method finds and draws hands on a picture,
          it takes 2 arguments which is the image itself and border set to be () by default
        """

        # Setting cropped_img if there's a border
        if len(border) != 0:
            cropped_img = img[0:border[1], 0:border[0]]
            imgRGB = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
        else:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Converting color to RGB
        self.imgGBR = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)

        # Results of hands recognition
        self.results = self.hands.process(imgRGB)

        # If there are hand landmarks, it draws them and their connections
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
            
    def find_position(self):
        """
          This method converts founded coordinates to the needed
          unit and sets each finger's state by comparing them
        """
        self.lm_lst = []

        # Converting coordinates
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(hand_lms.landmark):
                    ox, oy = int(self.imgGBR.shape[1] * lm.x), int(self.imgGBR.shape[0]*lm.y)
                    self.lm_lst.append([id, ox, oy])

            """ 
            Setting the state of fingers by comparing lms coordinates.
            The first index is the id of a landmark, the second index is X or Y coordinate (1 as X, 2 as Y)
            See https://developers.google.com/mediapipe/solutions/vision/hand_landmarker#models for more understanding
            """
            if self.lm_lst != 0:
                if self.lm_lst[4][1] > self.lm_lst[3][1]:
                    self.lms[0] = 1
                else:
                    self.lms[0] = 0
                if self.lm_lst[8][2] < self.lm_lst[6][2]:
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
        """
          This method is responsible for the manual volume managing
          if the gestures are matching.
        """
        # Drawing a line between thumb and index finger
        cv2.line(img, (self.lm_lst[4][1], self.lm_lst[4][2]), (self.lm_lst[8][1], self.lm_lst[8][2]), (255, 0, 255), thickness = 3)
        # Drawing a circle on their top lms
        cv2.circle(img, (self.lm_lst[4][1], self.lm_lst[4][2]), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (self.lm_lst[8][1], self.lm_lst[8][2]), 8, (255, 0, 255), cv2.FILLED)

        # Calculating the length of the vector (the line between the fingertips)
        vector_len = math.hypot((self.lm_lst[8][1] - self.lm_lst[4][1]), (self.lm_lst[8][2] - self.lm_lst[4][2]))

        # Converting the vector length to the 0-100 scale
        self.volume = int(np.interp(vector_len, [15, 150], [0, 100]))

        # Smoothing the volume changing
        smoothness = 1
        self.volume = smoothness * round(self.volume / smoothness)

    def draw_border_and_bar(self, img, border):
        """
          This method is responsible for drawing the border and the bar.
        """
        # Drawing the border
        cv2.rectangle(img, (0, 0), border, (255, 0, 0), thickness = 3)

        # Drawing the bar's border
        cv2.rectangle(img, (587, 225), (img.shape[1]-2, img.shape[0]-2), (255, 0, 0), thickness = 3)

        # Converting the vector length to the needed scale to fill the bar
        self.bar_length = int(np.interp(self.volume, [0, 100], [480, 225]))
        # If volume != 0 and there was already one gesture recognized, it fills the bar
        if self.volume != 0 and self.last_gesture != 'No hand':
            cv2.rectangle(img, (590, self.bar_length + 3), (img.shape[1] - 5, img.shape[0] - 5), (255, 10, 255), thickness = cv2.FILLED)
        # Putting volume percentage
        if self.volume == 100:
            cv2.putText(img, str(self.volume), (587 , 210), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
        else:
            cv2.putText(img, str(self.volume), (595 , 210), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
