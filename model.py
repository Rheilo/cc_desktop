class Datensatz():
    def __init__(self, item:str, id:int, spieler:str, wert:int):
        self.__item = item
        self.__id = id
        self.__spieler = spieler
        self.__wert = wert

    @property
    def item(self):
        return self.__item

    
    @property
    def id(self):
        return self.__id


    @property
    def spieler(self):
        return self.__spieler
    @spieler.setter
    def spieler(self, spieler):
        self.__spieler = spieler

    
    @property
    def wert(self):
        return self.__wert
    @wert.setter
    def wert(self, wert):
        if wert <= 0: self.__wert = 0
        else: self.__wert = wert