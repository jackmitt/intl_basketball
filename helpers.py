import pandas as pd
import numpy as np

class Database:
    def __init__(self, keys = []):
        self.df = pd.DataFrame()
        self.dict = {}
        for key in keys:
            self.dict[key] = []
        self.tempRow = []

    def getKeys(self):
        return (list(self.dict.keys()))

    def getCol(self, colName):
        return (self.dict[colName])

    def getLength(self):
        return (len(list(self.dict.keys())[0]))

    def getDict(self):
        return (self.dict)

    def getDataFrame(self):
        self.df = pd.DataFrame.from_dict(self.dict)
        return(self.df)

    def getCell(self, col, index):
        return (self.dict[col][index])

    def initDictFromCsv(self, path):
        self.dict = pd.read_csv(path, encoding = "ISO-8859-1").to_dict(orient="list")

    def addColumn(self, colName):
        self.dict[colName] = []

    def addCellToRow(self, datum):
        if (len(self.tempRow) + 1 > len(self.dict)):
            raise ValueError("The row is already full")
        else:
            self.tempRow.append(datum)

    def appendRow(self):
        if (len(self.tempRow) != len(self.dict)):
            raise ValueError("The row is not fully populated")
        else:
            for i in range(len(self.dict.keys())):
                self.dict[list(self.dict.keys())[i]].append(self.tempRow[i])
            self.tempRow = []

    def trashRow(self):
        self.tempRow = []

    def dictToCsv(self, pathName):
        self.df = pd.DataFrame.from_dict(self.dict)
        self.df = self.df.drop_duplicates()
        self.df.to_csv(pathName, index = False)

    def printRow(self):
        print(self.tempRow)

    def printDict(self):
        print(self.dict)

    def reset(self):
        self.tempRow = []
        self.dict = {}
        for key in list(self.dict.keys()):
            self.dict[key] = []

    def merge(self, B):
        for key in B.getKeys():
            if (key not in list(self.dict.keys())):
                self.dict[key] = B.getCol(key)

def standardizeTeamName(name, league = "Spain"):
    name = name.lower()
    if (league == "Spain"):
        if (name == "barcelona"):
            return ("FCB")
        elif (name == "baskonia"):
            return ("BASK")
        elif ("obradoiro" in name):
            return ("OBR")
        elif ("manresa" in name):
            return ("MAN")
        elif ("tenerife" in name):
            return ("TEN")
        elif ("real betis" in name):
            return ("BETIS")
        elif ("andorra" in name):
            return ("AND")
        elif ("unicaja" in name):
            return ("UNI")
        elif ("real madrid" in name):
            return ("RMB")
        elif ("gran canaria" in name):
            return ("GCN")
        elif (name == "gipuzkoa"):
            return ("GBC")
        elif ("estudiantes" in name):
            return ("EST")
        elif ("badalona" in name):
            return ("JOV")
        elif ("zaragoza" in name):
            return ("ZAR")
        elif ("valencia" in name):
            return ("VAL")
        elif ("murcia" in name):
            return ("MUR")
        elif ("fuenlabrada" in name):
            return ("MON")
        elif ("bilbao" in name):
            return ("BBB")
        elif ("san pablo" in name):
            return ("SPB")
        elif ("breogan" in name):
            return ("BRE")
        else:
            return ("ERROR: " + name)

def monthToInt(month):
    month = month.lower()
    if ('jan' in month):
        return (1)
    if ('feb' in month):
        return (2)
    if ('mar' in month):
        return (3)
    if ('apr' in month):
        return (4)
    if ('may' in month):
        return (5)
    if ('jun' in month):
        return (6)
    if ('jul' in month):
        return (7)
    if ('aug' in month):
        return (8)
    if ('sep' in month):
        return (9)
    if ('oct' in month):
        return (10)
    if ('nov' in month):
        return (11)
    if ('dec' in month):
        return (12)
    else:
        return (-1)
