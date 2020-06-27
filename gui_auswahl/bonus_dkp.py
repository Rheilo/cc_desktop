import tkinter as tk
import tkinter.ttk as ttk


class BonusDKP(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text='Link zum Raid').grid(
            column = 0,
            row = 1,
            sticky = 'nws'
        )
        self.link_log = tk.StringVar()
        self.link_log.set('https://canadian-crew.de/admin/manage_raids.php?s=&r=63&upd=true') # DEBUG: Bei realeas diese Zeile Löschen.
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
        #finde alle such felder.
        #/html[@class='no-touch']/body[@id='top']/div[@class='ui-multiselect-menu ui-widget ui-widget-content ui-corner-all']/div[@class='ui-widget-header ui-corner-all ui-multiselect-header ui-helper-clearfix ui-multiselect-hasfilter']/div[@class='ui-multiselect-filter']/input