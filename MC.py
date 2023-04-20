import cv2
from HM import HandsTracking
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from keyboard import Keyboard

class MediaController(HandsTracking):
    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(0)

        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.last_volume = -1

        self.success = None
        self.img = None

    def check_fingers(self, fingers, gestures) -> bool:
        for id in range(5):
            if fingers[id] != gestures[id]:
                return False
        return True

    def compare_lms(self, custom_gestures):
        if self.check_fingers(self.lms, custom_gestures[0]):
            self.manual_config(self.img)
            self.last_volume = self.vector_len_volume
            self.volume.SetMasterVolumeLevelScalar(self.vector_len_volume / 100, None)
            self.last_gesture = 'manual'

        elif self.check_fingers(self.lms, custom_gestures[1]):
            try:
                if self.last_gesture != 'play/pause1' and self.last_gesture is not None:
                    Keyboard.key(0xB3)
                    self.last_gesture = 'play/pause1'
            except:
                self.last_gesture = 'play/pause1'

        elif self.check_fingers(self.lms, custom_gestures[2]):
            self.vector_len_volume = 50
            self.volume.SetMasterVolumeLevelScalar(self.vector_len_volume / 100, None)

        elif self.check_fingers(self.lms, custom_gestures[3]):
            try:
                if self.last_gesture != 'min':
                    self.vector_len_volume = 0
                    self.volume.SetMasterVolumeLevelScalar(0, None)
                    self.last_gesture = 'min'
                else:
                    self.last_gesture = 'min'
            except:
                self.last_gesture = 'min'

        if self.check_fingers(self.lms, custom_gestures[-1]):
            try:
                if self.last_gesture == 'play/pause1':
                    Keyboard.key(0xB3)
                    self.last_gesture = 'play/pause2'
            except:
                self.last_gesture = 'play/pause2'

        if self.check_fingers(self.lms, custom_gestures[-1]):
            try:
                if self.last_gesture == 'min':
                    self.vector_len_volume = self.last_volume
                    self.volume.SetMasterVolumeLevelScalar(self.last_volume / 100, None)
                    self.last_gesture = 'back'
                else:
                    self.last_gesture = 'back'
            except:
                self.last_gesture = 'back'

    def action(self, custom_gestures):
        while True:
            self.success, self.img = self.cap.read()
            border = (self.img.shape[1] // 2 - 50, self.img.shape[0])

            self.draw_border_and_bar(self.img, border)
            self.find_hands(self.img, border)
            self.find_position(self.img)

            if self.detected:
                cv2.rectangle(self.img, (0, 0), border, (255, 10, 255), thickness=3)
                self.compare_lms(custom_gestures)
            else:
                self.last_gesture = 'no hand'

            cv2.imshow('Result', self.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

#
#
# def check_fingers(fingers, gestures) -> bool:
#     for id in range(5):
#         if fingers[id] != gestures[id]:
#             return False
#     return True
#
# def start(custom_gestures):
#     cap = cv2.VideoCapture(0)
#     detector = ht()
#     devices = AudioUtilities.GetSpeakers()
#     interface = devices.Activate(
#         IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#     volume = cast(interface, POINTER(IAudioEndpointVolume))
#     last_volume = -1
#
#     while True:
#
#         success, img = cap.read()
#         border = (img.shape[1] // 2 - 50, img.shape[0])
#
#         detector.draw_border_and_bar(img, border)
#         detector.find_hands(img, border)
#         detector.find_position(img)
#
#         if detector.detected:
#             cv2.rectangle(img, (0, 0), border, (255, 10, 255), thickness = 3)
#
#         if check_fingers(detector.lms, custom_gestures[0]):
#             detector.manual_config(img)
#             last_volume = detector.vector_len_volume
#             volume.SetMasterVolumeLevelScalar(detector.vector_len_volume/100, None)
#             detector.last_gesture = 'manual'
#         elif check_fingers(detector.lms, custom_gestures[1]):
#             try:
#                 if detector.last_gesture != 'play/pause1' and detector.last_gesture is not None:
#                     Keyboard.key(0xB3)
#                     detector.last_gesture = 'play/pause1'
#             except:
#                 detector.last_gesture = 'play/pause1'
#
#         elif check_fingers(detector.lms, custom_gestures[2]):
#             detector.vector_len_volume = 50
#             volume.SetMasterVolumeLevelScalar(detector.vector_len_volume / 100, None)
#
#         elif check_fingers(detector.lms, custom_gestures[3]):
#             try:
#                 if detector.last_gesture != 'min':
#                     detector.vector_len_volume = 0
#                     volume.SetMasterVolumeLevelScalar(0, None)
#                     detector.last_gesture = 'min'
#                 else:
#                     detector.last_gesture = 'min'
#             except:
#                 detector.last_gesture = 'min'
#
#         if check_fingers(detector.lms, custom_gestures[-1]):
#             try:
#                 if detector.last_gesture == 'play/pause1':
#                     Keyboard.key(0xB3)
#                     detector.last_gesture = 'play/pause2'
#             except:
#                 detector.last_gesture = 'play/pause2'
#
#         if check_fingers(detector.lms, custom_gestures[-1]):
#             try:
#                 if detector.last_gesture == 'min':
#                     detector.vector_len_volume = last_volume
#                     volume.SetMasterVolumeLevelScalar(last_volume/100, None)
#                     detector.last_gesture = 'back'
#                 else:
#                     detector.last_gesture = 'back'
#             except:
#                 detector.last_gesture = 'back'
#
#
#         cv2.imshow('Result', img)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break