from PIL import ImageTk
import PIL.Image
from tkinter import *
from src.script import main
from tkinter import filedialog
import webbrowser
import os


class Interface:
    def __init__(self):
        self.window = Tk()
        self.window.title("Automatic Annotation Table App")
        self.window.geometry("600x730")

        # Frame Initialization
        self.frame_head = Frame(self.window)
        self.frame = Frame(self.window)
        self.icon_frame = Frame(self.window)
        self.text_frame = Frame(self.window)
        self.copyright_frame = Frame(self.window)

        # Widget creation
        self.create_widget()

    def create_widget(self):
        self.header_widget()
        self.text_widget()
        self.icons_widget()
        self.copyright_widget()

    def header_widget(self):
        label_title = Label(self.frame_head,
                            text="Automatic Annotation Table",
                            font="Arial 24 bold",
                            fg="#114d74")
        label_title.pack(pady=15)

        self.img = PIL.Image.open('img/database.png')
        self.database = ImageTk.PhotoImage(self.img.resize((190, 190)))
        width = 200
        height = 200
        canvas = Canvas(self.frame, width=width, height=height)
        canvas.create_image(width/2, height/2, image=self.database)
        canvas.pack()
        self.frame_head.pack()
        self.frame.pack()

    def text_widget(self):
        label_title = Label(self.text_frame,
                            text="Content of the request:",
                            font="Arial 16")
        label_title.pack()

        self.txt = Text(self.text_frame, height=12,
                        wrap=WORD,
                        fg="#1e1e1e",
                        background='#eff0f1',
                        font="Courier 13")
        self.txt.insert(
            '1.0', 'Required file format : <gene symbol>,<organism>')
        self.txt.pack(fill=X, padx=20)
        self.text_frame.pack(pady=13)

    def icons_widget(self):
        self.img = PIL.Image.open('img/file.png')
        self.fileimport = ImageTk.PhotoImage(self.img.resize((90, 90)))

        self.img = PIL.Image.open('img/cloud.png')
        self.cloud = ImageTk.PhotoImage(self.img.resize((90, 90)))

        self.img = PIL.Image.open('img/open.png')
        self.open_img = ImageTk.PhotoImage(self.img.resize((90, 90)))

        button_import = Button(self.icon_frame,
                               text='1. Select a file',
                               command=self.import_file,
                               image=self.fileimport,
                               compound=TOP,
                               relief='flat')
        button_import.grid(row=0, column=0, padx=5, pady=5)

        button_upload = Button(self.icon_frame,
                               text='2. Start',
                               image=self.cloud,
                               command=self.execute,
                               compound=TOP,
                               highlightthickness=0,
                               bd=0)
        button_upload.grid(row=0, column=1, padx=5, pady=5)

        button_open = Button(self.icon_frame,
                             text='3. Open table',
                             image=self.open_img,
                             command=self.open_file,
                             compound=TOP,
                             highlightthickness=0,
                             bd=0)
        button_open.grid(row=0, column=2, padx=5, pady=5)
        self.icon_frame.pack()

    def copyright_widget(self):
        foot_text = Label(self.copyright_frame,
                          text="Matthias Lorthiois - Master Bioinformatics - University Rouen-Normandy",
                          font="Arial 11")
        foot_text.pack()
        self.copyright_frame.pack(pady=13)

    def import_file(self):
        global filename
        filename = filedialog.askopenfilename(filetypes=(
            ("TXT files", "*.txt"), ("All files", "*.*")))
        openedFile = open(filename)
        readFile = openedFile.read()
        self.txt.delete(1.0, END)
        self.txt.insert('1.0', readFile)

    def execute(self):
        main(filename, self.txt)

    def open_file(self):
        webbrowser.open('file://' + os.path.realpath('Results.html'))
