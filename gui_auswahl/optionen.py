import tkinter as tk
import tkinter.ttk as ttk
import webbrowser


class Optionen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.eqdkp_name = tk.StringVar()
        self.eqdkp_pass = tk.StringVar()
        ##
        ## DEBUG: Das setzen von eqdkp_name und eqdkp_pass muss entfernt werden.
        self.eqdkp_name.set('Rheilo')
        self.eqdkp_pass.set('Pass!234')
        self._erstelle_gui()


    def _erstelle_gui(self):
        ##
        ## Login Daten für EQDKP
        acc_daten_eqdkp = ttk.Labelframe(self, text='Login Daten EQDKP')
        acc_daten_eqdkp.grid_columnconfigure(1, weight=1)
        lbl = tk.Label(acc_daten_eqdkp, text='https://www.canadian-crew.de', fg='blue', cursor='hand2')
        lbl.grid(column=0, row=0, columnspan=2, sticky="nsw")
        lbl.bind('<Button-1>', lambda e : webbrowser.open_new_tab('https://www.canadian-crew.de/'))
        lbl1 = tk.Label(acc_daten_eqdkp, text='Benutzername:')
        lbl1.grid(column=0, row=1)
        _eqdkp_name = ttk.Entry(acc_daten_eqdkp, name = 'eqdkp_name', textvariable = self.eqdkp_name)
        _eqdkp_name.grid(column=1, row=1, pady='3', padx='3', sticky='news')
        lbl2 = tk.Label(acc_daten_eqdkp, text='Passwort:')
        lbl2.grid(column=0, row=2, sticky='nsw')
        _eqdkp_pass = ttk.Entry(acc_daten_eqdkp, name = 'eqdkp_pass', textvariable = self.eqdkp_pass)
        _eqdkp_pass.grid(column=1, row=2, pady='4', padx='3', sticky='news')
        acc_daten_eqdkp.pack(
            side='top',
            fill='x',
            expand=False,
            padx='6',
            pady='6'
        )