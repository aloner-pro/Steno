import os
import tkinter.scrolledtext as st
from tkinter import *
from tkinter import messagebox as m
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import sten.hover as ho
import sten.text as txt

root = Tk()
root.title('Steno')
root.config(bg='#f5f59a')
root.geometry('400x300')
img = PhotoImage(file="images/noshow.png").subsample(4, 4)
img2 = PhotoImage(file="images/show.png").subsample(4, 4)


def text_steno():
    win = Toplevel(master=root)
    win.title('Text Steno')
    win.geometry('480x400')
    win.config(bg='#c0ed98')
    win_label = Label(win, text='Text -Stenography', font=('Cascadia Code', 20), bg='#c0ed98', fg='#1046b3')
    win_label.place(x=5, y=4)

    def encode():
        global choice_button
        outfile_loc, m_or_f = '', ''

        size_label = Label(win, text='', font=('Cascadia Code', 10), bg='#c0ed98', fg='#f20713')
        size_label.place(x=5, y=45)
        es = Entry(win, width=55, font=('Cascadia Code', 10))
        es.place(x=7, y=65)

        m.showinfo("Procedure", "You will be asked to select\na file in which the data\nwill be hidden.")
        infile_loc = askopenfilename(parent=win, initialdir=os.getcwd(), title='Select File to ENCODE',
                                     filetypes=[('Text files', '.txt')], defaultextension='.txt')
        size_label.configure(text='Your data will be hidden inside-'.format(infile_loc))
        es.insert(0, infile_loc)

        ch_lb = Label(win, text='Select what you want to hide', bg='#c0ed98', fg='#1046b3',
                      font=('Cascadia Code', 10))
        ch_lb.place(x=5, y=85)
        select = StringVar(win)
        style = ttk.Style(master=win)
        style.configure('C.TRadiobutton', font=('Cascadia Code', 10), background='#c0ed98', foreground='#1046b3')

        choice_message = ttk.Radiobutton(win, text='Hide a Message', value="1", variable=select,
                                         style='C.TRadiobutton')
        choice_message.place(x=5, y=105)

        choice_file = ttk.Radiobutton(win, text='Hide a File', value="2", variable=select, style='C.TRadiobutton')
        choice_file.place(x=5, y=130)

        password = Entry(win, width=20, show='*', font=('Cascadia Code', 10), state=DISABLED)
        password.place(x=18, y=185)
        password.focus()

        def choice():
            global choice_button
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
                    password.config(show="")
                    pass_button.config(image=img2)
                elif password["show"] == "":
                    password.config(show='*')
                    pass_button.config(image=img)

        pass_label = Label(win, text='Set password:', font=('Cascadia Code', 10), bg='#c0ed98', fg='#1046b3')
        pass_label.place(x=10, y=155)

        pass_button = Button(win, image=img, relief='ridge', bg='#36f5eb', command=process)
        pass_button.place(x=195, y=180)
        ho.CreateToolTip(pass_button, 'Show/ Hide password')
        success = Label(win, text='', bg='#c0ed98', font=('Cascadia Code', 10), fg='red')
        success.place(x=20, y=280)

        def execute():
            global outfile_loc, m_or_f
            m.showinfo('Procedure', 'Where would you like the encoded file to be saved?\n'
                                    'Select the path in the next window.')
            outfile_loc = asksaveasfilename(title='Save your encoded file as', filetypes=[('Text File', '.txt')],
                                            defaultextension='.txt', initialdir=os.getcwd(), parent=win)
            if select.get() == '1':
                if password.get() != '' and infile_loc != '' and outfile_loc != '' and m_or_f != '' and es.get() != '':
                    try:
                        txt.encode(passwd=password.get(), infile=es.get(), outfile=outfile_loc, message=m_or_f)
                        success.config(text='Successfully encoded message in\n{}'.format(outfile_loc))
                    except FileNotFoundError:
                        txt.encode(passwd=password.get(), infile=infile_loc, outfile=outfile_loc, message=m_or_f)
                        success.config(text='Successfully encoded message in\n{}'.format(outfile_loc))
                else:
                    m.showerror('ERROR', 'Something went wrong\ntry again.')
            elif select.get() == '2':
                if password.get() != '' and infile_loc != '' and outfile_loc != '' and m_or_f != '' and es.get() != '':
                    try:
                        txt.encode(passwd=password.get(), infile=es.get(), outfile=outfile_loc, file=m_or_f)
                        success.config(text='Successfully encoded file {} in\n{}'.format(m_or_f, outfile_loc))
                    except FileNotFoundError:
                        txt.encode(passwd=password.get(), infile=infile_loc, outfile=outfile_loc, file=m_or_f)
                        success.config(text='Successfully encoded file {} in\n{}'.format(m_or_f, outfile_loc))
                else:
                    m.showerror('ERROR', 'Something went wrong\ntry again.')

        main = Button(win, text='Hide Data', command=execute, bg='#eba823', relief='ridge',
                      font=('Cascadia Code', 10))
        main.place(x=20, y=250)
        ho.CreateToolTip(main, 'Checks everything\nthen encodes the data')

        def refresh():
            if choice_button['state'] == DISABLED:
                choice_button.config(state=NORMAL)

        refresh = Button(win, text='Refresh', command=refresh, state=DISABLED, relief='ridge',
                         font=('Cascadia Code', 10), bg='#fca903')
        refresh.place(x=360, y=122)
        ho.CreateToolTip(refresh, 'Refreshes Page')

    def decode():
        dec = Toplevel(master=root)
        dec.title('Text Steno-DECODE')
        dec.geometry('480x250')
        dec.config(bg='#c0ed98')
        dec_label = Label(dec, text='Text -Stenography[DECODE]', font=('Cascadia Code', 20), bg='#c0ed98', fg='#1046b3')
        dec_label.place(x=5, y=4)
        info_label = Label(dec, text='Chosen File:', font=('Cascadia Code', 10), bg='#c0ed98', fg='#f20713')
        info_label.place(x=5, y=60)
        m.showinfo("Procedure", "You will be asked to select\na file which contains hidden data.")

        file_loc = askopenfilename(parent=dec, initialdir=os.getcwd(), title='Select File to ENCODE',
                                   filetypes=[('Text files', '.txt')], defaultextension='.txt')
        file_ent = Entry(master=dec, width=55, font=('Cascadia Code', 10))
        file_ent.place(x=7, y=85)
        file_ent.insert(0, file_loc)
        pass_lb = Label(dec, text='Enter password:', bg='#c0ed98', fg='#1046b3', font=('Cascadia Code', 10))
        pass_lb.place(x=5, y=110)
        pass_ent = Entry(dec, width=20, font=('Cascadia Code', 10), show='*')
        pass_ent.place(x=7, y=135)

        def show():
            if pass_ent["state"] == ACTIVE or pass_ent['state'] == NORMAL:
                if pass_ent["show"] == '*':
                    pass_ent.config(show="")
                    pass_bu.config(image=img2)
                elif pass_ent["show"] == "":
                    pass_ent.config(show='*')
                    pass_bu.config(image=img)

        pass_bu = Button(dec, image=img, command=show, bg='#36f5eb', relief='ridge')
        pass_bu.place(x=190, y=130)
        ho.CreateToolTip(pass_bu, 'Show/ Hide password')

        def work(event=None):
            global data
            try:
                data = txt.decode(passwd=pass_ent.get(), file=file_ent.get())
            except FileNotFoundError:
                data = txt.decode(passwd=pass_ent.get(), file=file_loc)
            finally:
                text_win = Toplevel(dec)
                text_win.title('Decoded Message')
                show_lb = Label(text_win, text='The message hidden in the selected file:', bg='yellow', fg='red',
                                font=('Cascadia Code', 10))
                show_lb.pack(side=TOP, fill=BOTH)
                show_text = st.ScrolledText(text_win)
                show_text.pack()
                show_text.tag_configure('beauty', font=('Cascadia Code', 10))
                show_text.insert(INSERT, data, 'beauty')
                show_text.config(state=DISABLED)
                show_bu = Button(text_win, text='Exit', bg='yellow', fg='red',
                                 command=text_win.destroy, font=('Cascadia Code', 10))
                show_bu.pack(side=BOTTOM, fill=BOTH)
                ho.CreateToolTip(show_bu, 'Closes the window')

        decode_main = Button(dec, text='Decode', relief='ridge', bg='#00fc69', font=('Cascadia Code', 10), command=work)
        decode_main.place(x=10, y=190)
        ho.CreateToolTip(decode_main, 'Checks the requirements then\nshows the decoded data.')
        exit_dec = Button(dec, text='Exit', bg='#eb3131', font=('Cascadia Code', 10), relief='ridge',
                          command=dec.destroy)
        exit_dec.place(x=360, y=200)
        ho.CreateToolTip(exit_dec, 'Closes the window')
        dec.bind('<Return>', work)

    encoding = Button(win, text='Encode data', command=encode, relief='ridge', font=('Cascadia Code', 10), bg='#f00c58')
    encoding.place(x=40, y=360)
    ho.CreateToolTip(encoding, 'Encoding data function')
    decoding = Button(win, text="Decode data", command=decode, relief='ridge', font=('Cascadia Code', 10), bg='#6b0cf0')
    decoding.place(x=180, y=360)
    ho.CreateToolTip(decoding, "Decoding data function")
    exit_win = Button(win, text='Exit', bg='#eb3131', font=('Cascadia Code', 10), relief='ridge', command=win.destroy)
    exit_win.place(x=360, y=360)
    ho.CreateToolTip(exit_win, 'Closes the window')


def image_steno():
    pass


def audio_steno():
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
