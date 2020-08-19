from collections import OrderedDict
from collections import defaultdict
import data.statsio as parse
from random import seed
from random import randint
from time import sleep

class Team():
    def __init__(self):
        self.teamName = ""
        self.draftPosition = 0

        self.selections = {}
        
        self.posMultiplier = {
            "QB": 1,
            "RB": 1,
            "WR": 1,
            "TE": 1,
            "DEF": 1,
            "K": 1
        }

        self.roster = defaultdict(list)
        self.roster = {
            "QB": [],
            "RB": [],
            "WR": [],
            "TE": [],
            "DEF": [],
            "K": []
        }


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


def ShowCommands():
    print("Type 'all' to see the top 20 available players")
    print("Type 'qb' to see the top 10 available ")
    print("Type 'rb' to see the top 10 available ")
    print("Type 'wr' to see the top 10 available ")
    print("Type 'te' to see the top 10 available ")
    print("Type 'def' to see the top 10 available ")
    print("Type 'k' to see the top 10 available ")

    print("\nWhen you're ready to draft a player, type 'draft'\n")

    print("To see your own team, type 'team'\n")

    print("Type 'q' to exit the live draft\n")


def showPostDraftCommands():
    print("Type 'myteam' to see your own team")
    print("Type 'all' to see everyone's team")
    print("Type 'mypicks' to see your own picks")
    print("Type 'allpicks' to see the entire draft history")
    print("Type 'q' to quit")


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


def ShowTeam(Team):
    print()
    for position in Team:
        print(f'{position}:  ', end="")

        for player in Team[position]:
            print(f'{player.name:25}', end="")

        print()


def CreateOrderedDicts(allPlayers):
    newDict = defaultdict(list)

    for player in allPlayers.values():
        newDict[player.composite].append(player)
    
    newDict = OrderedDict(sorted(newDict.items()))
    return newDict


# function to assign picks to specified teams
def AssignPicksToTeam(draftOrder, draftPosition, teamName, numTeams):
    for i in range(15):
        draftOrder[draftPosition + (i * numTeams)] = teamName
        draftPosition = numTeams - draftPosition + 1


def UserPick(selection, allPlayers, team, currentPick, draftLog):
    # add to roster
    team.roster[allPlayers[selection].position].append(allPlayers[selection])

    # add to team selections
    team.selections[currentPick] = selection

    # add to overall draft log
    draftLog[currentPick] = selection

    print(f'\n***{selection}*** has been added to your team. Great pick!\n')

    team.posMultiplier[allPlayers[selection].position] += 0.2


def CpuPick(bestPlayers, team, currentPick, draftLog):
    selection = ""
    possibleOptions = []

    # find best available player, add to roster
    # special case to make sure the CPU has a kicker
    if team.posMultiplier["K"] == 1 and len(team.selections) == 14:
        for playerList in bestPlayers.values():
            for player in playerList:
                if player.position == "K":
                    selection = player
                    break
            if selection != "":
                break
    else:
        i = 0
        for playerList in bestPlayers.values():
            for player in playerList:
                possibleOptions.append(player)
                i += 1

            if i == 3:
                break
        
        selection = possibleOptions[randint(0, 2)]
    
    # add team to roster
    team.roster[selection.position].append(selection)

    # add to team's selections
    team.selections[currentPick] = selection.name

    # add to draft log
    draftLog[currentPick] = selection.name

    print(f'\nThe pick is in. {team.teamName} has selected ***{selection.name}***.\n')

    team.posMultiplier[selection.position] += 0.2

    return selection.name



def FindPlayer(allPlayers):
    response = input("\nPlease enter the name of the player drafted exactly as it appears on the list, or 'back' to go back\n")
    while True:
        if response == "back":
            break
    
        if response not in allPlayers:
            response = input("\nCouldn't seem to find that player. Please type their name exactly as it appears on the list, or 'back' to go back\n")
        else:
            break
    
    return response


# simply deletes the player from the 'players' dictionary
def RemovePlayer(All, response):
    if response in All:
        del All[response]


def RedoSort(allPlayers, position):
    newDict = defaultdict(list)

    for player in allPlayers.values():
        if player.position == position or position == "all":
            newDict[player.composite].append(player)
        
    newDict = OrderedDict(sorted(newDict.items()))
    return newDict


def RedoComposite(posDict, posMultiplier):
    for player in posDict.values():
        player.composite *= posMultiplier[player.position]
        player.composite = round(player.composite, 2)

def ResetComposite(posDict, masterComposites):
    for player in posDict.values():
        player.composite = masterComposites[player.name]

