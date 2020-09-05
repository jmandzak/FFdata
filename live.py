from collections import OrderedDict
from collections import defaultdict
import data.statsio as parse

# useful functions

# function that runs everything from statsio
def Initialize(ppr):
    # fixes position multiplier based on PPR
    if ppr:
        parse.posMultiplier['WR'] = 0.95
        parse.posMultiplier['TE'] = 1.1

    # creates empty players dictionary
    players = {}

    # creates empty teams dictionary
    teams = {}

    # calls all functions to fill in dictionaries

    # strength of schedule
    teams = parse.GetSos("Stats/Sos_Full.txt", teams, "full")
    teams = parse.GetSos("Stats/Sos_Season.txt", teams, "season")
    teams = parse.GetSos("Stats/Sos_Playoff.txt", teams, "playoff")

    # past stats
    players, QBs = parse.ReadQB(players)
    players, RBs = parse.ReadRB(players)
    players, WRs = parse.ReadWR(players)
    players, TEs = parse.ReadTE(players)
    players, Ks = parse.ReadK(players)
    players, DEFs = parse.ReadDEF(players)

    # position specific tiers and rank
    # 3 positions are different based on if the league is PPR
    if ppr:
        players, RBs = parse.PosTiers("Stats/PPR_RB_Tiers.txt", players, RBs, "RB")
        players, WRs = parse.PosTiers("Stats/PPR_WR_Tiers.txt", players, WRs, "WR")
        players, TEs = parse.PosTiers("Stats/PPR_TE_Tiers.txt", players, TEs, "TE")
    else:
        players, RBs = parse.PosTiers("Stats/RB_Tiers.txt", players, RBs, "RB")
        players, WRs = parse.PosTiers("Stats/WR_Tiers.txt", players, WRs, "WR")
        players, TEs = parse.PosTiers("Stats/TE_Tiers.txt", players, TEs, "TE")

    players, QBs = parse.PosTiers("Stats/QB_Tiers.txt", players, QBs, "QB")
    players, Ks = parse.PosTiers("Stats/K_Tiers.txt", players, Ks, "K")
    players, DEFs = parse.DEFTiers(players, DEFs)

    # non position specific rank
    if ppr:
        players, QBs, RBs, WRs, TEs, Ks, DEFs = parse.ReadTiers("Stats/PPR_Tiers.txt", players, QBs, RBs, WRs, TEs, Ks, DEFs)
    else:    
        players, QBs, RBs, WRs, TEs, Ks, DEFs = parse.ReadTiers("Stats/Tiers.txt", players, QBs, RBs, WRs, TEs, Ks, DEFs)

    # assigning strength of schedule values
    players, QBs, RBs, WRs, TEs, Ks, DEFs = parse.AssignSos(players, QBs, RBs, WRs, TEs, Ks, DEFs, teams)

    # calculate composite for each player in each dict
    players = parse.CalcComposite(players)
    QBs = parse.CalcComposite(QBs)
    RBs = parse.CalcComposite(RBs)
    WRs = parse.CalcComposite(WRs)
    TEs = parse.CalcComposite(TEs)
    DEFs = parse.CalcComposite(DEFs)
    Ks = parse.CalcComposite(Ks)

    return players, QBs, RBs, WRs, TEs, Ks, DEFs

# triggered at the beginning of the program and on 'help' command to remind the user what they can do
def ShowCommands():
    print("Type 'all' to see the top 20 available players")
    print("Type 'qb' to see the top 10 available ")
    print("Type 'rb' to see the top 10 available ")
    print("Type 'wr' to see the top 10 available ")
    print("Type 'te' to see the top 10 available ")
    print("Type 'def' to see the top 10 available ")
    print("Type 'k' to see the top 10 available ")

    print("\nWhen you're ready to draft a player or someone else has drafted a player, type 'draft'\n")

    print("To see your own team, type 'team'\n")

    print("Type 'q' to exit the live draft\n")

