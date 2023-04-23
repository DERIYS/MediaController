import cv2
import win32api
from HM import HandsTracking
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from win32con import VK_MEDIA_PLAY_PAUSE, KEYEVENTF_EXTENDEDKEY


class MediaController(HandsTracking):
    def __init__(self):
        super().__init__()

        # Capturing video
        self.cap = cv2.VideoCapture(0)

        # Initializing needed variables for the future volume managing
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.manage_volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.last_volume = -1

        self.success = None
        self.img = None

    def check_fingers(self, fingers, gestures) -> bool:
        """
          This method returns True if the current state of
          fingers is matching the gesture and False otherwise
        """
        for id in range(5):
            if fingers[id] != gestures[id]:
                return False
        return True

    def compare_lms(self, custom_gestures):
        """
          This method is responsible for checking whether
          the gestures are matching the gesture and if so,
          executes the respective actions.
        """
        # Manual configuring if the gesture matches and if the last gesture wasn't 'play/pause1'
        if self.check_fingers(self.lms, custom_gestures[0]) and self.last_gesture != 'play/pause1':
            self.manual_config(self.img)
            # Setting calculated volume
            self.last_volume = self.volume
            self.manage_volume.SetMasterVolumeLevelScalar(self.volume / 100, None)
            # Overwriting of the last gesture
            self.last_gesture = 'manual'

        # Play/pause if the gestures match and if the last gesture wasn't 'play/pause1'
        elif self.check_fingers(self.lms, custom_gestures[1]):
            if self.last_gesture != 'play/pause1' and self.last_gesture is not None:
                win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
                self.last_gesture = 'play/pause1'

        # 50% volume if the gestures match
        elif self.check_fingers(self.lms, custom_gestures[2]):
            self.volume = 50
            self.manage_volume.SetMasterVolumeLevelScalar(self.volume / 100, None)
            self.last_gesture = '50%'

        # 0% volume if the gestures match
        elif self.check_fingers(self.lms, custom_gestures[3]):
            if self.last_gesture != 'min' and self.last_volume != -1:
                self.volume = 0
                self.manage_volume.SetMasterVolumeLevelScalar(0, None)
                self.last_gesture = 'min'
            else:
                self.last_gesture = 'min'

        # Unpause if the gesture is a fully open hand and the last gesture was 'play/pause1'
        if self.check_fingers(self.lms, custom_gestures[-1]):
            if self.last_gesture == 'play/pause1':
                win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
                self.last_gesture = 'play/pause2'

        # Returning to the previous volume if the gesture is a fully open hand and the last gesture was 'min'
        if self.check_fingers(self.lms, custom_gestures[-1]):
            if self.last_gesture == 'min' and self.last_volume != -1:
                self.volume = self.last_volume
                self.manage_volume.SetMasterVolumeLevelScalar(self.last_volume / 100, None)
                self.last_gesture = 'back'
            else:
                self.last_gesture = 'back'


    def action(self, custom_gestures):
        """
          This method is responsible for launching the app
          and executing all the methods above as well as super ones
        """
        while True:
            self.success, self.img = self.cap.read()
            # Creating a border within which the hand will be recognized
            border = (self.img.shape[1] // 2 - 50, self.img.shape[0])

            # Drawing border and volume bar
            self.draw_border_and_bar(self.img, border)

            # Finding hands
            self.find_hands(self.img, border)

            # Finding positions of landmarks and then state of fingers
            self.find_position()

            # if hand is detected
            if self.detected:
                # Change the color of the border
                cv2.rectangle(self.img, (0, 0), border, (255, 10, 255), thickness=3)

                # Checking if gestures match
                self.compare_lms(custom_gestures)
            else:
                # Changing last gesture to 'no hand' if no hand is found
                self.last_gesture = 'no hand'

            # Display the picture on the window
            cv2.imshow('Result', self.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
