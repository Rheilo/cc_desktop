import tkinter as tk
import tkinter.ttk as ttk
from threading import Lock

class BonusDKP(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.lock = Lock()
        self.play = False
        self.weiter = False
        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text='Link zum Raid').grid(
            column = 0,
            row = 1,
            sticky = 'nws'
        )
        self.link_raid = tk.StringVar()
        self.link_raid.set('https://canadian-crew.de/admin/manage_raids.php?s=&r=63&upd=true') # DEBUG: Bei realeas diese Zeile Löschen.
        self.__link = tk.Entry(self,
            name = 'tb_link',
            textvariable = self.link_raid
        )
        self.__link.grid(
            column = 1,
            row = 1,
            sticky = 'news',
            padx = '8',
            pady = '4'
        )
        frm = tk.Frame(self)
        frm.grid(column=0, row=0, columnspan=2, sticky='news')
        self.btn_play = ttk.Button(
            frm,
            name='btn_play',
            text='Start',
            command=self.__play)
        btn_next = ttk.Button(
            frm,
            name='btn_next',
            text='Weiter',
            command=self.__weiter)
        self.btn_play.pack(side='left')
        btn_next.pack(side='left')


    def __weiter(self):
        self.lock.acquire()
        self.weiter = True
        self.lock.release()
        print('YES')

    
    def __play(self):
        self.lock.acquire()
        self.play = False if self.play else True
        self.lock.release()
        if self.play:
            self.btn_play.configure(text='Pause')
        else:
            self.btn_play.configure(text='Start')
        #finde alle such felder.
        #/html[@class='no-touch']/body[@id='top']/div[@class='ui-multiselect-menu ui-widget ui-widget-content ui-corner-all']/div[@class='ui-widget-header ui-corner-all ui-multiselect-header ui-helper-clearfix ui-multiselect-hasfilter']/div[@class='ui-multiselect-filter']/input