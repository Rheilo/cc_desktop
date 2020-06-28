from threading import Thread, Condition, Lock
from typing import Callable, List, Any, Dict, Tuple
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
import logic


SONDERFÄLLE = {
    'Mi' : 'Mi_'
}


class LeseBonusDKP(Thread):
    def __init__(self, daten:str, mit_punkte:bool=False):
        Thread.__init__(self)
        self.d = daten
        self.mit_punkte = mit_punkte
        self._return = []


    def run(self):
        zeilen:str = self.d.splitlines()
        punkte:str = None
        for zeile in zeilen:
            zeile = zeile.strip()
            if self.mit_punkte:
                if zeile[0:1] == '1' or zeile[0:1] == '2' or \
                zeile[0:1] == '3' or zeile[0:1] == '4' or \
                zeile[0:1] == '5' or zeile[0:1] == '6':
                    punkte = zeile[0:1]
            if zeile[0:1] == '=' or zeile[0:1] == '1' or \
            zeile[0:1] == '2' or zeile[0:1] == '3' or \
            zeile[0:1] == '4' or zeile[0:1] == '5' or\
            zeile[0:1] == '6' or zeile == '0' or zeile == '':
                continue
            if zeile in SONDERFÄLLE:
                zeile = SONDERFÄLLE[zeile]
            self._return.append(
                (punkte, zeile) if self.mit_punkte else zeile
            )


    def join(self):
        Thread.join(self)
        return self._return


class SchreibeBonusDKP(Thread):
    def __init__(self, usr:str, pas:str, url:str, shared_data, punkte:List[Tuple[str, str]], lock:Lock=Lock):
        Thread.__init__(self)
        self.usr = usr
        self.pas = pas
        self.url = url
        self.browser = Chrome(logic.CHROME_DRIVER_PATH)
        self._shared_data = shared_data
        self.punkte = punkte
        self.lock = lock

    
    def run(self):
        self.browser.get(self.url)
        if 'Zugriff verweigert' in self.browser.page_source:
            usr_feld = self.browser.find_element_by_xpath("//input[@id='username']")
            usr_feld.send_keys(self.usr)
            pw_feld = self.browser.find_element_by_xpath("//input[@id='password']")
            pw_feld.send_keys(self.pas)
            self.browser.find_element_by_xpath("//button[@type='submit']").click()
        btn_add_adjs = self.browser.find_element_by_xpath("//button[@id='add-adjustment-btn']")
        tmp = self.browser.find_elements_by_xpath("//div[@class='ui-multiselect-menu ui-widget ui-widget-content ui-corner-all']/div[@class='ui-widget-header ui-corner-all ui-multiselect-header ui-helper-clearfix ui-multiselect-hasfilter']/div[@class='ui-multiselect-filter']/input")
        i = len(tmp)
        p_aktuell = 0
        p_count = 0
        for p,n in self.punkte:
            if p == 0:
                continue
            if int(p) > p_aktuell:
                self.browser.execute_script("arguments[0].click();", btn_add_adjs)
                i = i + 1
                p_aktuell = int(p)
                p_count = p_count + 1
                self.browser.find_element_by_xpath(
                    f"//input[@name='adjs[{p_count}][reason]']"
                ).send_keys('World Buffs ' + p)
                self.browser.find_element_by_xpath(
                    f"//input[@name='adjs[{p_count}][value]']"
                ).send_keys(p)
                self.browser.find_element_by_xpath(
                    f"//select[@name='adjs[{p_count}][event]']//option[@value='11']"
                ).click()
                if p_count > 1:
                    self.browser.find_element_by_xpath(
                        f"//button[@id='adjs_{p_count-1}_members_ms']"
                    ).click()
                self.browser.find_element_by_xpath(
                    f"//button[@id='adjs_{p_count}_members_ms']"
                ).click()
            suchfeld = self.browser.find_element_by_xpath(
                f"//div[@class='ui-multiselect-menu ui-widget ui-widget-content ui-corner-all'][{i}]/div[@class='ui-widget-header ui-corner-all ui-multiselect-header ui-helper-clearfix ui-multiselect-hasfilter']/div[@class='ui-multiselect-filter']/input"
            )
            suchfeld.send_keys(n)
            sleep(0.25)
            while True:
                if self._shared_data.play:
                    break
                else:
                    if self._shared_data.weiter:
                        self.lock.acquire()
                        self._shared_data.weiter = False
                        self.lock.release()
                        break
                sleep(0.25)
                print('weiter:'+str(self._shared_data.weiter))
            self.browser.find_element_by_xpath(
                f"//div[@class='ui-multiselect-menu ui-widget ui-widget-content ui-corner-all'][{i}]/div[@class='ui-widget-header ui-corner-all ui-multiselect-header ui-helper-clearfix ui-multiselect-hasfilter']/ul[@class='ui-helper-reset']/li[1]/a[@class='ui-multiselect-all']/span[2]"
            ).click()
            suchfeld.clear()