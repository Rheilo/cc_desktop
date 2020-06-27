import tkinter as tk
from tkinter.font import Font
import tkinter.ttk as ttk
import logic as l
import threading as thread
##
## Die einzelnen GUI's für die Funktionen
from gui_auswahl.daten_exportieren import DatenExportieren
from gui_auswahl.optionen import Optionen
from gui_auswahl.erstelle_raid import ErstelleRaid
from gui_auswahl.bonus_dkp import BonusDKP


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Canadian Crew <Patchwerk - EU>')
        self.funktionen = {
            'Raid Anlegen': ErstelleRaid(self),
            'Daten Exportieren': DatenExportieren(self),
            'Bounus DKP': BonusDKP(self),
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
        auswahl = self.auswahl.get()
        self.funktionen[auswahl].tkraise()
        if auswahl != 'Optionen':
            self.daten.tkraise()
        ## DEBUG: Insert daten zum Testen
        if auswahl == 'Raid Anlegen':
            debug_daten = '''1 DKP für World-Buffs / Flask: 
======================== 
Merlana 

6 DKP für World-Buffs / Flask: 
======================== 
Esperanca 
Mi
'''
            i:int = 0
            for z in debug_daten.split(r'\n'):
                self.daten.insert(str(i)+'.0', z)
                i = i+1


    ##
    ##  Verbindung zur Logik
    ##
    def btn_run_clicked(self):
        fall = self.auswahl.get()
        if fall == 'Daten Exportieren':
            bg_worker = thread.Thread(
                target=l.export_to_eqdkp, 
                args=(
                    self.daten,
                    self.funktionen[fall]._link_addr.get(),
                    self.funktionen['Optionen'].eqdkp_name.get(),
                    self.funktionen['Optionen'].eqdkp_pass.get()
                )
            )
            bg_worker.start()
        elif fall == 'Raid Anlegen':
            bg_worker = thread.Thread(
                target=l.raid_anlegen, 
                args=(
                    'https://www.canadian-crew.de/admin/manage_raids.php?s=',
                    self.funktionen['Optionen'].eqdkp_name.get(),
                    self.funktionen['Optionen'].eqdkp_pass.get(),
                    self.daten,
                    True if self.funktionen[fall].auswahl.get() == 1 else False
                )
            )
            bg_worker.start()
        elif fall == 'Bounus DKP':
            bg_worker = thread.Thread(
                target=l.export_to_eqdkp_world_buffs,
                args=(
                    self.funktionen[fall]._link_addr.get(),
                    self.funktionen['Optionen'].eqdkp_name.get(),
                    self.funktionen['Optionen'].eqdkp_pass.get(),
                    self.daten
                )
            )
            bg_worker.start()

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