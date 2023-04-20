import tkinter as tk
import customtkinter as CTk
from MC import MediaController as MC

class GestureEditor:
    def __init__(self, master):
        self.counter = 0

        self.default_gestures = (
            [1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [1, 1, 0, 0, 1],
            [1, 1, 1, 1, 1]
        )

        self.custom_gestures = [
            [1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [1, 1, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]

        self.hand_image = tk.PhotoImage(file="pictures/hand.png")
        self.thumb_image = tk.PhotoImage(file="pictures/thumb.png")
        self.finger_image = tk.PhotoImage(file="pictures/finger.png")

        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.title("Gesture editor")
        self.master.geometry("800x600")

        # Создание фрейма для руки
        self.hand_frame = tk.Frame(
            self.master,
            bg="#f0f0f0",
            width=450,
            height=550
        )
        self.hand_frame.place(x=20, y=25)

        # Создание и размещение canvas для пальцев
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

        self.fingers = [0 for _ in range(5)]

        self.open_close_foos_list = [
            [
                lambda x: self.close_thumb(),
                lambda x: self.close_finger1(),
                lambda x: self.close_finger2(),
                lambda x: self.close_finger3(),
                lambda x: self.close_pinky(),
            ],

            [
                lambda x: self.open_thumb(),
                lambda x: self.open_finger(1),
                lambda x: self.open_finger(2),
                lambda x: self.open_finger(3),
                lambda x: self.open_pinky()
            ]
        ]

        # Создание фрейма для кнопок
        self.button_frame = tk.Frame(
            self.master,
            bg="#f0f0f0",
            width=260,
            height=600
        )
        self.button_frame.pack(side=tk.RIGHT, pady=0, padx=30)

        # Создание кнопок в правом фрейме
        self.button_choice = None

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

        # Создание кнопки внизу

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

        # Создание холста с рисунком руки
        self.hand_canvas = tk.Canvas(
            self.hand_frame,
            bg="#f0f0f0",
            width=294,
            height=236,
            highlightthickness=0
        )
        self.hand_canvas.place(x=156, y=309)
        self.hand_canvas.create_image(145, 114, image=self.hand_image)

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

    def open_thumb(self):
        self.thumb_canvas.create_rectangle(0, 0, 80, 128, fill="#f0f0f0", outline="#f0f0f0")
        self.hand_canvas.create_rectangle(0, 113, 25, 138, fill="black")
        self.thumb_canvas.create_image(41, 63, image=self.thumb_image)
        self.thumb_canvas.create_oval(22, 20, 47, 45, fill="#d9d9d9")
        self.thumb_canvas.bind('<ButtonPress-1>', lambda x: self.press_dot(0, self.button_choice))

    def open_finger(self, id):
        self.canvas_list[id].create_rectangle(0, 0, 55, 250, fill="#f0f0f0", outline="#f0f0f0")
        self.canvas_list[id].create_image(27, 127, image=self.finger_image)
        self.canvas_list[id].create_oval(15, 17, 40, 42, fill="#d9d9d9")
        self.canvas_list[id].bind('<ButtonPress-1>', lambda x: self.press_dot(id, self.button_choice))

    def open_pinky(self):
        self.pinky_canvas.create_rectangle(0, 0, 55, 143, fill="#f0f0f0", outline="#f0f0f0")
        self.pinky_canvas.create_image(27, 125, image=self.finger_image)
        self.pinky_canvas.create_oval(15, 17, 40, 42, fill="#d9d9d9")
        self.pinky_canvas.bind('<ButtonPress-1>', lambda x: self.press_dot(4, self.button_choice))

    def draw_open_hand(self):
        for id in range(1, 4): self.open_finger(id)
        self.open_thumb()
        self.open_pinky()

        self.fingers = [1 for _ in range(5)]

    def close_thumb(self):
        self.thumb_canvas.create_rectangle(1, 0, 79, 128, fill="#f0f0f0", outline="#f0f0f0")
        self.thumb_canvas.create_image(65, 87, image=self.thumb_image)
        self.hand_canvas.create_oval(0, 113, 25, 138, fill="#f0f0f0")

    def close_finger1(self):
        self.finger1_canvas.create_rectangle(0, 0, 55, 250, fill="#f0f0f0", outline="#f0f0f0")
        self.finger1_canvas.create_image(27, 205, image=self.finger_image)
        self.finger1_canvas.create_oval(15, 154, 40, 179, fill="#d9d9d9")

    def close_finger2(self):
        self.finger2_canvas.create_rectangle(0, 0, 55, 250, fill="#f0f0f0", outline="#f0f0f0")
        self.finger2_canvas.create_image(27, 275, image=self.finger_image)
        self.finger2_canvas.create_oval(15, 223, 40, 248, fill="#d9d9d9")

    def close_finger3(self):
        self.finger3_canvas.create_rectangle(0, 0, 55, 250, fill="#f0f0f0", outline="#f0f0f0")
        self.finger3_canvas.create_image(27, 235, image=self.finger_image)
        self.finger3_canvas.create_oval(15, 183, 40, 208, fill="#d9d9d9")

    def close_pinky(self):
        self.pinky_canvas.create_rectangle(0, 0, 55, 189, fill="#f0f0f0", outline="#f0f0f0")
        self.pinky_canvas.create_image(27, 169, image=self.finger_image)
        self.pinky_canvas.create_oval(15, 116, 40, 141, fill="#d9d9d9")

    def press_dot(self, id, button_choice):
        if button_choice is not None:
            if self.fingers[id] % 2:
                self.open_close_foos_list[0][id]("леу")
            else:
                self.open_close_foos_list[1][id]("леу")
            self.fingers[id] += 1
            self.fingers[id] %= 2
            self.custom_gestures[button_choice] = self.fingers.copy()

    def set_gesture(self, fingers):
        for id in range(5):
            self.open_close_foos_list[fingers[id]][id]('леу')
        self.fingers = fingers.copy()

    def choose_gesture(self, button_choice):
        self.button_choice = button_choice
        for button in self.button_list: button.configure(fg_color='#D9D9D9')
        self.button_list[button_choice].configure(fg_color='#B8B8B8')
        self.set_gesture(self.custom_gestures[button_choice])

    def reset(self, button_choice):
        if button_choice is not None:
            self.set_gesture(self.default_gestures[button_choice])
            self.custom_gestures[button_choice] = self.default_gestures[button_choice].copy()


    def start(self, custom_gestures):
        media_controller = MC()
        media_controller.action(custom_gestures)
