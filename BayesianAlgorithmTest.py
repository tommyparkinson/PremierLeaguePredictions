#Author Tom Parkinson
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from JointMethods import printPoints
from JointMethods import addPoints
from JointMethods import profit
from JointMethods import printProfit
from sklearn.model_selection import train_test_split
#from printing import printTest
import csv

print("BAYESIAN ALGORITHM:")
print("Predictions on a weekly basis, starting from week 19, throughout the season.")
print()
#data source for 2015/16 season
bayesData = pd.read_csv('actualTestingBayes.csv')
#X is an array of the matches. y is an array of the results in the matches.
X = bayesData.drop(['FTR'], 1)
y=bayesData['FTR']
bayesPredictedResults = []


#init amount of points for each team
points = 0

#init amount amount of wins for each match outcome.
nHW=0
nD=0
nAW=0

#Amount of games in training and testing set
trainingGames=900
testingGames=100

#spliting the data into training and testing sets.
#x is the training data which is all the data up to the defined amount of trainingGames
xTrainingSet=np.array(X[:trainingGames])
yTrainingSet=np.array(y[:trainingGames])

#y testing data which is all the data after the defined amount of trainingGames
xTestingSet=np.array(X[trainingGames:])
yTestingSet=np.array(y[trainingGames:])
actualResults= np.array(yTestingSet)

print("testing:",len(yTestingSet))
print("training:",len(yTrainingSet))

#Learning how many home wins, draws and away wins are in the training set.
for x in range(0,trainingGames):
    if(yTrainingSet[x]=="H"):
        nHW+=1 
    elif(yTrainingSet[x]=="D"):
        nD+=1
    elif(yTrainingSet[x]=="A"):
        nAW+=1
#Classifier
def bayes(homeTeamWins, homeTeamDraws, homeTeamLoss, homeTeamPlayed, awayTeamWin,awayTeamDraws,awayTeamLoss,awayTeamPlayed):
    global nHW
    global nD
    global nAW
    #probabilities of each matches outcome given the data in the training set
    probHomeWin = nHW/trainingGames
    probDraw = nD/trainingGames
    probAwayWin = nAW/trainingGames


    #Calculating the probability that a given team wins at home and the away team loses away given their history in the training set.
    try:
        probHomeTeamWinAtHome = homeTeamWins/homeTeamPlayed
    except ZeroDivisionError:
        probHomeTeamWinAtHome = 0
    try:
        probAwayTeamLoseAway = awayTeamLoss/awayTeamPlayed
    except ZeroDivisionError:
        probAwayTeamLoseAway = 0
        
    jointHomeProb = probHomeTeamWinAtHome*probAwayTeamLoseAway

    #Calculating the probability that a given team draws at home and away team also draws away given their history in the training set.
    try:    
        probHomeTeamDrawAtHome = homeTeamDraws/homeTeamPlayed
    except ZeroDivisionError:
        probHomeTeamDrawAtHome = 0
    try:
        probAwayTeamDrawAway = awayTeamDraws/awayTeamPlayed
    except ZeroDivisionError:
        probAwayTeamDrawAway = 0
        
    jointDrawProb = probHomeTeamDrawAtHome*probAwayTeamDrawAway
    
    #Calculating the probability that a given team loses at home and away team wins away given their history in the training set.
    try:
        probHomeTeamLoseAtHome = homeTeamLoss/homeTeamPlayed
    except ZeroDivisionError:
        probHomeTeamLoseAtHome = 0
    try:
        probAwayTeamWinAway = awayTeamWins/awayTeamPlayed
    except ZeroDivisionError:
        probAwayTeamWinAway = 0

    jointAwayProb = probHomeTeamLoseAtHome*probAwayTeamWinAway

    #The above probabilities wont add up to 1. For example, when calculating the probability of a home win above
    #it is only calculating that probability that the home team win and the away team lose. The match could also be a draw
    #or the home team lose and away team win. The next part of this method combines all the probabilities so that
    #the probability of a home win is calculated given that it isnt a draw or away win. All probabilites will add up to 1.
    try:
        probHW = (probHomeWin*jointHomeProb)/((probHomeWin*jointHomeProb)+(probDraw*jointDrawProb)+(probAwayWin*jointAwayProb))
    except ZeroDivisionError:
        probHW = 0
    try:
        probD = (probDraw*jointDrawProb)/((probHomeWin*jointHomeProb)+(probDraw*jointDrawProb)+(probAwayWin*jointAwayProb))
    except ZeroDivisionError:
        probD = 0
    try:
        probAW = (probAwayWin*jointAwayProb)/((probHomeWin*jointHomeProb)+(probDraw*jointDrawProb)+(probAwayWin*jointAwayProb))
    except ZeroDivisionError:
        probAW = 0

    #Checking which probability is highest to make a classification
    if(probHW>probD) and (probHW>probAW):
        classification = "H"
    elif(probD>probHW) and (probD>probAW):
        classification = "D"
    else:
        classification = "A"

      ##print(probHW)
      ##print(probD)
      ##print(probAW)

    return classification

