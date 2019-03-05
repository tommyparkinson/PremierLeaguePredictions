#Author Tom Parkinson

import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from scipy.stats import poisson
import csv
from sklearn.metrics import classification_report
from JointMethods import printPoints
from JointMethods import addPoints
from JointMethods import profit
from JointMethods import printProfit
#from printing import printTest

print("POISSON DISTRIBUTION:")
print("Making predictions..")
print()
#data source for 2015/16 season
data = pd.read_csv('poissonActualTesting.csv')
#X is an array of the matches. y is an array of the results in the matches.
X = data.drop(['FTR'], 1)
y=data['FTR']

#Amount of games in training and testing set
trainingGames = 280
testingGames=100

#x is the training data which is all the data up to the defined amount of trainingGames
xTestingSet=np.array(X[trainingGames:])
yTestingSet=np.array(y[trainingGames:])

#y testing data which is all the data after the defined amount of trainingGames
xTrainingSet=np.array(X[:trainingGames])
yTrainingSet=np.array(y[:trainingGames])
actualResults= np.array(yTestingSet)
predictedResults = []

#print(xTrainingSet)
homeWinProb = 0
drawProb = 0
awayWinProb = 0

#init averages
homeGoalsForAverageLeague = 0
homeGoalsAgainstAverageLeague = 0
awayGoalsForAverageLeague = 0
awayGoalsAgainstAverageLeague = 0

#init goals total
homeGoalsForTotal = 0
homeGoalsAgainstTotal = 0
awayGoalsForTotal = 0
awayGoalsAgainstTotal = 0

#init games played
homeGamesPlayedTotal = 0
awayGamesPlayedTotal = 0

#This method calculates the average amount goals scored by home teams and away teams in a match
def calcAverages():
    global homeGoalsForAverageLeague 
    global homeGoalsAgainstAverageLeague 
    global awayGoalsForAverageLeague 
    global awayGoalsAgainstAverageLeague 

    global homeGoalsForTotal 
    global homeGoalsAgainstTotal 
    global awayGoalsForTotal 
    global awayGoalsAgainstTotal

    global homeGamesPlayedTotal
    global awayGamesPlayedTotal
    goalsForTotal=0
    goalsAgainstTotal=0
    gamesPlayed=0

    #loop through all the games in the training set
    for x in range(0,trainingGames):
        i = x+1
        match = np.array(xTrainingSet[x:i])
        #get the amount of goals scored in the match for the home and away team
        goalsFor=match[0][2]
        goalsAgainst=match[0][3]
        #add them to the total
        goalsForTotal += goalsFor
        goalsAgainstTotal += goalsAgainst
        gamesPlayed+=1
    #dived them by the amount of games played to get the average
    homeGoalsForAverageLeague = goalsForTotal/gamesPlayed
    homeGoalsAgainstAverageLeague = goalsAgainstTotal/gamesPlayed
    awayGoalsForAverageLeague = goalsAgainstTotal/gamesPlayed
    awayGoalsAgainstAverageLeague = goalsForTotal/gamesPlayed

#call the method above to get all the averages needed to the classifications.
calcAverages()

#This method makes the classification
def poissonDistCalc(homeTeamExpectedGoals, awayTeamExpectedGoals,):
    global homeWinProb
    global drawProb
    global awayWinProb
    homeTeam = poisson(homeTeamExpectedGoals)
    awayTeam = poisson(awayTeamExpectedGoals)
    #Calculate the probability of scores up to a final score 10-10
    for i in range(0,10):
        for j in range(0,10):
            #pH = prob home team scoring i goals
            #pA = prob away team scoring j goals
            #Example: if i = 1 and j = 2 then this would be the probability of
            #Home team scoring 1 goal and away team scoring 2 goals
            pH = homeTeam.pmf(i)
            pA = awayTeam.pmf(j)
            #They are then multiplied together to get the probability of a final score of 1-2
            prob = (pH*pA)*100

            #Add all the probabilities for home wins, draws and away wins together
            if(i>j):
                homeWinProb = homeWinProb+prob
            elif(i==j):
                drawProb = drawProb+prob
            else:
                awayWinProb = awayWinProb+prob
                
    #Check the highest probability
    if(homeWinProb>drawProb) and (homeWinProb>awayWinProb):
        classification = "H"
    elif(drawProb>homeWinProb and (drawProb>awayWinProb)):
        classification = "D"
    else:
        classification = "A"

    #Reset the variables back to 0 so when the next game is classified, the variables are reset.
    homeWinProb = 0
    drawProb = 0
    awayWinProb = 0
    return classification

