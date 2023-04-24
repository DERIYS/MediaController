import tkinter as tk
import customtkinter as CTk
from MC import MediaController as MC


class GestureEditor:
    def __init__(self, master):
        self.default_gestures = (
            [1, 1, 0, 0, 0],  # Tuple of default gestures,
            [0, 0, 0, 0, 0],  # that we recommend to use.
            [0, 1, 1, 0, 0],  #
            [1, 1, 0, 0, 1],  # Each element in lists represents state of respective finger
            [1, 1, 1, 1, 1]   # (0 as closed, 1 as open)
        )

        self.custom_gestures = [
            [1, 1, 0, 0, 0],  # List of customizable gestures,
            [0, 0, 0, 0, 0],  # that user can change
            [0, 1, 1, 0, 0],  #
            [1, 1, 0, 0, 1],  # Each element in lists represents state of respective finger
            [1, 1, 1, 1, 1]  # (0 as closed, 1 as open)
        ]

        # Initializing a list of current states of fingers.
        self.fingers = [0 for _ in range(5)]

        # Loading images
        self.hand_image = tk.PhotoImage(file="pictures/hand.png")
        self.thumb_image = tk.PhotoImage(file="pictures/thumb.png")
        self.finger_image = tk.PhotoImage(file="pictures/finger.png")

        # Configuring the master
        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.title("Gesture editor")
        self.master.geometry("800x600")

        # Creating and placing the hand frame
        self.hand_frame = tk.Frame(
            self.master,
            bg="#f0f0f0",
            width=450,
            height=550
        )
        self.hand_frame.place(x=20, y=25)

        # Creating and placing each finger's canvas
        self.canvas_list = [
            tk.Canvas(
                self.hand_frame,
                bg="#f0f0f0",
                width=80,
                height=128,
                highlightthickness=0
            ),
            tk.Canvas(
                self.hand_frame,
                bg="#f0f0f0",
                width=54,
                height=251,
                highlightthickness=0
            ),
            tk.Canvas(
                self.hand_frame,
                bg="#f0f0f0",
                width=54,
                height=251,
                highlightthickness=0
            ),
            tk.Canvas(
                self.hand_frame,
                bg="#f0f0f0",
                width=54,
                height=251,
                highlightthickness=0
            ),
            tk.Canvas(self.hand_frame, bg="#f0f0f0", width=55, height=149, highlightthickness=0)
        ]
        self.thumb_canvas = self.canvas_list[0]
        self.finger1_canvas = self.canvas_list[1]
        self.finger2_canvas = self.canvas_list[2]
        self.finger3_canvas = self.canvas_list[3]
        self.pinky_canvas = self.canvas_list[4]

        self.thumb_canvas.place(x=76, y=344)
        self.finger1_canvas.place(x=179, y=128)
        self.finger2_canvas.place(x=250, y=58)
        self.finger3_canvas.place(x=323, y=98)
        self.pinky_canvas.place(x=394, y=165)

        # Initializing a dwo-dimensional list of fingers' opening and closing methods.
        self.open_close_foos_list = [
            [  #
                lambda x: self.close_thumb(),  # The first element (list of lambdas),
                lambda x: self.close_finger1(),  # that available by index 0, contains
                lambda x: self.close_finger2(),  # lambdas calling methods to close
                lambda x: self.close_finger3(),  # a respective finger.
                lambda x: self.close_pinky(),  #
            ],

            [  #
                lambda x: self.open_thumb(),  # The first element (list of lambdas),
                lambda x: self.open_finger(1),  # that available by index 1, contains
                lambda x: self.open_finger(2),  # lambdas calling methods to open
                lambda x: self.open_finger(3),  # a respective finger.
                lambda x: self.open_pinky()  #
            ]
        ]

        # Creating the right-side button frame
        self.button_frame = tk.Frame(
            self.master,
            bg="#f0f0f0",
            width=260,
            height=600
        )
        self.button_frame.pack(side=tk.RIGHT, pady=0, padx=30)

        # Creating and placing buttons in the frame
        # Creating button_choice variable to represent the currently pressed button
        self.button_choice = None

        # List of right-side buttons, each one calls choose_gesture() method passing its id on clicking
        self.button_list = [
            CTk.CTkButton(
                master=self.button_frame,
                text="Manual",
                width=107,
                height=62,
                corner_radius=20,
                text_color="black",
                hover_color="#B8B8B8",
                hover=True,
                fg_color="#D9D9D9",
                command=lambda: self.choose_gesture(0)
            ),

            CTk.CTkButton(
                master=self.button_frame,
                text="Play/Pause",
                width=62,
                height=62,
                corner_radius=20,
                text_color="black",
                hover_color="#B8B8B8",
                hover=True,
                fg_color="#D9D9D9",
                command=lambda: self.choose_gesture(1)
            ),

            CTk.CTkButton(
                master=self.button_frame,
                text="Set to 50%",
                width=109,
                height=62,
                corner_radius=20,
                text_color="black",
                hover_color="#B8B8B8",
                hover=True,
                fg_color="#D9D9D9",
                command=lambda: self.choose_gesture(2)
            ),

            CTk.CTkButton(
                master=self.button_frame,
                text="Set to 0%",
                width=109,
                height=62,
                corner_radius=20,
                text_color="black",
                hover_color="#B8B8B8",
                hover=True,
                fg_color="#D9D9D9",
                command=lambda: self.choose_gesture(3)
            )
        ]

        self.manual_button = self.button_list[0]
        self.play_pause_button = self.button_list[1]
        self.set50_button = self.button_list[2]
        self.set0_button = self.button_list[3]

        self.manual_button.pack(pady=10)
        self.play_pause_button.pack(pady=10)
        self.set50_button.pack(pady=10)
        self.set0_button.pack(pady=10)

        # Creating and packing starting button
        self.start_button = CTk.CTkButton(
            master=self.button_frame,
            text="Start",
            width=159,
            height=62,
            corner_radius=20,
            text_color="black",
            hover_color="#B8B8B8",
            hover=True,
            fg_color="#D9D9D9",
            command=lambda: self.start(self.custom_gestures)
        )
        self.start_button.pack(pady=40)

        # Creating and placing hand canvas, where the hand and fingers will appear
        self.hand_canvas = tk.Canvas(
            self.hand_frame,
            bg="#f0f0f0",
            width=294,
            height=236,
            highlightthickness=0
        )
        self.hand_canvas.place(x=156, y=309)
        self.hand_canvas.create_image(145, 114, image=self.hand_image)

        # Creating and placing a reset button
        self.default_reset_button = CTk.CTkButton(
            master=self.hand_frame,
            text="Reset default gesture",
            width=109,
            height=62,
            corner_radius=20,
            text_color="black",
            hover_color="#B8B8B8",
            hover=True,
            fg_color="#D9D9D9",
            command=lambda: self.reset(self.button_choice)
        )
        self.default_reset_button.place(x=0, y=0)

        # Binding open/close methods to each finger's canvas and passing respective finger's id as well as the current button choice
        self.thumb_canvas.bind('<ButtonPress-1>', lambda x: self.open_close_finger(0, self.button_choice))
        self.finger1_canvas.bind('<ButtonPress-1>', lambda x: self.open_close_finger(1, self.button_choice))
        self.finger2_canvas.bind('<ButtonPress-1>', lambda x: self.open_close_finger(2, self.button_choice))
        self.finger3_canvas.bind('<ButtonPress-1>', lambda x: self.open_close_finger(3, self.button_choice))
        self.pinky_canvas.bind('<ButtonPress-1>', lambda x: self.open_close_finger(4, self.button_choice))

    """
      Frontend opening and closing fingers methods.

      The bottom line is to clear all the objects 
      related to the closed/open finger and draw
      a new picture.
    """

    def open_thumb(self):
        # Clearing all objects in the canvas to draw a new picture
        self.thumb_canvas.delete('all')
        self.hand_canvas.delete('thumb_dot')

        # Creating the thumb image in a way that it seems open
        self.thumb_canvas.create_image(41, 63, image=self.thumb_image)

        # Creating a grey dot that represents a nail, for a better navigation
        self.thumb_canvas.create_oval(22, 20, 47, 45, fill="#d9d9d9")

    def open_finger(self, id):
        # Clearing all objects in the canvas to draw a new picture
        self.canvas_list[id].delete('all')

        # Creating the finger's image in a way that it seems open
        self.canvas_list[id].create_image(27, 127, image=self.finger_image)

        # Creating a grey dot that represents a nail, for a better navigation
        self.canvas_list[id].create_oval(15, 17, 40, 42, fill="#d9d9d9")

    def open_pinky(self):
        # Clearing all objects in the canvas to draw a new picture
        self.pinky_canvas.delete('all')

        # Creating the pinky's image in a way that it seems open
        self.pinky_canvas.create_image(27, 125, image=self.finger_image)

        # Creating a grey dot that represents a nail, for a better navigation
        self.pinky_canvas.create_oval(15, 17, 40, 42, fill="#d9d9d9")

    def draw_open_hand(self):
        """
          This method is responsible for drawing an open hand
        """
        for id in range(1, 4): self.open_finger(id)
        self.open_thumb()
        self.open_pinky()

        self.fingers = [1 for _ in range(5)]

    def close_thumb(self):
        # Clearing all objects in the canvas to draw a new picture
        self.thumb_canvas.delete('all')

        # Creating the thumb image in a way that it seems close
        self.thumb_canvas.create_image(65, 87, image=self.thumb_image)

        # Creating a grey dot that represents a nail, for a better navigation
        self.hand_canvas.create_oval(0, 113, 25, 138, fill="#f0f0f0", tags='thumb_dot')

    def close_finger1(self):
        # Clearing all objects in the canvas to draw a new picture
        self.finger1_canvas.delete('all')

        # Creating the finger's image in a way that it seems close
        self.finger1_canvas.create_image(27, 205, image=self.finger_image)

        # Creating a grey dot that represents a nail, for a better navigation
        self.finger1_canvas.create_oval(15, 154, 40, 179, fill="#d9d9d9")

    def close_finger2(self):
        # Clearing all objects in the canvas to draw a new picture
        self.finger2_canvas.delete('all')

        # Creating the finger's image in a way that it seems close
        self.finger2_canvas.create_image(27, 275, image=self.finger_image)

        # Creating a grey dot that represents a nail, for a better navigation
        self.finger2_canvas.create_oval(15, 223, 40, 248, fill="#d9d9d9")

    def close_finger3(self):
        # Clearing all objects in the canvas to draw a new picture
        self.finger3_canvas.delete('all')

        # Creating the finger's image in a way that it seems close
        self.finger3_canvas.create_image(27, 235, image=self.finger_image)

        # Creating a grey dot that represents a nail, for a better navigation
        self.finger3_canvas.create_oval(15, 183, 40, 208, fill="#d9d9d9")

    def close_pinky(self):
        # Clearing all objects in the canvas to draw a new picture
        self.pinky_canvas.delete('all')

        # Creating the pinky's image in a way that it seems close
        self.pinky_canvas.create_image(27, 169, image=self.finger_image)

        # Creating a grey dot that represents a nail, for a better navigation
        self.pinky_canvas.create_oval(15, 116, 40, 141, fill="#d9d9d9")

    """
       Back-end open/closing methods
    """

    def open_close_finger(self, id, button_choice):
        """
          This method is responsible for opening and closing the finger of the pressed canvas.
        """
        # This if statement prevents accidental finger opening/closing if no gesture button was pressed
        if button_choice is not None:
            """
            The list of methods was designed specifically to be able to call a desired method within one string
            If (the finger's state + 1) % 2 == 0, it will close it since 0 stays for a closed figner, and by id, 
            it chooses the specific method for the pressed finger.
            
            Example:
            Current state of a finger is: 1 (open)
            If it's pressed, the user wants to close it, hence: (1 + 1) % 2 = 0, =>
            it closes the finger.
            """
            self.open_close_foos_list[(self.fingers[id] + 1) % 2][id]("леу)")
            # Updating the finger's state.
            self.fingers[id] += 1
            self.fingers[id] %= 2
            # Updating the custom_gestures to the current fingers state.
            self.custom_gestures[button_choice] = self.fingers.copy()

    def set_gesture(self, fingers):
        """
          This method is responsible for setting the needed fingers states and called within choose_gesture method,
          it takes one argument which represents the needed fingers states.
        """
        for id in range(5):
            # fingers[id] can be either 0 or 1 (closed or open), therefore it calls the needed function
            self.open_close_foos_list[fingers[id]][id]('леу)')
        # Saving now the current state of the fingers.
        self.fingers = fingers.copy()

    def choose_gesture(self, button_choice):
        """
          This method is called whenever a gesture button is pressed,
          it takes one argument which represents the currently pressed button.
        """
        # Setting the current button choice
        self.button_choice = button_choice

        # Changing the bg color of the buttons
        for button in self.button_list: button.configure(fg_color='#D9D9D9')
        self.button_list[button_choice].configure(fg_color='#B8B8B8')

        # Setting the gesture that goes with the currently pressed button
        self.set_gesture(self.custom_gestures[button_choice])

    def reset(self, button_choice):
        """
          This method is called when the reset button is pressed,
          it takes one which represents the currently pressed button.
        """
        # Preventing accidental resetting when no gesture is chosen
        if button_choice is not None:
            # Setting the default state of fingers on the display
            self.set_gesture(self.default_gestures[button_choice])

            # Changing the current state of fingers
            self.custom_gestures[button_choice] = self.default_gestures[button_choice].copy()

    def start(self, custom_gestures):
        """
          This method is called when the start button is pressed,
          it takes one argument which represents user-customized gestures
        """
        media_controller = MC()  # Initializing the instance of MC module
        try:
            media_controller.action(custom_gestures)  # Calling the action method, which takes care of further work
        except AttributeError:
            tk.messagebox.showerror(title='Error', message="Unable to detect a webcam, please make sure it's connected")
