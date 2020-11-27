import os
from tkinter import *
import sten.text as txt
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

root = Tk()
root.title('Steno')
root.geometry('400x300')


def text_steno(event=None):
    win = Tk()
    win.title('Text Steno')
    win.geometry('300x300')
    win_label = Label(win, text='Text\n-Stenography', font=('Cascadia Code',)).place(x=5, y=5)

    def encode():
        infile_loc = askopenfilename(initialdir=os.getcwd(), title='Select File to ENCODE',
                                     filetypes=[('Text files', '.txt')], defaultextension='.txt')
        select = IntVar()
        choice_label = Label(win, text='Select which type of data you want to encode').place(x=20, y=55)
        choice_message = ttk.Radiobutton(win, text='Encode a Message', value=1, variable=select)
        choice_message.place(x=5, y=75)
        choice_file = ttk.Radiobutton(win, text='Encode a File', value=2, variable=select)
        choice_file.place(x=5, y=105)
        pass_label = Label(win, text='Set password:').place(x=20, y=125)
        password = Entry(win, width=20, show='*').place(x=18, y=145)

        def enter_save(event=None):
            outfile_loc = asksaveasfilename(title='Save your encoded file as', filetypes=[('Text File', '.txt')],
                                            defaultextention='.txt', initialdir=os.getcwd())
            return outfile_loc

        pass_button = Button(win, text='Enter', relief='ridge', command=enter_save).place(x=145, y=143)
        win.bind('<Return>', enter_save)
        # txt.encode(passwd=password, infile=infile_loc, outfile=enter_save())

    def decode():
        pass

    encoding = Button(win, text='Encode data', command=encode, relief='ridge').place(x=40, y=260)
    decoding = Button(win, text="Decode data", command=decode, relief='ridge').place(x=180, y=260)

    win.mainloop()


def image_steno(event=None):
    pass


def audio_steno(event=None):
    pass


lb = Label(root, text="Steno\n- Ultimate Stenography", font=('Showcard Gothic', 20))
lb.place(x=20, y=20)
text = Button(root, text='Text\nStenography', command=text_steno, relief='flat', bg='#A68064')
text.place(x=56, y=250)
image = Button(root, text='Image\nStenography', command=image_steno, relief='flat', bg='#A68064')
image.place(x=156, y=250)
audio = Button(root, text='Audio\nStenography', command=audio_steno, relief='flat', bg='#A68064')
audio.place(x=256, y=250)

root.mainloop()