#calculating attack and defence strength of each team in comparison to the league average
def teamStrength(homeGoalsFor, homeGoalsAgainst, homeGamesPlayed, awayGoalsFor, awayGoalsAgainst, awayGamesPlayed):
    global homeGoalsForAverageLeague
    global homeGoalsAgainstAverageLeague
    global awayGoalsForAverageLeague
    global awayGoalsAgainstAverageLeague

    #Home team strengths
    homeTeamAverageGoalsFor = homeGoalsFor/homeGamesPlayed
    homeAttackStrength = homeTeamAverageGoalsFor/homeGoalsForAverageLeague
    homeTeamAverageGoalsAgainst = homeGoalsAgainst/homeGamesPlayed
    homeDefenceStrength = homeTeamAverageGoalsAgainst/homeGoalsAgainstAverageLeague
    #away team strengths
    awayTeamAverageGoalsFor = awayGoalsFor/awayGamesPlayed
    awayAttackStrength = awayTeamAverageGoalsFor/awayGoalsForAverageLeague
    awayTeamAverageGoalsAgainst = awayGoalsAgainst/awayGamesPlayed
    awayDefenceStrength = awayTeamAverageGoalsAgainst/awayGoalsAgainstAverageLeague

    #Expected goals for each team based on their strengths
    homeExpectedGoals = homeTeamAverageGoalsFor*homeAttackStrength*awayDefenceStrength
    awayExpectedGoals = awayTeamAverageGoalsFor*awayAttackStrength*homeDefenceStrength

    #call the method to make the classification based on their expected goals
    #The classification uses the expected goals to calculate probabilities of all
    #final scores up to 10-10
    classification = poissonDistCalc(homeExpectedGoals, awayExpectedGoals)
    return classification

#Learning home many goals a team scores at home for a particular team
def homeGoals(teamName):
    goalsScored=0
    goalsConceded=0
    gamesPlayed=0
    homeTeamGoals = []

    for x in range(0,trainingGames):
        if(xTrainingSet[x][0]==teamName):
            goalsScored+=xTrainingSet[x][2]
            goalsConceded+=xTrainingSet[x][3]
            gamesPlayed+=1
    homeTeamGoals.append(goalsScored)
    homeTeamGoals.append(goalsConceded)
    homeTeamGoals.append(gamesPlayed)
    return homeTeamGoals

#Learning how many goals a team scores away for a particular team
def awayGoals(teamName):
    goalsScored=0
    goalsConceded=0
    gamesPlayed = 0
    awayTeamGoals = []
    for x in range(0,trainingGames):
        if(xTrainingSet[x][1]==teamName):
            goalsScored+=xTrainingSet[x][3]
            goalsConceded+=xTrainingSet[x][2]
            gamesPlayed+=1
    awayTeamGoals.append(goalsScored)
    awayTeamGoals.append(goalsConceded)
    awayTeamGoals.append(gamesPlayed)
    return awayTeamGoals  

#Loop through testing games (games you want to predict) and call the methods to make the classification 
for x in range(0,testingGames):
    i = x+1
    match = np.array(xTestingSet[x:i])

    homeTeamName = match[0][0]
    awayTeamName = match[0][1]
    homeTeamStats = homeGoals(homeTeamName)
    awayTeamStats = awayGoals(awayTeamName)

    homeGoalsFor = homeTeamStats[0]
    homeGoalsAgainst = homeTeamStats[1]
    homeGamesPlayed = homeTeamStats[2]

    awayGoalsFor = awayTeamStats[0]
    awayGoalsAgainst = awayTeamStats[1]
    awayGamesPlayed = awayTeamStats[2]

    ftr = yTestingSet[x]
    classification = teamStrength(homeGoalsFor, homeGoalsAgainst, homeGamesPlayed, awayGoalsFor, awayGoalsAgainst, awayGamesPlayed)
    #print(homeTeamName, " v " , awayTeamName, classification)
    predictedResults.append(classification)
    #adding points to a teams projected points
    if(classification=="H"):
        points = 3
        addPoints(homeTeamName,3)
    elif(classification=="D"):
        points = 1
        addPoints(homeTeamName, points)
        addPoints(awayTeamName, points)
    else:
        points = 3
        addPoints(awayTeamName,3)
    #Adding to the profit based on the result
    if(ftr==classification):
        if(ftr=="H"):
            odds = match[0][4]
            profit(odds, "win")
        elif(ftr=="D"):
            odds = match[0][5]
            profit(odds, "win")
        else:
            odds = match[0][6]
            profit(odds, "win")
    else:
        profit(1, "lose")

#Printing the classification info
profit = printProfit(testingGames)
print()
print("Profit if placed £1 on predictions: £",round(profit,2))
print()
predictions = pd.Series(predictedResults)
actual = pd.Series(actualResults)
target_names = ['A','D','H']
poissonAccuracy = (accuracy_score(actualResults, predictedResults)) * 100
print("Classification Accuracy: ")
print(poissonAccuracy, "%")
print()
print("Confusion Matrix:")
print()
cm = pd.crosstab(actual, predictions, rownames=['Expected'], colnames=['Predicted'], margins = True)
print(cm)
#printPoints()
    
