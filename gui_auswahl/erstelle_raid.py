import tkinter as tk
import tkinter.ttk as ttk


class ErstelleRaid(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid_columnconfigure(1, weight=1)
        self.auswahl = tk.IntVar()
        self.auswahl.set(2)
        frm = ttk.Labelframe(self, text='Auswahl der Datenbasis')
        frm.grid(
            column = 0,
            row = 0,
            columnspan = 2,
            sticky = 'new'
        )
        tk.Radiobutton(
            frm,
            text='classic.warcraftlogs.com',
            value=1,
            variable=self.auswahl
        ).grid(column=0, row=0)
        tk.Radiobutton(
            frm,
            text='AddOn',
            value=2,
            variable=self.auswahl
        ).grid(column=1, row=0)
        tk.Label(self, text='Link zum Log').grid(
            column = 0,
            row = 1,
            sticky = 'nws'
        )
        self.link_log = tk.StringVar()
        self.link_log.set('https://classic.warcraftlogs.com/reports/6vmyj1aqMThkYb8R/') # DEBUG: Bei realeas diese Zeile Löschen.
        self.__link = tk.Entry(self,
            name = 'tb_link',
            textvariable = self.link_log
        )
        self.__link.grid(
            column = 1,
            row = 1,
            sticky = 'news',
            padx = '8',
            pady = '4'
        )