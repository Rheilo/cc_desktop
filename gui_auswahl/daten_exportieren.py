import tkinter as tk


class DatenExportieren(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text='Link zum Raid').grid(
            column = 0,
            row = 0,
            sticky = 'nws'
        )
        self._link_addr = tk.StringVar()
        self._link_addr.set('https://canadian-crew.de/admin/manage_raids.php?s=&r=63&upd=true') # DEBUG: Bei realeas diese Zeile Löschen.
        self._link = tk.Entry(self,
            name = 'tb_link',
            textvariable = self._link_addr
        )
        self._link.grid(
            column = 1,
            row = 0,
            sticky = 'news',
            padx = '8',
            pady = '4'
        )