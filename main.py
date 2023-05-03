# Slava Ukraini!

from gui import GestureEditor as GE
from tkinter import Tk

root = Tk()
root.iconbitmap("pictures/icon.ico")

app = GE(root)
app.draw_open_hand()

root.mainloop()
