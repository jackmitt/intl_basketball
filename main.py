from scrapers import oddsportal
from scrapers import realgm
from scrapers import nowgoal
import data_manipulation as dm
import prediction_evaluation as pe

# dm.preMatchAverages()
# dm.train_test_split()
# dm.predictions()
# pe.simulateKellyBets(20000, kellyDiv = 1, preCovid = False)
#realgm("https://basketball.realgm.com/international/league/1/Euroleague/scores/", 2014, 10, 15)
# realgm("https://basketball.realgm.com/international/league/12/French-Jeep-Elite/scores/", 2014, 9, 26)
#realgm("https://basketball.realgm.com/international/league/6/Italian-Lega-Basket-Serie-A/scores/", 2014, 10, 11)
#realgm("https://basketball.realgm.com/international/league/8/Greek-HEBA-A1/scores/", 2014, 10, 12)
#realgm("https://basketball.realgm.com/international/league/5/Australian-NBL/scores/", 2014, 10, 10)
#realgm("https://basketball.realgm.com/international/league/15/German-BBL/scores/", 2014, 10, 2)
nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/20", 10, "Spain")
nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/19", 9, "France")
nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/16", 10, "Italy")
nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/17", 10, "Greece")
nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/14", 10, "Australia")
nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/22", 10, "German")
