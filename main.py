from tkinter import *

root = Tk()
root.title('Steno')
root.geometry('400x300')


def text_steno(event=None):
    pass


def image_steno(event=None):
    pass


def audio_steno(event=None):
    pass


lb = Label(root, text="Steno\n- Ultimate Stenography", font=20)
lb.place(x=20, y=20)
text = Button(root, text='Text\nStenography', command=text_steno()).place(x=56, y=250)
text = Button(root, text='Image\nStenography', command=image_steno()).place(x=156, y=250)
text = Button(root, text='Audio\nStenography', command=audio_steno()).place(x=256, y=250)


root.mainloop()
