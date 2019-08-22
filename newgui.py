from tkinter import *
import database as db
from tkinter import filedialog
import filer
from threading import Thread
import downloadjson as dj


def stampa():
    tmp = db._getalliscritti()
    print(tmp)
    print('La lista è lunga : ', len(tmp))
    count = 0
    for i in tmp:
        if i[1]:
            count += 1
    print('la mail è stata ricevuta da :', count, ' iscritti')


class _FrameScelta(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()

        user = Label(self, text="Upload Subscribers")
        user.grid(row=0, column=0)
        self.entry = Entry(self, width=50)
        self.entry.grid(row=0, column=1)
        button_content = Button(self, text="Scegli il file", width=20, command=lambda: self.uploadIscritti())
        button_content.grid(row=0, column=2)
        #thread = Thread(target=, args=)
        button_content = Button(self,
                                text="Upload!",
                                bg='green',
                                width=20,
                                command=lambda: Thread(target=filer.aggiungiscritti,
                                                       args= (self.entry.get(),)
                                                       ).start()
                                )#filer.aggiungiscritti(self.entry.get()))
        button_content.grid(row=0, column=3)


    entry = None

    def uploadIscritti(self):
        tmp = filedialog.askopenfilename(title="Select subscribers file",
                                         filetypes=(("excel", "*.xls"),("text", "*.txt"),("JSON", "*.json")))
        self.entry.delete(0, END)
        self.entry.insert(0, tmp)
        return


class _FrameDownloadJson(Frame):

    entry = None

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()

        user = Label(self, text="Paste json URL")
        user.grid(row=0, column=0)
        self.entry = Entry(self, width=100)
        self.entry.grid(row=0, column=1)
        #thread = Thread(target=, args=)
        button_content = Button(self,
                                text="Download and Query!",
                                bg='green',
                                width=20,
                                command=lambda: Thread(target=dj.json_url_query,
                                                       args= (self.entry.get(),)
                                                       ).start()
                                )#filer.aggiungiscritti(self.entry.get()))
        button_content.grid(row=0, column=2)



class _FrameOpenData(Frame):

    domain = None
    data_id = None
    token = None

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()

        user = Label(self, text="Copy SODA endpoint api (domain - dataset_id - token)")
        user.grid(row=0, column=0)
        self.domain = Entry(self, width=30)
        self.domain.grid(row=0, column=1)
        self.data_id = Entry(self, width=10)
        self.data_id.grid(row=0, column=2)
        self.token = Entry(self, width=30)
        self.token.grid(row=0, column=3)
        #thread = Thread(target=, args=)
        button_content = Button(self,
                                text="Download!",
                                bg='green',
                                width=20,
                                command=lambda: Thread(target=dj.downloadata,
                                                       args=(self.domain.get(), self.data_id.get(), self.token.get())
                                                       ).start()
                                )#filer.aggiungiscritti(self.entry.get()))
        button_content.grid(row=0, column=4)



def newgui(parent):
    root = Toplevel(parent)
    root.geometry("900x150")
    root.resizable(0, 0)
    root.title('Subscribers Managing')

    inputframe = Frame(root)
    inputframe.pack()

    user = Label(inputframe, text="Delete subscriber")
    user.grid(row=0, column=0)
    userin = Entry(inputframe, width=40)
    userin.grid(row=0, column=1)
    button_close = Button(inputframe, text='Delete!', bg='red', width=25, command=lambda: db.deleteiscritto(userin.get()))
    button_close.grid(row=0, column=2)

    fram = _FrameScelta(root)
    framopdat = _FrameOpenData(root)
    framejson = _FrameDownloadJson(root)

    bottom_frame = Frame(root)
    bottom_frame.pack(side=BOTTOM)
    button_subs = Button(bottom_frame, text='Print Subs!', bg='#000888fff', width=25, command=lambda: stampa())
    button_subs.pack(side=RIGHT)
    button_res_subs = Button(bottom_frame,
                             text='Reset Subs count!',
                             bg='red',
                             width=25,
                             command=lambda: Thread(target=db._resetiscritti).start())#db._resetiscritti())
    button_res_subs.pack(side=LEFT)
    # button_close = Button(bottom_frame, text='Close', bg='#fff555000', width=25, command=lambda: root.destroy())
    # button_close.pack(side=RIGHT)

    root.mainloop()
