import sys
import newgui as ng
from tkinter import *
from tkinter import filedialog, _setit
import mail
from threading import Thread
import os



def _sending(user, psw, subj, content):
    user = user.get()
    psw = psw.get()
    subj = subj.get()
    content = content.get()

    l = [user, psw, subj, content]
    for i in l:
        if i==None :
            print("missing parameter")
            sys.exit(1)

    mail.mailer(user, psw, subj, content)

    return



class _FrameScelta(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()


        self.entry = Entry(self, width=50)
        self.entry.grid(row=0, column=1)
        button_content = Button(self, text="Scegli il contenuto", width=20, command=lambda: self.openContenuto())
        button_content.grid(row=0, column=0)

    _entry = None

    def openContenuto(self):
        tmp = filedialog.askopenfilename(title="Select content file", filetypes=(("HTML file", "*.html"),))
        self.entry.delete(0, END)
        self.entry.insert(0, tmp)
        return


def gui():
    root = Tk()
    root.geometry("600x150")
    root.resizable(0, 0)
    root.title('Bulk Mailer')


    inputframe = Frame(root)
    inputframe.pack()

    user = Label(inputframe, text="UserName")
    user.grid(row=0, column=0)
    userin = Entry(inputframe, width=40)
    userin.grid(row=0, column=1)

    psw = Label(inputframe, text="Password")
    psw.grid(row=1, column=0)
    pswin = Entry(inputframe, show="*", width=40)
    pswin.grid(row=1, column=1)

    sub = Label(inputframe, text="Subject")
    sub.grid(row=2, column=0)
    subin = Entry(inputframe, width=40)
    subin.grid(row=2, column=1)

    frame_scelta = _FrameScelta(root)

    framei = Frame(root)
    framei.pack()
    button_iscritti = Button(framei, text='Iscritti', bg='#000888fff', width=25, command=lambda: ng.newgui(root))
    button_iscritti.pack()

    frame2 = Frame(root)
    frame2.pack(side=BOTTOM)

    button_send = Button(frame2,
                         text='Send',
                         bg='green',
                         width=25,
                         command=lambda: Thread(target=_sending, args=(userin, pswin, subin, frame_scelta.entry)).start())
    button_send.pack(side=RIGHT)

    #button_close = Button(frame2, text='Close', width=25, command=lambda: Thread(target=sys.exit))
    #button_close.pack(side=RIGHT)
    button_stop = Button(frame2, text='Forced Stop', bg='red', width=15, command=lambda: os._exit(0))
    button_stop.pack(side=LEFT)


    root.mainloop()


def main():
    print('------------------------------------------------------------------------------')
    print('Bulk Mailer 2.0 by Davide Casalini')
    print('This version is faster but less reliable, if forced to stop db ')
    print('could not be updated completely')
    print('BTW no big deal !!')
    print('\n')
    print('if app token is not working, just leave the box empty, but connection may be ')
    print('subject to throttling')
    print('------------------------------------------------------------------------------')
    gui()


if __name__ == "__main__":
    sys.exit(main())
