import os
from tkinter import *
import sten.text as txt
import sten.hover as ho
from tkinter import ttk
from tkinter import messagebox as m
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring

root = Tk()
root.title('Steno')
root.config(bg='#f5f59a')
root.geometry('400x300')


def text_steno(event=None):
    global img
    win = Toplevel(master=root)
    win.title('Text Steno')
    win.geometry('480x400')
    win.config(bg='#c0ed98')
    win_label = Label(win, text='Text -Stenography', font=('Cascadia Code', 20), bg='#c0ed98', fg='#1046b3')
    win_label.place(x=5, y=4)
    size_label = Label(win, text='', font=('Cascadia Code', 10), bg='#c0ed98', fg='#f20713')
    size_label.place(x=5, y=45)

    def encode():
        global img, choice_button
        outfile_loc, m_or_f = '', ''

        m.showinfo("Procedure", "You will be asked to select\na file in which the data\nwill be hidden.")
        infile_loc = askopenfilename(parent=win, initialdir=os.getcwd(), title='Select File to ENCODE',
                                     filetypes=[('Text files', '.txt')], defaultextension='.txt')
        size_label.configure(text='Your data will be hidden inside the contents of -\n{}'.format(infile_loc))

        ch_lb = Label(win, text='Select what you want to hide', bg='#c0ed98', fg='#1046b3', font=('Cascadia Code', 10))
        ch_lb.place(x=5, y=85)
        select = StringVar(win)
        style = ttk.Style(master=win)
        style.configure('C.TRadiobutton', font=('Cascadia Code', 10), background='#c0ed98', foreground='#1046b3')

        choice_message = ttk.Radiobutton(win, text='Hide a Message', value="1", variable=select, style='C.TRadiobutton')
        choice_message.place(x=5, y=105)

        choice_file = ttk.Radiobutton(win, text='Hide a File', value="2", variable=select, style='C.TRadiobutton')
        choice_file.place(x=5, y=130)

        password = Entry(win, width=20, show='*', font=('Cascadia Code', 10), state=DISABLED)
        password.place(x=18, y=185)
        password.focus()

        def choice():
            global img, choice_button
            if select.get() == "1":
                message = Toplevel(master=win)
                message.title('Enter Message')
                lm = Label(message, text='Enter your message that you want to hide:', bg='yellow',
                           font=('Cascadia Code', 10))
                lm.pack(side=TOP, fill=BOTH)
                ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
                t = Text(message)
                t.config(font=('Cascadia Code', 10))
                t.pack()

                def click(event=None):
                    global m_or_f
                    password.config(state=NORMAL)
                    message.withdraw()
                    m_or_f = t.get("1.0", "end-1c")

                bm = Button(message, text='Done(Alt-x)', command=click, relief='flat', bg='yellow',
                            font=('Cascadia Code', 10))
                bm.pack(side=BOTTOM, fill=BOTH)
                ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
                message.bind('<Alt-x>', click)
                choice_button.config(state=DISABLED)
                refresh.config(state=NORMAL)

            elif select.get() == "2":
                global m_or_f
                m.showinfo('Procedure', 'Select the file which contains\nthe data you want to encode.')
                m_or_f = askopenfilename(parent=win, initialdir=os.getcwd(), title='Select File',
                                         filetypes=[('Text files', '.txt')], defaultextension='.txt')
                password.config(state=NORMAL)
                choice_button.config(state=DISABLED)
                refresh.config(state=NORMAL)

        choice_button = Button(win, text='Select', command=choice, bg='#08d0fc',
                               font=('Cascadia Code', 10), relief='ridge')
        choice_button.place(x=152, y=122)
        ho.CreateToolTip(choice_button, 'Opens a promt according\nto your chosen option.')

        def process():
            if password["state"] == ACTIVE or password['state'] == NORMAL:
                if password["show"] == '*':
                    password.config(show=None)

        pass_label = Label(win, text='Set password:', font=('Cascadia Code', 10), bg='#c0ed98', fg='#1046b3')
        pass_label.place(x=10, y=155)

        img = PhotoImage(file="images/noshow.png").subsample(4, 4)
        pass_button = Button(win, image=img, relief='ridge', bg='#36f5eb',
                             command=process, font=('Cascadia Code', 10))
        pass_button.place(x=195, y=180)
        ho.CreateToolTip(pass_button, 'Show password')
        success = Label(win, text='', bg='#c0ed98', font=('Cascadia Code', 10), fg='red')
        success.place(x=20, y=280)

        def execute(event=None):
            global outfile_loc, m_or_f
            m.showinfo('Procedure', 'Where would you like the encoded file to be saved?\n'
                                    'Select the path in the next window.')
            outfile_loc = asksaveasfilename(title='Save your encoded file as', filetypes=[('Text File', '.txt')],
                                            defaultextension='.txt', initialdir=os.getcwd(), parent=win)
            if select.get() == '1':
                txt.encode(passwd=password.get(), infile=infile_loc, outfile=outfile_loc, message=m_or_f)
                success.config(text='Successfully encoded message in\n{}'.format(outfile_loc))
            elif select.get() == '2':
                txt.encode(passwd=password.get(), infile=infile_loc, outfile=outfile_loc, file=m_or_f)
                success.config(text='Successfully encoded file {} in\n{}'.format(m_or_f, outfile_loc))

        main = Button(win, text='Hide Data', command=execute, bg='#eba823', relief='ridge', font=('Cascadia Code', 10))
        main.place(x=20, y=250)
        ho.CreateToolTip(main, 'Checks everything\nthen encodes the data')

        def refresh():
            if choice_button['state'] == DISABLED:
                choice_button.config(state=NORMAL)

        refresh = Button(win, text='Refresh', command=refresh, state=DISABLED, relief='ridge',
                         font=('Cascadia Code', 10), bg='#4159f2')
        refresh.place(x=360, y=360)
        ho.CreateToolTip(refresh, 'Refreshes Page')

    def decode():
        pass

    encoding = Button(win, text='Encode data', command=encode, relief='ridge', font=('Cascadia Code', 10), bg='#f00c58')
    encoding.place(x=40, y=360)
    ho.CreateToolTip(encoding, 'Encoding data function')
    decoding = Button(win, text="Decode data", command=decode, relief='ridge', font=('Cascadia Code', 10), bg='#6b0cf0')
    decoding.place(x=180, y=360)
    ho.CreateToolTip(decoding, "Decoding data function")


def image_steno(event=None):
    pass


def audio_steno(event=None):
    pass


lb = Label(root, text="Steno\n- Ultimate Stenography", font=('Showcard Gothic', 20), bg='#f5f59a', fg='#8507fa')
lb.place(x=20, y=20)

text = Button(root, text='Text\nStenography', relief='flat', bg='#A68064',
              command=text_steno, font=('Cascadia Code', 10))
text.place(x=56, y=250)
ho.CreateToolTip(text, 'Click here\nto hide your\ndata in a text file')

image = Button(root, text='Image\nStenography', relief='flat', bg='#A68064',
               command=image_steno, font=('Cascadia Code', 10))
image.place(x=156, y=250)
ho.CreateToolTip(image, 'Click here\nto hide your\ndata in an image file')

audio = Button(root, text='Audio\nStenography', relief='flat', bg='#A68064',
               command=audio_steno, font=('Cascadia Code', 10))
audio.place(x=256, y=250)
ho.CreateToolTip(audio, 'Click here\nto hide data in\n an audio file.')

root.mainloop()