def main():
    currentPick = 1
    lastPick = 0            # the numerical value of the last pick of the draft
    teams = {}              # dictionary of all the teams in the draft
    draftOrder = {}         # key = number of the pick, val = team who owns that pick
    masterComposites = {}   # This holds all the players original composites in a dictionary
    draftLog = {}           # This holds the entire draft log, showing who was picked at each spot

    # opening statments
    print("\n\n\n**********Welcome to the Fantasy Football Wizard's Mock Draft!**********\n")
    print("Before we begin the draft, we need to know a few things.")
    
    # some important variables to be used throughout the program
    numTeams = int(input("\nPlease enter the number of teams in your league (i.e. '8', '10', '12', etc.)\n"))
    userPickPosition = input("\nPlease enter the number position you will be drafting (for a random position, please type 'random')\n")

    if userPickPosition == "random":
        userPickPosition = randint(1, int(numTeams))
        print(f'\nYou\'ll be picking at #{userPickPosition}!\n')
    else:
        userPickPosition = int(userPickPosition)

    # figures out what data to parse
    response = input("Before we start, is this a ppr league?\ntype 'y' for yes\ntype 'n' for no\n")
    if response == 'y':
        ppr = True
    else:
        ppr = False

    print("Perfect. Let's begin!\n")

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

    # set all the master composites
    for player in players.values():
        masterComposites[player.name] = player.composite

    # figure out numerical value of last pick
    lastPick = numTeams * 15

    # create teams
    for i in range(numTeams):
        if i+1 == userPickPosition:
            teamName = "Your Team"
            draftPosition = userPickPosition
        else:
            teamName = "Team #" + str(i + 1)
            draftPosition = i + 1
        
        temp = Team()
        temp.teamName = teamName
        temp.draftPosition = draftPosition

        teams[teamName] = temp

    # go through teams to assign picks to teams in the draft
    for team in teams.values():
        AssignPicksToTeam(draftOrder, team.draftPosition, team.teamName, numTeams)

    # order the picks
    draftOrder = OrderedDict(sorted(draftOrder.items()))

    # this is where the mock draft begins
    while(currentPick <= lastPick):
        draftingTeam = draftOrder[currentPick]

        # handle user pick
        if draftingTeam == "Your Team":
            # adjust composites to account for user's team
            RedoComposite(players, teams[draftingTeam].posMultiplier)
            RedoComposite(QBs, teams[draftingTeam].posMultiplier)
            RedoComposite(RBs, teams[draftingTeam].posMultiplier)
            RedoComposite(WRs, teams[draftingTeam].posMultiplier)
            RedoComposite(TEs, teams[draftingTeam].posMultiplier)
            RedoComposite(DEFs, teams[draftingTeam].posMultiplier)
            RedoComposite(Ks, teams[draftingTeam].posMultiplier)

            bestAll = RedoSort(players, "all")
            bestQBs = RedoSort(QBs, "QB")
            bestRBs = RedoSort(RBs, "RB")
            bestWRs = RedoSort(WRs, "WR")
            bestTEs = RedoSort(TEs, "TE")
            bestDEFs = RedoSort(DEFs, "DEF")
            bestKs = RedoSort(Ks, "K")

            print("You're up! Who's it gonna be?")

            while(True):
                response = input("\nAwaiting input...  (type 'help' to see a list of commands')\n")
                
                if response == "q":
                    return
                
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
                    ShowTeam(teams[draftingTeam].roster)

                elif response == "draft":
                    # figure out who the user is drafting
                    response = FindPlayer(players)

                    # draft the player
                    UserPick(response, players, teams[draftingTeam], currentPick, draftLog)

                    # remove the player
                    RemovePlayer(players, response)
                    RemovePlayer(QBs, response)
                    RemovePlayer(RBs, response)
                    RemovePlayer(WRs, response)
                    RemovePlayer(TEs, response)
                    RemovePlayer(DEFs, response)
                    RemovePlayer(Ks, response)

                    # reset composites
                    ResetComposite(players, masterComposites)
                    ResetComposite(QBs, masterComposites)
                    ResetComposite(RBs, masterComposites)
                    ResetComposite(WRs, masterComposites)
                    ResetComposite(TEs, masterComposites)
                    ResetComposite(DEFs, masterComposites)
                    ResetComposite(Ks, masterComposites)

                    # break out of while loop
                    break

        # handle CPU pick
        else:
            print(f'\n{draftingTeam} is on the clock...')

            # recalculate composite of best available players and re-sort
            RedoComposite(players, teams[draftingTeam].posMultiplier)
            bestAll = RedoSort(players, "all")

            # draft the player
            selection = CpuPick(bestAll, teams[draftingTeam], currentPick, draftLog)

            # remove the player
            RemovePlayer(players, selection)
            RemovePlayer(QBs, selection)
            RemovePlayer(RBs, selection)
            RemovePlayer(WRs, selection)
            RemovePlayer(TEs, selection)
            RemovePlayer(DEFs, selection)
            RemovePlayer(Ks, selection)

            # reset composites
            ResetComposite(players, masterComposites)

        currentPick += 1

    print("\n\n*****Congratulations! You've completed the mock draft!*****\n")
    showPostDraftCommands()

    while(True):
        response = input("\nAwaiting input... (type 'help' to see available commands)\n")

        if response == "q":
            break

        elif response == "myteam":
            ShowTeam(teams["Your Team"].roster)

        elif response == "all":
            for team in teams.values():
                print(f'{team.teamName}\'s team:')
                ShowTeam(team.roster)
                print('\n')
        
        elif response == "mypicks":
            for pickNumber, selection in teams["Your Team"].selections.items():
                print(f'{pickNumber:<4}{selection}')
        
        elif response == "allpicks":
            for pickNumber, selection in draftLog.items():
                print(f'{pickNumber:<4}{selection}')

        elif response == "help":
            showPostDraftCommands()
        



if __name__ == "__main__":
    main()