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
    win = Tk()
    win.title('Text Steno')
    win.geometry('480x400')
    win.config(bg='#c0ed98')
    win_label = Label(win, text='Text -Stenography', font=('Cascadia Code', 15)).place(x=5, y=4)
    size_label = Label(win, text='', font=('Cascadia Code', 10))
    size_label.place(x=5, y=55)

    def encode():
        outfile_loc, m_or_f = '', ''
        m.showinfo("Process", "You will be told to select\na file in which you would\nlike to hide the data.")

        infile_loc = askopenfilename(parent=win, initialdir=os.getcwd(), title='Select File to ENCODE',
                                     filetypes=[('Text files', '.txt')], defaultextension='.txt')
        size_label.configure(text='The chosen file is {}'.format(infile_loc))

        style = ttk.Style(master=win)
        style.configure('C.TRadiobutton', font=('Cascadia Code', 10))
        choice_label = Label(win, text='Select which type of data you want to hide',
                             font=('Cascadia Code', 10)).place(x=5, y=75)
        select = StringVar(win)
        choice_message = ttk.Radiobutton(win, text='Hide a Message', value="1", variable=select, style='C.TRadiobutton')
        choice_message.place(x=5, y=105)
        choice_file = ttk.Radiobutton(win, text='Hide a File', value="2", variable=select, style='C.TRadiobutton')
        choice_file.place(x=5, y=125)

        password = Entry(win, width=20, show='*', state=DISABLED)
        password.place(x=18, y=175)
        password.focus()

        def choice(event=None):
            if select.get() == "1":
                message = Toplevel(master=win)
                message.title('Enter Message')
                lm = Label(message, text='Enter your message that you want to hide:',
                           font=('Cascadia Code', 10)).pack(side=TOP)
                t = Text(message)
                t.config(font=('Cascadia Code', 10))
                t.pack()

                def click(event=None):
                    global m_or_f
                    password.config(state=NORMAL)
                    message.withdraw()
                    m_or_f = t.get("1.0", "end-1c")

                bm = Button(message, text='Enter(Alt-x)', command=click, relief='flat', bg='yellow',
                            font=('Cascadia Code', 10))
                bm.pack(side=BOTTOM, fill=BOTH)
                ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
                message.bind('<Alt-x>', click)

            elif select.get() == "2":
                global m_or_f
                m_or_f = askopenfilename(parent=win, initialdir=os.getcwd(), title='Select File',
                                         filetypes=[('Text files', '.txt')], defaultextension='.txt')
                password.config(state=NORMAL)

        choice_button = Button(win, text='Select', command=choice,
                               font=('Cascadia Code', 10), relief='ridge', bg='#08d0fc')
        choice_button.place(x=150, y=125)

        def main_en():
            global outfile_loc, m_or_f
            # excessive print statements remove them after testing
            print(select.get())
            if select.get() == '1':
                print('passwd=', password.get(), 'infile=', infile_loc, 'outfile=', outfile_loc, 'message=', m_or_f)
                txt.encode(passwd=password.get(), infile=infile_loc, outfile=outfile_loc, message=m_or_f)
                print('Successful')
            elif select.get() == '2':
                txt.encode(passwd=password.get(), infile=infile_loc, outfile=outfile_loc, file=m_or_f)
                print('Successful')

        def enter_save(event=None):
            global outfile_loc
            m.showinfo('Procedure', 'Where would you like the encoded file to be saved?\n'
                                    'Select the path in the next window.')
            outfile_loc = asksaveasfilename(title='Save your encoded file as', filetypes=[('Text File', '.txt')],
                                            defaultextension='.txt', initialdir=os.getcwd(), parent=win)

        pass_label = Label(win, text='Set password:', font=('Cascadia Code', 10)).place(x=20, y=145)
        pass_button = Button(win, text='Enter', relief='ridge', command=enter_save,
                             font=('Cascadia Code', 10), bg='#5ae80e')
        pass_button.place(x=145, y=170)

        main = Button(win, text='Main', command=main_en, bg='#eba823')
        main.place(x=180, y=250)

    def decode():
        pass

    encoding = Button(win, text='Encode data', command=encode, relief='ridge', font=('Cascadia Code', 10), bg='#f00c58')
    encoding.place(x=40, y=360)
    ho.CreateToolTip(encoding, 'Encodes your\npreferred data\nin your preferred text file.')
    decoding = Button(win, text="Decode data", command=decode, relief='ridge', font=('Cascadia Code', 10), bg='#6b0cf0')
    decoding.place(x=180, y=360)
    ho.CreateToolTip(decoding, "Decodes the data if it's\npresent in the file")

    win.mainloop()


def image_steno(event=None):
    pass


def audio_steno(event=None):
    pass


lb = Label(root, text="Steno\n- Ultimate Stenography", font=('Showcard Gothic', 20))
lb.place(x=20, y=20)
text = Button(root, text='Text\nStenography', command=text_steno, relief='flat',
              bg='#A68064', font=('Cascadia Code', 10))
text.place(x=56, y=250)
ho.CreateToolTip(text, 'Click here\nto hide your\ndata in a text file')
image = Button(root, text='Image\nStenography', command=image_steno, relief='flat',
               bg='#A68064', font=('Cascadia Code', 10))
image.place(x=156, y=250)
ho.CreateToolTip(image, 'Click here\nto hide your\ndata in an image file')
audio = Button(root, text='Audio\nStenography', command=audio_steno, relief='flat',
               bg='#A68064', font=('Cascadia Code', 10))
audio.place(x=256, y=250)
ho.CreateToolTip(audio, 'Click here\nto hide data in\n an audio file.')
root.mainloop()
