from selenium import webdriver

import re

driver = webdriver.Chrome('C:\\NextCloud\\python\\selenium\\chromedriver_win32_v80.exe')
# driver.get('https://de.classic.wowhead.com/search?q=[Stulpen der Macht]')
# id_str = driver.current_url
# pattern = r'/item=\d*/'
# match = re.findall(pattern, id_str)
# item_id = str(match[0]).split('=')[1][:-1]

driver.get('https://de.classic.wowhead.com/items/name:[Stiefel des Arkanisten]')
e = driver.find_element_by_css_selector('table.listview-mode-default tr td div a')
item_link = e.get_attribute('href')
pattern = r'/item=\d*/'
match = re.findall(pattern, item_link)
item_id = str(match[0]).split('=')[1][:-1]
driver.close()
print(item_id)