#Method to learn how many home wins, draws and away wins a given home team has
def learnHomeData(teamName):
    homeWins=0
    homeDraws=0
    homeLoss=0
    homePlayed=0
    homeResults=[]
    
    for x in range(0, trainingGames):
        if(xTrainingSet[x][0]==teamName):
            if(yTrainingSet[x]=="H"):
               homeWins+=1
               homePlayed+=1
            elif(yTrainingSet[x]=="D"):
                 homeDraws+=1
                 homePlayed+=1
            elif(yTrainingSet[x]=="A"):
                 homeLoss+=1
                 homePlayed+=1
    homeResults.append(homeWins)
    homeResults.append(homeDraws)
    homeResults.append(homeLoss)
    homeResults.append(homePlayed)

    return homeResults

#Method to learn how many home wins, draws and away wins a given away team has
def learnAwayData(teamName):
    awayWins=0
    awayDraws=0
    awayLoss=0
    awayPlayed=0
    awayResults=[]
    for x in range(0, trainingGames):
        if(xTrainingSet[x][1]==teamName):
            if(yTrainingSet[x]=="H"):
               awayWins+=1
               awayPlayed+=1
            elif(yTrainingSet[x]=="D"):
                 awayDraws+=1
                 awayPlayed+=1
            elif(yTrainingSet[x]=="A"):
                 awayLoss+=1
                 awayPlayed+=1

    awayResults.append(awayWins)
    awayResults.append(awayDraws)
    awayResults.append(awayLoss)
    awayResults.append(awayPlayed)

    return awayResults

#This loops through all of the testing games (games that you want to predict)
#It learns the data for the home and away teams
#It then makes a classification on the data
#It then calculates profit and adds to a teams points projection.
for x in range(0,testingGames):
    i = x+1
    bayesMatch = np.array(xTestingSet[x:i])
    homeTeam = bayesMatch[0][0]
    awayTeam = bayesMatch[0][1]

    homeStats = learnHomeData(homeTeam)
    awayStats = learnAwayData(awayTeam)
    ##print(homeStats)
    ##print(awayStats)

    homeTeamWins=homeStats[0]
    homeTeamDraws=homeStats[1]
    homeTeamLoss=homeStats[2]
    homeTeamPlayed=homeStats[3]

    awayTeamWins=awayStats[2]
    awayTeamDraws=awayStats[1]
    awayTeamLoss=awayStats[0]
    awayTeamPlayed=awayStats[3]
    classification = bayes(homeTeamWins, homeTeamDraws, homeTeamLoss, homeTeamPlayed, awayTeamWins,awayTeamDraws,awayTeamLoss,awayTeamPlayed)
    ftr = yTestingSet[x]
    bayesPredictedResults.append(classification)
    
    if(classification=="H"):
        points = 3
        addPoints(homeTeam,3)
        #print(homeTeam, "v" ,awayTeam, "H")
    elif(classification=="D"):
        points = 1
        addPoints(homeTeam, points)
        addPoints(awayTeam, points)
        #print(homeTeam, "v" ,awayTeam, "D")
        #print(homeStats)
        #print(awayStats)
    else:
        points = 3
        addPoints(awayTeam,3)
        #print(homeTeam, "v" ,awayTeam, "A")
    if(ftr==classification):
        if(ftr=="H"):
            odds = bayesMatch[0][2]
            profit(odds, "win")
        elif(ftr=="D"):
            odds = bayesMatch[0][3]
            profit(odds, "win")
        else:
            odds = bayesMatch[0][4]
            profit(odds, "win")
    else:
        profit(1, "lose")
        
predictions = pd.Series(bayesPredictedResults)
actual = pd.Series(actualResults)

profit = printProfit(testingGames)

#Printing classification info
print()
print("Profit if placed £1 on predictions: £",round(profit,2))
target_names = ['A','D','H']
bayesAccuracy = (accuracy_score(actualResults, bayesPredictedResults)) * 100
print("Classification Accuracy: ")
print(bayesAccuracy, "%")
print("Confusion Matrix:")
print()
cm = pd.crosstab(actual, predictions, rownames=['Expected'], colnames=['Predicted'], margins = True)
print(cm)
#uncomment the method call below to show a points projection.
#The points value needs to be correct in the JointMethods.py file in order for this to work.
#printPoints()
print()

