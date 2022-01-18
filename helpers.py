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
        if ("barcelona" in name or name == "barca"):
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
        elif ("orleanaise" in name or name == "orleans loiret basket"):
            return ("ORL")
        elif ("strasbourg" in name):
            return ("STR")
        elif ("asvel" in name):
            return ("LYV")
        elif ("boulogne" in name):
            return ("BSM")
        elif ("dunkerque" in name or name == "bcm gravelines"):
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
        elif ("fos ouest" in name or name == "fos sur mer"):
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
        elif ("ea7-" in name or "armani exchange" in name):
            return ("MIL")
        elif ("virtus roma" in name):
            return ("ROM")
        elif ("pepsi caserta" in name):
            return ("JUV")
        elif ("air avellino" in name):
            return ("AVE")
        elif ("umana reyer venezia" in name or name == "umana venezia"):
            return ("VEN")
        elif ("upea c.d." in name):
            return ("ORL")
        elif ("carmatic pistoia" in name):
            return ("PIS")
        elif ("brindisi" in name):
            return ("NBB")
        elif ("scavolini spar pesaro" in name or name == "carpegna prosciutto basket pesaro"):
            return ("PES")
        elif ("pallacanestro trento" in name or name == "dolomiti energia trento"):
            return ("TREN")
        elif ("trenkwalder" in name or name == "grissin bon reggio emilia"):
            return ("REG")
        elif ("dinamo sassari" in name or name == "banco di sardegna sassari"):
            return ("SAS")
        elif ("la fortezza" in name or name == "virtus bologna"):
            return ("BOL")
        elif ("varese" in name):
            return ("VAR")
        elif ("bennet cantu" in name):
            return ("CAN")
        elif ("pms torino" in name):
            return ("TOR")
        elif ("brescia" in name):
            return ("BRE")
        elif ("treviso" in name):
            return ("TREV")
        elif ("biancoblu basket bologna" in name or name == "fortituto kontatto bologna"):
            return ("BOLO")
        elif ("pallacanestro trieste" in name):
            return ("TRIE")
        elif ("tortona" in name):
            return ("TORT")
        elif ("basket napoli" in name or name == "napoli basket" or "cuore napoli" in name):
            return ("NAP")
        else:
            return ("ERROR: " + name)

    if (league == "Euroleague"):
        if ("real madrid" in name):
            return ("RMB")
        elif ("zalgiris" in name):
            return ("ZAL")
        elif ("nizhny" in name):
            return ("NIZ")
        elif ("sassari" in name):
            return ("SAS")
        elif ("efes pilsen" in name):
            return ("EFE")
        elif ("kazan" in name):
            return ("UNICS")
        elif ("cedevita zagreb" in name):
            return ("CED")
        elif ("unicaja" in name):
            return ("UNI")
        elif ("limoges" in name):
            return ("CSP")
        elif ("cabi electra" in name):
            return ("MAC")
        elif ("alba berlin" in name):
            return ("BER")
        elif ("cska moscow" in name):
            return ("CSKA")
        elif ("barcelona" in name or name == "barca"):
            return ("FCB")
        elif ("bayern " in name):
            return ("BAY")
        elif ("ea7-" in name):
            return ("MIL")
        elif ("fenerbahce" in name):
            return ("FEN")
        elif ("panathinaikos" in name):
            return ("PAN")
        elif ("turow zgorzelec" in name):
            return ("TUR")
        elif ("baskonia" in name):
            return ("BASK")
        elif ("neptunas" in name):
            return ("NEP")
        elif ("crvena zvezda" in name):
            return ("ZVE")
        elif ("galatasaray" in name):
            return ("GAL")
        elif ("valencia" in name):
            return ("VAL")
        elif ("olympiacos" in name):
            return ("OLY")
        elif ("khimki" in name):
            return ("KHI")
        elif ("strasbourg" in name):
            return ("STR")
        elif ("pinar karsiyaka" in name):
            return ("PIN")
        elif ("lokomotiv" in name):
            return ("LOK")
        elif ("zastal" in name):
            return ("ZAS")
        elif ("daruss afaka" in name):
            return ("DBI")
        elif ("bamberg" in name):
            return ("BRO")
        elif ("buducnost" in name):
            return ("BUD")
        elif ("pinar karsiyaka" in name):
            return ("PIN")
        elif ("gran canaria" in name):
            return ("GCN")
        elif ("asvel " in name):
            return ("LYV")
        elif ("zenit " in name):
            return ("ZEN")
        else:
            return ("ERROR: " + name)

    if (league == "Turkey"):
        if ("galatasaray" in name):
            return ("GAL")
        elif ("usak sportlif" in name):
            return ("UUB")
        elif ("istanbul bb" in name):
            return ("IBB")
        elif ("ted ankara" in name):
            return ("TED")
        elif ("daruss afaka" in name):
            return ("DBI")
        elif ("besiktas" in name):
            return ("BES")
        elif ("trabzonspor" in name):
            return ("TRA")
        elif ("torku konyaspor" in name):
            return ("TOR")
        elif (name == "tofas"):
            return ("TOF")
        elif ("edirne" in name):
            return ("ESK")
        elif ("gaziantep" in name):
            return ("GAZ")
        elif ("efes pilsen" in name):
            return ("EFE")
        elif ("pinar karsiyaka" in name):
            return ("PIN")
        elif ("banvitspor" in name):
            return ("BVS")
        elif ("turk telekom" in name):
            return ("TUR")
        elif ("fenerbahce" in name):
            return ("FEN")
        elif ("buyukcekmece" in name):
            return ("DEM")
        elif ("yesilgiresun" in name):
            return ("YES")
        elif ("balikesir buyuksehir" in name):
            return ("BBB")
        elif ("eskisehir" in name):
            return ("ESK")
        elif ("sakarya " in name):
            return ("SAK")
        elif ("bahcesehir" in name):
            return ("BAHC")
        elif ("afyon belediye" in name):
            return ("AFYO")
        elif ("bursaspor" in name):
            return ("BURS")
        elif ("sigortam.net" in name):
            return ("ITU")
        elif ("genc ankara" in name):
            return ("OGK")
        elif ("fethiye belediye" in name):
            return ("LOKM")
        elif ("petkim spor" in name):
            return ("SOC")
        elif ("yalova bld" in name):
            return ("YAL")
        elif ("maik ze fendi" in name):
            return ("MERK")
        else:
            return ("ERROR: " + name)

    if (league == "VTB"):
        if ("nymburk" in name):
            return ("NYM")
        elif ("lokomotiv" in name):
            return ("LOK")
        elif ("khimki" in name):
            return ("KHI")
        elif ("avtodor" in name):
            return ("AVT")
        elif ("zenit " in name):
            return ("ZEN")
        elif ("cska " in name):
            return ("CSKA")
        elif ("nilan " in name):
            return ("NIL")
        elif ("krylya" in name):
            return ("KRY")
        elif ("nizhny" in name):
            return ("NIZ")
        elif ("volgograd" in name):
            return ("OKT")
        elif ("kazan" in name):
            return ("UNICS")
        elif ("kalev cramo" in name):
            return ("KCT")
        elif ("riga " in name):
            return ("RIG")
        elif ("enisey" in name):
            return ("ENI")
        elif ("minsk" in name):
            return ("MIN")
        elif (" astana" in name):
            return ("AST")
        elif ("tbilisi" in name):
            return ("VITA")
        elif ("zastal" in name):
            return ("ZAS")
        elif ("parma perm" in name):
            return ("PARM")
        else:
            return ("ERROR: " + name)

    if (league == "Adriatic"):
        if ("zvezda" in name):
            return ("ZVE")
        elif ("levski" in name):
            return ("LEV")
        elif ("cibona zagreb" in name):
            return ("CIB")
        elif ("cedevita olimpija" in name):
            return ("OLI")
        elif (" krka" in name):
            return ("KRK")
        elif ("cedevita zagreb" in name):
            return ("CED")
        elif ("szolnoki" in name):
            return ("SZO")
        elif ("partizan" in name):
            return ("PAR")
        elif ("mega vizura" in name):
            return ("MEG")
        elif (" skopje" in name):
            return ("MZT")
        elif ("buducnost" in name):
            return ("BUD")
        elif ("metalac" in name):
            return ("MET")
        elif ("zadar" in name):
            return ("ZAD")
        elif ("igokea" in name):
            return ("IGO")
        elif ("alpos sentjur" in name):
            return ("SEN")
        elif ("mega leks" in name):
            return ("MEGAL")
        elif ("sutjeska" in name):
            return ("SUT")
        elif ("mornar " in name):
            return ("MOR")
        elif ("beograd" in name):
            return ("FMP")
        elif ("karpos" == name):
            return ("KAR")
        elif ("co split" == name):
            return ("SPL")
        elif ("borac" == name):
            return ("BOR")
        elif ("studentski" in name):
            return ("STU")
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
