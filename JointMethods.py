import matplotlib.pyplot as plt

Arsenal = 36
AstonVilla = 8
Bournemouth = 20
Chelsea = 19
CrystalPalace = 30
Everton = 26
Leicester = 38
Liverpool = 27
ManCity = 35
ManUnited = 29
Newcastle = 17
Norwich = 17
Southampton = 24
Stoke = 26
Sunderland = 12
Swansea = 18
Tottenham = 32
Watford = 29
WestBrom = 20
WestHam = 26

acc = 0

def printPoints():
    x=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    y1=[71,17,42,50,42,47,81,60,66,66,37,34,64,51,39,47,70,45,43,62]
    y2=[Arsenal,AstonVilla,Bournemouth,Chelsea,CrystalPalace,Everton, Leicester,Liverpool,ManCity,ManUnited,Newcastle,Norwich,Southampton,Stoke,Sunderland,Swansea,Tottenham,Watford,WestBrom,WestHam]
    plt.scatter(x,y1)
    plt.scatter(x,y2)
    plt.title("Predicted Points v Actual Points")
    plt.xlabel("Team")
    teams=["ARS", "AVL", "BOU", "CHE", "CRY", "EVE","LEI","LIV","MCI", "MUN", "NEW", "NOR", "SOU", "STK", "SUN", "SWA", "TOT", "WAT", "WBA", "WHU"]
    plt.xticks(x,teams)
    plt.ylabel("Points")
    plt.show()

def addPoints(teamName, points):
    global Arsenal
    global AstonVilla
    global Bournemouth
    global Chelsea
    global CrystalPalace
    global Everton
    global Leicester
    global Liverpool
    global ManCity
    global ManUnited
    global Newcastle
    global Norwich
    global Southampton
    global Stoke
    global Sunderland
    global Swansea
    global Tottenham
    global Watford
    global WestBrom
    global WestHam

    if(teamName=="Arsenal"):
        Arsenal = Arsenal + points
    elif(teamName=="Aston Villa"):
        AstonVilla = AstonVilla + points
    elif(teamName=="Bournemouth"):
        Bournemouth = Bournemouth + points
    elif(teamName=="Chelsea"):
        Chelsea = Chelsea + points
    elif(teamName=="Crystal Palace"):
        CrystalPalace = CrystalPalace + points
    elif(teamName=="Everton"):
       Everton = Everton + points
    elif(teamName=="Leicester"):
        Leicester = Leicester + points
    elif(teamName=="Liverpool"):
        Liverpool = Liverpool + points
    elif(teamName=="Man City"):
        ManCity = ManCity + points
    elif(teamName=="Man United"):
        ManUnited = ManUnited + points
    elif(teamName=="Newcastle"):
        Newcastle = Newcastle + points
    elif(teamName=="Norwich"):
        Norwich = Norwich + points
    elif(teamName=="Southampton"):
        Southampton = Southampton + points
    elif(teamName=="Stoke"):
        Stoke = Stoke + points
    elif(teamName=="Sunderland"):
        Sunderland = Sunderland + points
    elif(teamName=="Swansea"):
        Swansea = Swansea + points
    elif(teamName=="Tottenham"):
        Tottenham = Tottenham + points
    elif(teamName=="Watford"):
        Watford = Watford + points
    elif(teamName=="West Brom"):
        WestBrom = WestBrom + points
    elif(teamName=="West Ham"):
        WestHam = WestHam + points
        
def profit(odds, winLose):
    global acc
    if(winLose=="win"):
        acc += odds

def printProfit(amountGamesBetOn):
    global acc
    acc -= amountGamesBetOn
    return acc
