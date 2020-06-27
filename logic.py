from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote import webdriver as WebDriver
import re
import tkinter as tk
from time import sleep
from model import *


CHROME_DRIVER_PATH = 'C:\\NextCloud\\python\\selenium\\chromedriver_win32_v83.exe'


def __extrahiere_itemid(url:str) -> int:
    pattern = r'[item=]{5}[\d]*'
    match = re.findall(pattern, url)
    item_id = str(match[0]).split('=')[1][:]
    return int(item_id)


def __hole_item_id(item_name:str, driver:WebDriver.WebDriver) -> int:
# def _hole_item_id(item_name:str, driver:webdriver.Chrome):
    driver.get('https://classic.wowhead.com/items/name:' + item_name)
    # driver.get('https://de.classic.wowhead.com/items/name:' + item_name)
    e: WebDriver.WebElement = driver.find_element_by_css_selector('table.listview-mode-default tr td div a')
    item_link = e.get_attribute('href')
    return __extrahiere_itemid(item_link)


def daten_len(daten:tk.Text) -> int:
    return int(daten.index('end-1c').split('.')[0])


def __insert_daten(item_id:str, e:tk.Tk, line_index:str):
        line:str = e.daten.get(line_index + '.0', line_index + '.end')
        csv = line.split('\t')
        csv[1] = str(item_id)
        output = ''
        for i in csv:
            output += i + '\t'
        e.daten.insert(line_index + '.0', output)
        e.daten.delete(line_index + '.'+str(len(output)-1), line_index + '.end')


def hole_item_id(e):
    driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    for i in range(1, daten_len(e.daten)+1, 1):
        #
        # Überspringe die unvaliden Zeilen
        pattern = r'[a-zA-Z\[\] \S]+[\t]{2}[\S]+[\t][\d]+'
        line:str = e.daten.get(str(i)+'.0', str(i)+'.end')
        match = re.findall(pattern, line)
        if len(match) <= 0: continue
        #
        # Zeile ist valide und kann bearbeitet werden
        item = ''
        if line.find(']') >= 0: item = line[:line.find(']')+1]
        else: item = line[:line.find('\t')]
        item_id = __hole_item_id(item, driver)
        __insert_daten(item_id, e, str(i))
    driver.quit()


def __login(browser, usr:str, pw:str) -> None:
    usr_feld = browser.find_element_by_xpath("//input[@id='username']")
    usr_feld.send_keys(usr)
    pw_feld = browser.find_element_by_xpath("//input[@id='password']")
    pw_feld.send_keys(pw)
    browser.find_element_by_xpath("//button[@type='submit']").click()


def export_to_eqdkp(d:tk.Text, link:str, usr:str, pw:str):
    browser = webdriver.Chrome(CHROME_DRIVER_PATH)
    browser.get(link)
    if 'Zugriff verweigert' in browser.page_source:
        __login(browser, usr, pw)

        btn_add_item:WebElement = browser.find_element_by_xpath("//button[@id='add-item-btn']")
        zähler = 0
        pattern = r'[a-zA-Z\' \[\]\w]+[\t]{1}[0-9]+[\t]{1}[a-zA-Z_\w]+[\t]{1}[0-9]+'
        zeilen:str = d.get('0.0', 'end-1c')
        match = re.findall(pattern, zeilen)
        for d in match:
            dd = d.split('\t')
            ds = Datensatz(dd[0][1:-1], int(dd[1]), dd[2], int(dd[3]))
            zähler += 1
            # Ist das gleiche wie btn_add_item.click() wird jetzt aber über JavaScript
            # ausgeführt und somit muss das element nicht im Sichtfeld / Anzeigebereich
            # liegen um ausgeführt zu werden
            browser.execute_script("arguments[0].click();", btn_add_item)
            #btn_add_item.click()
            sleep(0.25)
            seiten_elemente:WebElement = browser.find_elements_by_xpath(
                "//input[@id='items_"+str(zähler)+"']/../..//input")
            if(len(seiten_elemente) > 0):
                browser.find_element_by_xpath("//input[@id='items_"+str(zähler)+"']/../..//button").click()
                seiten_elemente[1].send_keys(ds.item)
                seiten_elemente[2].send_keys(ds.id)
                seiten_elemente[3].send_keys(ds.wert)
                tmp = browser.find_elements_by_xpath("//div[@class='ui-multiselect-filter']/../../div/div/input")
                tmp[zähler+2].send_keys(ds.spieler)
                sleep(0.25)
                browser.find_elements_by_xpath("//div[@class='ui-multiselect-filter']/../..//li/a[@class='ui-multiselect-all']")[zähler+2].click()
                browser.find_element_by_xpath("//input[@id='items_"+str(zähler)+"']/../..//button").click()
            
    else:
        pass


def lade_daten_from_wowhead_by_npc(d:tk.Text, link:str):
    browser = webdriver.Chrome(CHROME_DRIVER_PATH)
    browser.get(link)
    loot_table = browser.find_elements_by_xpath(
        "//table[@class='listview-mode-default']//a[@class='q4 listview-cleartext']")
    boss_name:str = browser.find_element_by_xpath("//h1[@class='heading-size-1']").text
    zeile:int = 1
    d.insert(str(zeile) + '.0', boss_name + '\n')
    zeile += 1
    for loot in loot_table:
        id = __extrahiere_itemid(loot.get_attribute('href'))
        d.insert(str(zeile) + '.0', '['+loot.text+']' + '\t' + str(id) + '\n')
        zeile + 1
    browser.quit()