# this stat line is what shows up above the players when showing best available
def ShowStatLine(position):
    correctStats = {
        "all": f'     {"Name":25}{"Pos.":<6}{"Team":<6}{"Rank":<6}{"Tier":<6}{"SoS":<6}{"Comp.":<8}',
        "qb": f'     {"Name":25}{"Team":<6}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"P.Yds":<8}{"P.TD":<6}{"Int":<4}{"R.Yds":<8}{"R.TD":<6}{"Comp.":<8}',
        "rb": f'     {"Name":25}{"Team":<6}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"Ru.Yds":<8}{"Ru.TD":<6}{"Target":<8}{"Recep":<8}{"Re.Yds":<8}{"Re.TD":<6}{"Comp":<8}',
        "wr": f'     {"Name":25}{"Team":<6}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"Target":<8}{"Recep":<8}{"Yds":<8}{"TD":<4}{"Comp":<8}',
        "te": f'     {"Name":25}{"Team":<6}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"Target":<8}{"Recep":<8}{"Yds":<8}{"TD":<4}{"Comp":<8}',
        "def": f'     {"Name":5}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"Sack":<6}{"FR":<4}{"Int":<4}{"TD":<4}{"K.TD":<6}{"Comp":<8}',
        "k": f'     {"Name":25}{"Team":<6}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"FGM":<4}{"FGA":<4}{"FG%":<6}{"EPM":<4}{"EPA":<4}{"Comp":<8}'
    }

    return correctStats[position]

# function to show top 20 available players
def ShowAll(bestAll, response, players):
    i = 1
    print(ShowStatLine(response))
    print()
    for vals in bestAll.values():

        for player in vals:
            # only show them if they haven't been drafted
            if player.name in players:
                print(f'{str(i) + ".":5}', end= "")
                player.showStats()
                i = i+1

        if i == 21:
            break
        
# function to show top 10 available players at a certain position
def ShowPos(best, pos, players):
    i = 1
    print(ShowStatLine(pos))
    print()
    for vals in best.values():

        for player in vals:
            # only do this if player hasn't been drafted
            if player.name in players:
                print(f'{str(i) + ".":5}', end= "")
                player.showPosStats()
                i = i+1

        if i == 11:
            break

# triggered when you draft a player to your team
def AddToTeam(myTeam, response, All, posMultiplier):
    myTeam[All[response].position].append(All[response])

    print(f'{response} has been added to your team. Great Pick!')

    # now we modify the composite of other available players based on that pick
    posMultiplier[All[response].position] += 0.2

# simply deletes the player from the 'players' dictionary
def RemovePlayer(All, response):
    if response in All:
        del All[response]

# triggered when a player is being drafted, mainly error checking user input
def FindPlayer(All):
    response = input("Please enter the name of the player drafted exactly as it appears on the list, or 'back' to go back\n")
    while True:
        if response == "back":
            break
    
        if response not in All:
            response = input("Couldn't seem to find that player. Please type their name exactly as it appears on the list, or 'back' to go back\n")
        else:
            break
    
    return response

def ShowMyTeam(myTeam):
    print()
    for position in myTeam:
        print(f'{position}:  ', end="")

        for player in myTeam[position]:
            print(f'{player.name:25}', end="")

        print()

def CreateOrderedDicts(allPlayers):
    newDict = defaultdict(list)

    for player in allPlayers.values():
        newDict[player.composite].append(player)
    
    newDict = OrderedDict(sorted(newDict.items()))
    return newDict

def RedoSort(allPlayers, position):
    newDict = defaultdict(list)

    for player in allPlayers.values():
        if player.position == position or position == "all":
            newDict[player.composite].append(player)
        
    newDict = OrderedDict(sorted(newDict.items()))
    return newDict

def RedoComposite(posDict, posMultiplier):
    for player in posDict.values():
        if player.position != '':
            player.composite *= posMultiplier[player.position]
            player.composite = round(player.composite, 2)

