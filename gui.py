import tkinter as tk
from tkinter.font import Font
import tkinter.ttk as ttk
import logic as l
import threading as thread
##
## Die einzelnen GUI's für die Funktionen
from gui_auswahl.daten_exportieren import DatenExportieren
from gui_auswahl.optionen import Optionen


from pprint import pprint


class App_(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._erstelle_gui()


    def _erstelle_gui(self):
        self.geometry('480x800+{0:d}+{1:d}'.format(
            int(self.winfo_screenwidth() / 2 - 480/2),
            int(self.winfo_screenheight() / 2 - 800/2)
        ))
        ##
        ## Button Zeile
        frm1 = tk.Frame(self)
        frm1.pack(side=tk.TOP, fill=tk.X, expand=False)
        self.btn_hole_item_ID = tk.Button(
            frm1,
            name='btn_hole_item_ID', 
            text='Finde Item IDs',
            command=self.btn_hole_item_ID_clicked
        )
        self.btn_hole_item_ID.pack(side=tk.LEFT)
        frm2 = tk.Frame(frm1)
        frm2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        lbl_name = tk.Label(frm2, name='name', text='Benutzername:')
        lbl_name.grid(row=0, column=0)
        self.tb_name_val = tk.StringVar()
        self.tb_name_val.set('Rheilo') #DEBUG: Variable wird vorab gefüllt zum Testen
        tb_name = tk.Entry(frm2, name='tb_name', textvariable=self.tb_name_val)
        tb_name.grid(row=0, column=1)
        lbl_pass = tk.Label(frm2, name='pass', text='Passwort:', anchor=tk.W)
        lbl_pass.grid(row=1, column=0)
        self.tb_pass_val = tk.StringVar()
        #self.tb_pass_val.set('Pass!234') #DEBUG: Variable wird vorab gefüllt zum Testen
        tb_pass = tk.Entry(frm2, name='tb_pass', textvariable=self.tb_pass_val)
        tb_pass.grid(row=1, column=1)
        self.btn_export_to_eqdkp = tk.Button(
            frm1,
            name = 'btn_export_to_exdkp',
            text = 'Export -> EQDKP',
            command = self.btn_export_to_eqdkp_clicked
        )
        self.btn_export_to_eqdkp.pack(side=tk.LEFT)
        self.btn_load_loot_table = tk.Button(
            frm1,
            name = 'btn_load_loot_table',
            text = 'Daten laden',
            command = self.btn_load_loot_table_clicked
        )
        self.btn_load_loot_table.pack(side=tk.LEFT)
        frm3 = tk.Frame(self)
        frm3.pack(side=tk.TOP, fill=tk.X)
        lbl = tk.Label(frm3, text='Link zum Raid: ')
        lbl.pack(side=tk.LEFT)
        self.tb_link_raid = tk.StringVar()
        self.tb_link_raid.set('https://canadian-crew.de/admin/manage_raids.php?s=&r=63&upd=true') #DEBUG: Variable wird vorab gefüllt zum Testen
        tb_link_raid = tk.Entry(frm3, name='tb_link_raid', textvariable=self.tb_link_raid)
        tb_link_raid.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ##
        ## Textfeld -> Input / Output der Daten
        self.daten:tk.Text = tk.Text(self, name='daten')
        self.daten.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.btn_export_to_eqdkp.bind('<Button-3>', lambda e, d=self.daten: self.debug_daten(e, d)) #DEBUG: Funktion nur für Debug zwecke eingefügt.


    ##
    ##  Verbindung zur Logik
    ##
    def btn_hole_item_ID_clicked(self):
        background_methode = thread.Thread(target=l.hole_item_id, args=(self,))
        background_methode.start()


    def btn_export_to_eqdkp_clicked(self):
        bg_worker = thread.Thread(
            target=l.export_to_eqdkp, 
            args=(
                self.daten, 
                self.tb_link_raid.get(),
                self.tb_name_val.get(),
                self.tb_pass_val.get()
            )
        )
        bg_worker.start()


    def btn_load_loot_table_clicked(self):
        l.lade_daten_from_wowhead_by_npc(self.daten, self.tb_link_raid.get())


    def debug_daten(self, e:tk.EventType.ButtonPress, d:tk.Text):
        if len(self.tb_link_raid.get()) <= 0:
            self.tb_link_raid.set('https://canadian-crew.de/admin/manage_raids.php?s=&r=63&upd=true')
        d.insert('0.0', "[Teufelsherzhörner]\t16808\tVoltox\t25\n")
        d.insert('1.0', "[Zauberdolch]\t18878\tHilo\t50\n")
        d.insert('2.0', "[Helm des Cenarius]\t16834\tNador\t5\n")
        d.insert('3.0', "[Aurastein-Hammer]\t17105\tTreehugs\t75\n")




class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Canadian Crew <Patchwerk - EU>')
        self.funktionen = {
            'Daten Exportieren': DatenExportieren(self),
            'Bounus DKP': None,
            'Raid aus dem Log Anlegen': None,
            'Finde Item IDs': None,
            'Extrakt Loot-table': None,
            'Optionen' : Optionen(self)
        }
        for frm in self.funktionen.values():
            if frm is not None:
                if frm == self.funktionen['Optionen']:
                    frm.grid(column=0, row=2, sticky='nesw', rowspan=2)
                    continue
                frm.grid(column=0, row=2, sticky='nesw')
        self._erstelle_gui()


    def _erstelle_gui(self):
        self.geometry('480x800+{0:d}+{1:d}'.format(
            int(self.winfo_screenwidth() / 2 - 480/2),
            int(self.winfo_screenheight() / 2 - 800/2)
        ))
        ##
        ## Aufteilung
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(3, weight = 1)
        frm1 = tk.Frame(self, bg='')
        frm2 = tk.Frame(self, bg='black', height=2)
        lbl = tk.Label(
            frm1,
            text = 'Auswahl: ',
            font = ('', 18, 'bold')
        )
        lbl.pack(side=tk.LEFT)
        self.auswahl = ttk.Combobox(
            frm1,
            state = 'readonly',
            values = list(self.funktionen.keys())
        )
        self.auswahl.bind('<<ComboboxSelected>>', self.auswahl_select)
        self.auswahl.set(self.auswahl['values'][0])
        self.auswahl.pack(side=tk.LEFT, expand=True, fill='x')
        self.btn_run = ttk.Button(
            frm1, 
            name='btn_run', 
            text='R',
            command = self.btn_run_clicked
        )
        self.btn_run.pack(side=tk.LEFT)
        frm1.grid(column=0, row=0, sticky='ew')
        frm2.grid(column=0, row=1, sticky='ew')
        self.daten = tk.Text(self, name='daten')
        self.daten.grid(column=0, row=3, sticky='news')


    def auswahl_select(self, sender):
        auswahl = sender.widget.get()
        self.funktionen[auswahl].tkraise()
        if auswahl != 'Optionen':
            self.daten.tkraise()


    def btn_run_clicked(self):
        fall = self.auswahl.get()
        if fall == 'Daten Exportieren':
            l.export_to_eqdkp(
                self.daten,
                self.funktionen[fall]._link_addr.get(),
                self.funktionen['Optionen'].eqdkp_name.get(),
                self.funktionen['Optionen'].eqdkp_pass.get()
            )

        print(self.auswahl.get())
        print(self.funktionen['Optionen'].eqdkp_name.get())


    ##
    ##  Verbindung zur Logik
    ##
    def btn_hole_item_ID_clicked(self):
        background_methode = thread.Thread(target=l.hole_item_id, args=(self,))
        background_methode.start()


    def btn_export_to_eqdkp_clicked(self):
        bg_worker = thread.Thread(
            target=l.export_to_eqdkp, 
            args=(
                self.daten, 
                self.tb_link_raid.get(),
                self.tb_name_val.get(),
                self.tb_pass_val.get()
            )
        )
        bg_worker.start()


    def btn_load_loot_table_clicked(self):
        l.lade_daten_from_wowhead_by_npc(self.daten, self.tb_link_raid.get())


    def debug_daten(self, e:tk.EventType.ButtonPress, d:tk.Text):
        if len(self.tb_link_raid.get()) <= 0:
            self.tb_link_raid.set('https://canadian-crew.de/admin/manage_raids.php?s=&r=63&upd=true')
        d.insert('0.0', "[Teufelsherzhörner]\t16808\tVoltox\t25\n")
        d.insert('1.0', "[Zauberdolch]\t18878\tHilo\t50\n")
        d.insert('2.0', "[Helm des Cenarius]\t16834\tNador\t5\n")
        d.insert('3.0', "[Aurastein-Hammer]\t17105\tTreehugs\t75\n")