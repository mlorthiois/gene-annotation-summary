#!/usr/src/env python
from PIL import ImageTk
import PIL.Image
from tkinter import *
from src.main import main
from tkinter import filedialog


def import_file():
    global filename
    filename = filedialog.askopenfilename(filetypes=(
        ("TXT files", "*.txt"), ("All files", "*.*")))
    openedFile = open(filename)
    readFile = openedFile.read()
    txt.delete(1.0, END)
    txt.insert('1.0', readFile)


def execute():
    main(filename, txt)


# Constant
window = Tk()
window.title("Gene-Table Generator")
window.geometry("500x650")

img = PIL.Image.open('img/database.png')
database = ImageTk.PhotoImage(img.resize((190, 190)))
img = PIL.Image.open('img/file.png')
fileimport = ImageTk.PhotoImage(img.resize((90, 90)))

img = PIL.Image.open('img/cloud.png')
cloud = ImageTk.PhotoImage(img.resize((90, 90)))

# Frame
frame_head = Frame(window)
frame = Frame(window)
icon_frame = Frame(window)
text_frame = Frame(window)
copyright_frame = Frame(window)

# Widgets
label_title = Label(frame_head,
                    text="Gene Datatable Creator",
                    font="Helvetica 24 bold",
                    fg="#114d74")
label_title.pack(pady=15)

width = 200
height = 200
canvas = Canvas(frame, width=width, height=height)
canvas.create_image(width/2, height/2, image=database)
canvas.pack()

label_title = Label(text_frame,
                    text="File processing:",
                    font="Helvetica 16")
label_title.pack()

button_import = Button(icon_frame,
                       text='1. Select a file',
                       command=import_file,
                       image=fileimport,
                       compound=TOP,
                       relief='flat')
button_import.grid(row=0, column=0, padx=5, pady=5)

button_upload = Button(icon_frame,
                       text='2. Start',
                       image=cloud,
                       command=execute,
                       compound=TOP,
                       highlightthickness=0,
                       bd=0)
button_upload.grid(row=0, column=1, padx=5, pady=5)

txt = Text(text_frame, height=12,
           wrap=WORD,
           fg="#1e1e1e",
           background='#eff0f1',
           font="Courier 13")
txt.insert('1.0', 'Required file format : <gene symbol>,<organism>')
txt.pack(fill=X, padx=20)

foot_text = Label(copyright_frame,
                  text="© Matthias Lorthiois - M1 Bioinformatique - Université Rouen-Normandie",
                  font="Helvetica 12")
foot_text.pack()

# Pack
frame_head.pack()
frame.pack()
text_frame.pack(pady=13)
icon_frame.pack()
copyright_frame.pack(pady=13)

# Start
window.mainloop()
