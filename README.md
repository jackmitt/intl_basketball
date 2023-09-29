## Workflow

### Data Extraction
* Data is collected at the team and player level
* More emphasis is put on advanced metrics such possession-adjusted points, true shooting %, offensive rebound %, etc, but typical basketball metrics must be gathered first
* For every season, stats from every players' former seasons are scraped and stored to better estimate their performance in the new season
* Betting markets are scraped for model evaluation later

[scrapers.py](https://github.com/jackmitt/intl_basketball/blob/main/code/scrapers.py) --> contains functions for scraping data publicly available web data using Selenium + BeautifulSoup

### Data Cleaning / Feature Engineering
* Team-level features are the averages of advanced metrics recorded in previous games in the season
* Player-level features, all of which are percentages, are based on the Bayesian posterior of their respective Beta distributions where the 'weight' of the prior distribution is set according to domain knowledge (Beta dist mean calculated in [helpers.py](https://github.com/jackmitt/intl_basketball/blob/main/code/helpers.py))
* The posterior means are combined based on general role (perimeter/inside player) and then weighted within their team according to expected playing time

[data_manipulation.py](https://github.com/jackmitt/intl_basketball/blob/master/code/data_manipulation.py) --> in addition to the above, typical cleaning and feature engineering makes up the functions in here

### Modeling
* OLS Linear Regression is used with responses being the difference in the two teams scores and the sum of the scores
* Train (70%) and test (30%) set
* There is a separate player-based model and team-based model (4 in total: player --> difference, player --> sum, team --> difference, team --> sum)

[predictions.py](https://github.com/jackmitt/intl_basketball/blob/main/code/predictions.py) --> aggregateModelPredictions()

### Evaluation of Models
* Traditional determinations of model fit are not greatly meaningful; instead, we are most concerned with the performance of our bets against the market
* There are two primary markets for each game: the Asian handicap market, which considers the difference of scores between the two teams, and the totals market, which considers the sum of scores
* Various strategies for betting are explored
* The best strategy: if both the player and the team model are in agreement that the market line is off, then a flat bet is made

[evaluations.py](https://github.com/jackmitt/intl_basketball/blob/main/code/prediction_evaluation.py) --> all different potential strategies are explored here through evaluating predictions made on the test set
