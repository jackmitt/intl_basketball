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

def standardizeTeamName(name, league):
    name = name.lower()
    if (league == "Spain"):
        if ("barcelona" in name):
            return ("FCB")
        elif ("baskonia" in name):
            return ("BASK")
        elif ("obradoiro" in name):
            return ("OBR")
        elif ("manresa" in name):
            return ("MAN")
        elif ("tenerife" in name):
            return ("TEN")
        elif ("real betis" in name or name =="cajasol sevilla"):
            return ("BETIS")
        elif ("andorra" in name):
            return ("AND")
        elif ("unicaja" in name):
            return ("UNI")
        elif ("real madrid" in name):
            return ("RMB")
        elif ("gran canaria" in name):
            return ("GCN")
        elif ("gipuzkoa" in name):
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

    if (league == "France"):
        if ("pau-orthez" in name):
            return ("PAU")
        elif ("orleanaise" in name):
            return ("ORL")
        elif ("strasbourg" in name):
            return ("STR")
        elif ("lyon asvel" in name):
            return ("LYV")
        elif ("boulogne" in name):
            return ("BSM")
        elif ("dunkerque" in name):
            return ("GRV")
        elif ("limoges" in name):
            return ("CSP")
        elif ("nancy" in name):
            return ("NAN")
        elif ("cholet" in name):
            return ("CHO")
        elif ("dijon" in name):
            return ("DIJ")
        elif ("le mans" in name):
            return ("LEM")
        elif ("rouen" in name):
            return ("ROU")
        elif ("chalons-reims" in name):
            return ("RCB")
        elif ("paris" in name):
            return ("PLV")
        elif ("nanterre" in name):
            return ("N92")
        elif ("elan chalon-saone" in name):
            return ("CHA")
        elif ("bourg-en-bresse" in name):
            return ("JLB")
        elif ("le havre" in name):
            return ("SLH")
        elif ("antibes" in name):
            return ("ANT")
        elif ("monaco" in name):
            return ("ASM")
        elif ("le portel" in name):
            return ("PORT")
        elif ("hyeres toulon" in name):
            return ("HYT")
        elif ("boulazac" in name):
            return ("BBD")
        elif ("fos ouest" in name):
            return ("FOS")
        elif ("chorale roanne" in name):
            return ("ROA")
        else:
            return ("ERROR: " + name)

    if (league == "Australia"):
        if ("illawarra hawks" in name):
            return ("ILL")
        elif ("townsville crocodiles" in name):
            return ("TOW")
        elif ("adelaide 36ers" in name):
            return ("ADE")
        elif ("cairns taipans" in name):
            return ("CRN")
        elif ("perth wildcats" in name):
            return ("PER")
        elif ("new zealand breakers" in name):
            return ("NZB")
        elif ("sydney kings" in name):
            return ("SYD")
        elif ("melbourne united" in name):
            return ("MEL")
        elif ("brisbane bullets" in name):
            return ("BRI")
        elif ("south east melbourne" in name):
            return ("SEM")
        elif ("tasmania" in name):
            return ("JACK")
        else:
            return ("ERROR: " + name)

    if (league == "Germany"):
        if ("alba berlin" in name):
            return ("BER")
        elif ("bg goettingen" in name):
            return ("GOE")
        elif ("bayreuth" in name):
            return ("BAYR")
        elif ("crailsheim" in name):
            return ("CRA")
        elif ("artland" in name):
            return ("ART")
        elif ("tubingen" in name):
            return ("TUB")
        elif ("ludwigsburg" in name or "riesen" in name):
            return ("LUD")
        elif ("telekom baskets bonn" in name):
            return ("TBB")
        elif ("bayern" in name):
            return ("BAY")
        elif ("mitteldeutscher bc" in name):
            return ("BC")
        elif ("bamberg" in name):
            return ("BRO")
        elif ("eisbaren bremerhaven" in name):
            return ("EIS")
        elif ("fraport skyliners" in name):
            return ("FRA")
        elif ("phoenix hagen" in name):
            return ("HAG")
        elif ("tbb trier" in name):
            return ("TRI")
        elif ("new yorker phantoms" in name or "braunschweig" in name):
            return ("BLB")
        elif ("ratiopharm ulm" in name):
            return ("RUL")
        elif ("ewe baskets oldenburg" in name):
            return ("EWE")
        elif ("46ers" in name):
            return ("GIE")
        elif ("s.oliver" in name):
            return ("OLI")
        elif ("rasta vechta" in name):
            return ("RAS")
        elif (name == "jena"):
            return ("SCJ")
        elif (name == "gotha"):
            return ("BIG")
        elif (name == "hamburg" or name == "hamburg towers"):
            return ("HAM")
        elif ("chemcats" in name or "chemnitz" in name):
            return ("BVC")
        elif ("heidelberg" in name):
            return ("MLP")
        else:
            return ("ERROR: " + name)

    if (league == "Greece"):
        if ("sharon leki" in name):
            return ("PAOK")
        elif ("rethymno aegean" in name):
            return ("RETH")
        elif ("panelefsiniakos" in name):
            return ("PANEL")
        elif ("aris tt bank" in name):
            return ("ARIS")
        elif ("panionios" in name):
            return ("PAI")
        elif ("kolossos" in name):
            return ("KOL")
        elif ("olympiacos" in name):
            return ("OLY")
        elif ("apollon" in name):
            return ("APO")
        elif ("as koroivos amaliadas" in name):
            return ("AMA")
        elif ("aek athens" in name):
            return ("ATH")
        elif ("kao dramas" in name):
            return ("KAOD")
        elif ("trikala 2000" in name):
            return ("ARI")
        elif ("panathinaikos" in name):
            return ("PAN")
        elif ("ae nea kifisia" in name):
            return ("AENK")
        elif ("kavala" in name):
            return ("KAV")
        elif ("gs lavrio" in name):
            return ("LAV")
        elif ("sefa arkadikos" in name):
            return ("ARK")
        elif ("ae doxa lefkadas" in name):
            return ("DOX")
        elif ("prometheus" in name):
            return ("PROM")
        elif (name == "kymis"):
            return ("KYM")
        elif ("larry shas" in name):
            return ("LAR")
        elif ("dash peristeri" in name):
            return ("PER")
        elif ("hongragos" in name):
            return ("HOL")
        elif ("ionikos nikaias" in name):
            return ("IONI")
        elif ("larisa b.c." in name):
            return ("ERMI")
        elif ("iraklis" in name):
            return ("IRAK")
        elif ("gs harilaos trikoupis" in name):
            return ("CTM")
        else:
            return ("ERROR: " + name)

    if (league == "Italy"):
        if ("vanoli cremona" in name):
            return ("CRE")
        elif ("ea7-" in name):
            return ("MIL")
        elif ("virtus roma" in name):
            return ("ROM")
        elif ("pepsi caserta" in name):
            return ("JUV")
        elif ("air avellino" in name):
            return ("AVE")
        elif ("umana reyer venezia" in name):
            return ("VEN")
        elif ("upea c.d." in name):
            return ("ORL")
        elif ("carmatic pistoia" in name):
            return ("PIS")
        elif ("enel brindisi" in name):
            return ("NBB")
        elif ("scavolini spar pesaro" in name):
            return ("PES")
        elif ("pallacanestro trento" in name):
            return ("TREN")
        elif ("trenkwalder" in name):
            return ("REG")
        elif ("dinamo sassari" in name):
            return ("SAS")
        elif ("la fortezza" in name):
            return ("BOL")
        elif ("whirlpool varese" in name):
            return ("VAR")
        elif ("bennet cantu" in name):
            return ("CAN")
        elif ("pms torino" in name):
            return ("TOR")
        elif ("centrale del latte brescia" in name):
            return ("BRE")
        elif ("benetton treviso" in name):
            return ("TREV")
        elif ("biancoblu basket bologna" in name):
            return ("BOLO")
        elif ("pallacanestro trieste" in name):
            return ("TRIE")
        elif (name == "tortona"):
            return ("TORT")
        elif ("basket napoli" in name):
            return ("NAP")
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