def main():
    # intro
    print("\n\n\n\n**********Fantasy Football Ultimate Draft Algorithm**********")
    print("\n\nWelcome to the ultimate fantasy football draft algorithm! Let's get started.\n")

    # figures out what data to parse
    response = input("Before we start, is this a ppr league?\ntype 'y' for yes\ntype 'n' for no\n")
    if response == 'y':
        ppr = True
    else:
        ppr = False

    # get all the players
    players, QBs, RBs, WRs, TEs, Ks, DEFs = Initialize(ppr)

    # make process to put all players into a sorted dictionary by composite
    bestAll = CreateOrderedDicts(players)
    bestQBs = CreateOrderedDicts(QBs)
    bestRBs = CreateOrderedDicts(RBs)
    bestWRs = CreateOrderedDicts(WRs)
    bestTEs = CreateOrderedDicts(TEs)
    bestKs = CreateOrderedDicts(Ks)
    bestDEFs = CreateOrderedDicts(DEFs)

    myTeam = defaultdict(list)

    # Initializes dictionary of team to have 0 players at each position
    myTeam = {
        "QB": [],
        "RB": [],
        "WR": [],
        "TE": [],
        "DEF": [],
        "K": []
    }

    # This dictionary will act as a multiplier to change composite
    # values of available players based on who's in the user's team
    posMultiplier = {
        "QB": 1,
        "RB": 1,
        "WR": 1,
        "TE": 1,
        "DEF": 1,
        "K": 1
    }

    # This is where the program begins
    ShowCommands()

    # beginning of the loop (main menu)
    while(True):

        response = input("\nAwaiting input...  (type 'help' to see a list of commands')\n")

        if response == "q":
            break
        
        elif response == "help":
            ShowCommands()

        elif response == "all":
            ShowAll(bestAll, response, players)
        elif response == "qb":
            ShowPos(bestQBs, response, players)
        elif response == "rb":
            ShowPos(bestRBs, response, players)
        elif response == "wr":
            ShowPos(bestWRs, response, players)
        elif response == "te":
            ShowPos(bestTEs, response, players)
        elif response == "def":
            ShowPos(bestDEFs, response, players)
        elif response == "k":
            ShowPos(bestKs, response, players)

        elif response == "team":
            ShowMyTeam(myTeam)

        # draft block
        elif response == "draft":
            print("Was this player drafted by you or someone else?\n")
            print("Type: 'me' if you drafted the player")
            print("Type: 'other' if someone else drafted the player")
            
            response = input()

            # drafted by me
            if response == "me":
                response = FindPlayer(players)
                if response != "back":
                    # draft the player
                    AddToTeam(myTeam, response, players, posMultiplier)

                    # remove the player
                    RemovePlayer(players, response)
                    RemovePlayer(QBs, response)
                    RemovePlayer(RBs, response)
                    RemovePlayer(WRs, response)
                    RemovePlayer(TEs, response)
                    RemovePlayer(DEFs, response)
                    RemovePlayer(Ks, response)

                    # fix the composites
                    RedoComposite(players, posMultiplier)
                    RedoComposite(QBs, posMultiplier)
                    RedoComposite(RBs, posMultiplier)
                    RedoComposite(WRs, posMultiplier)
                    RedoComposite(TEs, posMultiplier)
                    RedoComposite(DEFs, posMultiplier)
                    RedoComposite(Ks, posMultiplier)

                    bestAll = RedoSort(players, "all")
                    bestQBs = RedoSort(QBs, "QB")
                    bestRBs = RedoSort(RBs, "RB")
                    bestWRs = RedoSort(WRs, "WR")
                    bestTEs = RedoSort(TEs, "TE")
                    bestDEFs = RedoSort(DEFs, "DEF")
                    bestKs = RedoSort(Ks, "K")
                    

            # drafted by someone else
            elif response == "other":
                response = FindPlayer(players)
                if response != "back":
                    RemovePlayer(players, response)

        

if __name__ == '__main__':
    main()