import os
import tkinter.scrolledtext as st
from tkinter import *
from tkinter import messagebox as m
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import sten.hover as ho
import sten.text as txt
import sten.audio as aud

root = Tk()
root.title('Steno')
root.config(bg='#f5f59a')

root_h, root_w = 300, 400
s_w = root.winfo_screenwidth()
s_h = root.winfo_screenheight()
x_coor = int((s_w / 2) - (root_w / 2))
y_coor = int((s_h / 2) - (root_h / 2))
root.geometry("{}x{}+{}+{}".format(root_w, root_h, x_coor, y_coor))

root.resizable(False, False)
cas = ('Cascadia Code', 10)
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

        size_label = Label(win, text='', font=cas, bg='#c0ed98', fg='#f20713')
        size_label.place(x=5, y=45)
        es = Entry(win, width=55, font=cas)
        es.place(x=7, y=65)

        m.showinfo("Procedure", "You will be asked to select\na file in which the data\nwill be hidden.")
        infile_loc = askopenfilename(parent=win, initialdir=os.getcwd(), title='Select File to ENCODE',
                                     filetypes=[('Text files', '.txt')], defaultextension='.txt')
        size_label.configure(text='Your data will be hidden inside-'.format(infile_loc))
        es.insert(0, infile_loc)
        # TODO add a widget where user will be able to see contents of their chosen file

        ch_lb = Label(win, text='Select what you want to hide', bg='#c0ed98', fg='#1046b3', font=cas)
        ch_lb.place(x=5, y=85)
        select = StringVar(win)
        style = ttk.Style(master=win)
        style.configure('C.TRadiobutton', font=cas, background='#c0ed98', foreground='#1046b3')

        choice_message = ttk.Radiobutton(win, text='Hide a Message', value="1", variable=select,
                                         style='C.TRadiobutton')
        choice_message.place(x=5, y=105)

        choice_file = ttk.Radiobutton(win, text='Hide a File', value="2", variable=select, style='C.TRadiobutton')
        choice_file.place(x=5, y=130)

        password = Entry(win, width=20, show='*', font=cas, state=DISABLED)
        password.place(x=10, y=185)

        def choice():
            global choice_button
            if select.get() == "1":
                message = Toplevel(master=win)
                message.title('Enter Message')
                message.resizable(False, False)
                lm = Label(message, text='Enter your message that you want to hide:', bg='yellow', font=cas)
                lm.pack(side=TOP, fill=BOTH)
                ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
                t = st.ScrolledText(message)
                t.config(font=cas)
                t.pack()

                def click(event=None):
                    global m_or_f
                    password.config(state=NORMAL)
                    message.withdraw()
                    m_or_f = t.get("1.0", "end-1c")
                    password.focus()

                bm = Button(message, text='Done(Ctrl-b)', command=click, relief='flat', bg='yellow', font=cas)
                bm.pack(side=BOTTOM, fill=BOTH)
                ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
                message.bind('<Control-b>', click)
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
                password.focus()

        choice_button = Button(win, text='Select', command=choice, bg='#08d0fc', font=cas, relief='ridge')
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

        pass_label = Label(win, text='Set password:', font=cas, bg='#c0ed98', fg='#1046b3')
        pass_label.place(x=10, y=155)

        pass_button = Button(win, image=img, relief='ridge', bg='#36f5eb', command=process)
        pass_button.place(x=195, y=180)
        ho.CreateToolTip(pass_button, 'Show/ Hide password')
        success = Label(win, bg='#c0ed98', font=cas, fg='red')
        success.place(x=20, y=280)

        def execute():
            global outfile_loc, m_or_f
            m.showinfo('Procedure', 'Where would you like the encoded file to be saved?\n'
                                    'Select the path in the next window.')
            outfile_loc = asksaveasfilename(title='Save your encoded file as', filetypes=[('Text File', '.txt')],
                                            defaultextension='.txt', initialdir=os.getcwd(), parent=win)
            if password.get() != '' and infile_loc != '' and outfile_loc != '' and m_or_f != '' and es.get() != '':
                if select.get() == '1':
                    try:
                        txt.encode(passwd=password.get(), infile=es.get(), outfile=outfile_loc, message=m_or_f)
                        success.config(text='Successfully encoded message in\n{}'.format(outfile_loc))
                    except FileNotFoundError:
                        txt.encode(passwd=password.get(), infile=infile_loc, outfile=outfile_loc, message=m_or_f)
                        success.config(text='Successfully encoded message in\n{}'.format(outfile_loc))
                elif select.get() == '2':
                    try:
                        txt.encode(passwd=password.get(), infile=es.get(), outfile=outfile_loc, file=m_or_f)
                        success.config(text='Successfully encoded file\n{} in\n{}'.format(m_or_f, outfile_loc))
                    except FileNotFoundError:
                        txt.encode(passwd=password.get(), infile=infile_loc, outfile=outfile_loc, file=m_or_f)
                        success.config(text='Successfully encoded file\n{} in\n{}'.format(m_or_f, outfile_loc))
            else:
                m.showerror('ERROR', 'Something went wrong\ntry again.')

        main = Button(win, text='Hide Data', command=execute, bg='#eba823', relief='ridge', font=cas)
        main.place(x=20, y=250)
        ho.CreateToolTip(main, 'Checks everything\nthen encodes the data')

        # TODO show contents of file after encoding[optional]

        def refresh():
            if choice_button['state'] == DISABLED:
                choice_button.config(state=NORMAL)

        refresh = Button(win, text='Refresh', command=refresh, state=DISABLED, relief='ridge', font=cas, bg='#fca903')
        refresh.place(x=360, y=122)
        ho.CreateToolTip(refresh, 'Refreshes Page')

    def decode():
        dec = Toplevel(master=root)
        dec.title('Text Steno-DECODE')
        dec.geometry('480x250')
        dec.config(bg='#c0ed98')
        dec_label = Label(dec, text='Text -Stenography[DECODE]', font=('Cascadia Code', 20), bg='#c0ed98', fg='#1046b3')
        dec_label.place(x=5, y=4)
        info_label = Label(dec, text='Chosen File:', font=cas, bg='#c0ed98', fg='#f20713')
        info_label.place(x=5, y=60)
        m.showinfo("Procedure", "You will be asked to select\na file which contains hidden data.")

        file_loc = askopenfilename(parent=dec, initialdir=os.getcwd(), title='Select File to ENCODE',
                                   filetypes=[('Text files', '.txt')], defaultextension='.txt')
        file_ent = Entry(master=dec, width=55, font=cas)
        file_ent.place(x=7, y=85)
        file_ent.insert(0, file_loc)
        pass_lb = Label(dec, text='Enter password:', bg='#c0ed98', fg='#1046b3', font=cas)
        pass_lb.place(x=5, y=110)
        pass_ent = Entry(dec, width=20, font=cas, show='*')
        pass_ent.place(x=7, y=135)
        pass_ent.focus()

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
                text_win.resizable(False, False)
                show_lb = Label(text_win, text='The message hidden in the selected file:',
                                bg='yellow', fg='red', font=cas)
                show_lb.pack(side=TOP, fill=BOTH)
                show_text = st.ScrolledText(text_win)
                show_text.pack()
                show_text.tag_configure('beauty', font=cas)
                show_text.insert(INSERT, data, 'beauty')
                show_text.config(state=DISABLED)
                show_bu = Button(text_win, text='Exit', bg='yellow', fg='red',
                                 command=text_win.destroy, font=cas)
                show_bu.pack(side=BOTTOM, fill=BOTH)
                ho.CreateToolTip(show_bu, 'Closes the window')

        decode_main = Button(dec, text='Decode', relief='ridge', bg='#00fc69', font=cas, command=work)
        decode_main.place(x=10, y=190)
        ho.CreateToolTip(decode_main, 'Checks the requirements then\nshows the decoded data.')
        exit_dec = Button(dec, text='Exit', bg='#eb3131', font=cas, relief='ridge',
                          command=dec.destroy)
        exit_dec.place(x=360, y=200)
        ho.CreateToolTip(exit_dec, 'Closes the window')
        dec.bind('<Return>', work)

    encoding = Button(win, text='Encode data', command=encode, relief='ridge', font=cas, bg='#f00c58')
    encoding.place(x=40, y=360)
    ho.CreateToolTip(encoding, 'Encoding data function')
    decoding = Button(win, text="Decode data", command=decode, relief='ridge', font=cas, bg='#6b0cf0')
    decoding.place(x=180, y=360)
    ho.CreateToolTip(decoding, "Decoding data function")
    exit_win = Button(win, text='Exit', bg='#eb3131', font=cas, relief='ridge', command=win.destroy)
    exit_win.place(x=360, y=360)
    ho.CreateToolTip(exit_win, 'Closes the window')


