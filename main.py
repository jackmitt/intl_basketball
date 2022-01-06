from scrapers import oddsportal
from scrapers import realgm
import data_manipulation as dm
import prediction_evaluation as pe

#dm.predictions()
#pe.simulateKellyBets(20000, kellyDiv = 10)
realgm("https://basketball.realgm.com/international/league/1/Euroleague/scores/", 2014, 10, 15)
realgm("https://basketball.realgm.com/international/league/12/French-Jeep-Elite/scores/", 2014, 9, 26)
realgm("https://basketball.realgm.com/international/league/6/Italian-Lega-Basket-Serie-A/scores/", 2014, 10, 11)
realgm("https://basketball.realgm.com/international/league/8/Greek-HEBA-A1/scores/", 2014, 10, 12)
realgm("https://basketball.realgm.com/international/league/5/Australian-NBL/scores/", 2014, 10, 10)
realgm("https://basketball.realgm.com/international/league/15/German-BBL/scores/", 2014, 10, 2)
