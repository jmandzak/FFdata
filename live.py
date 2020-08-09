from collections import OrderedDict
from collections import defaultdict
from data.statsio import RunAll

# useful functions

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

    for player in All.values():
        player.composite *= posMultiplier[player.position]
        player.composite = round(player.composite, 2)

    return myTeam

# simply deletes the player from the 'players' dictionary
def RemovePlayer(All, response):
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


def main():
    # get all the players
    players, QBs, RBs, WRs, TEs, Ks, DEFs = RunAll()

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

    # intro
    print("\n\n\n\n**********Fantasy Football Ultimate Draft Algorithm**********")
    print("\n\nWelcome to the ultimate fantasy football draft algorithm! Let's get started.\n")

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
                    myTeam = AddToTeam(myTeam, response, players, posMultiplier)
                    RemovePlayer(players, response)
                    bestAll = RedoSort(players, "all")
                    bestQBs = RedoSort(players, "QB")
                    bestRBs = RedoSort(players, "RB")
                    bestWRs = RedoSort(players, "WR")
                    bestTEs = RedoSort(players, "TE")
                    bestDEFs = RedoSort(players, "DEF")
                    bestKs = RedoSort(players, "K")
                    

            # drafted by someone else
            elif response == "other":
                response = FindPlayer(players)
                if response != "back":
                    RemovePlayer(players, response)

        elif response == "team":
            ShowMyTeam(myTeam)

if __name__ == '__main__':
    main()