def image_steno():
    # TODO complete image related stenography func
    pass


def audio_steno():
    aud_win = Toplevel(master=root)
    aud_win.title('Audio Steno')
    aud_win.geometry('515x260')
    aud_win.config(bg='#c3f0fa')
    au_lb = Label(aud_win, text='Audio -Stenography', bg='#c3f0fa', fg='#fa05bd', font=('Cascadia Code', 20))
    au_lb.place(x=10, y=10)

    def em_aud():
        global file, mess
        select_lb = Label(aud_win, text='Select File:', font=cas, bg='#c3f0fa', fg='#fa0505')
        select_lb.place(x=5, y=50)
        file_au = Entry(aud_win, width=55, font=cas, relief='ridge')
        file_au.place(x=7, y=75)
        file_au.focus()

        def browse():
            global file
            file = askopenfilename(parent=aud_win, initialdir=os.getcwd(), title='Select File to EMBED',
                                   filetypes=[('Audio files', '.wav')], defaultextension='.wav')
            file_au.delete(0, END)
            file_au.insert(0, file)
            select_lb.config(text='Selected File:')

        se_bu = Button(aud_win, text='Browse', bg='#8ed925', font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)

        def pan():
            global mess
            message = Toplevel(aud_win)
            message.title('Enter Message')
            message.resizable(False, False)
            lm = Label(message, text='Enter your message that you want to hide:', bg='yellow', font=cas)
            lm.pack(side=TOP, fill=BOTH)
            ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
            t = st.ScrolledText(message)
            t.config(font=cas)
            t.pack()

            def click(event=None):
                global mess
                message.withdraw()
                mess = t.get("1.0", "end-1c")

            bm = Button(message, text='Done(Ctrl-b)', command=click, relief='flat', bg='yellow', font=cas)
            bm.pack(side=BOTTOM, fill=BOTH)
            ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
            message.bind('<Control-b>', click)

        b = Button(aud_win, command=pan, text='Enter Message', font=cas, bg='#94f748')
        b.place(x=10, y=100)
        success = Label(aud_win, bg='#c3f0fa', font=cas)
        success.place(x=10, y=170)

        def done():
            global file, mess
            m.showinfo('Procedure', 'Where would you like the encoded file to be saved?\n'
                                    'Select the path in the next window.')
            out = asksaveasfilename(title='Save your embedded file as', filetypes=[('Audio File', '.wav')],
                                    defaultextension='.wav', initialdir=os.getcwd(), parent=aud_win)
            if mess != '' and file != '' and file_au.get() != '':
                try:
                    aud.embed(infile=file, message=mess, outfile=out)
                    success.config(text='Successfully embedded in\n{}'.format(out))
                except FileNotFoundError:
                    aud.embed(infile=file_au.get(), message=mess, outfile=out)
                    success.config(text='Successfully embedded in\n{}'.format(out))
            else:
                m.showerror('ERROR', 'Something went wrong try again')

        main_bu = Button(aud_win, text='Embed Message', bg='#f79205', font=cas, command=done)
        main_bu.place(x=10, y=130)

    def ex_aud():
        # TODO complete extracting func
        pass

    bu_en = Button(aud_win, text='Embed', font=cas, bg='#05ff82', fg='#0569ff', command=em_aud)
    bu_en.place(x=70, y=220)
    ho.CreateToolTip(bu_en, 'Embeds data in audio file')
    bu_ex = Button(aud_win, text='Extract', font=cas, bg='#acff05', fg='#fa029b', command=ex_aud)
    bu_ex.place(x=260, y=220)
    ho.CreateToolTip(bu_ex, 'Extracts data from audio file')


lb = Label(root, text="Steno\n- Ultimate Stenography", font=('Showcard Gothic', 20), bg='#f5f59a', fg='#8507fa')
lb.place(x=18, y=20)

text = Button(root, text='Text\nStenography', relief='flat', bg='#A68064', command=text_steno, font=cas)
text.place(x=56, y=250)
ho.CreateToolTip(text, 'Click here\nto hide your\ndata in a text file')

image = Button(root, text='Image\nStenography', relief='flat', bg='#A68064', command=image_steno, font=cas)
image.place(x=156, y=250)
ho.CreateToolTip(image, 'Click here\nto hide your\ndata in an image file')

audio = Button(root, text='Audio\nStenography', relief='flat', bg='#A68064', command=audio_steno, font=cas)
audio.place(x=256, y=250)
ho.CreateToolTip(audio, 'Click here\nto hide data in\n an audio file.')

root.mainloop()
