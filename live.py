import sort
from collections import OrderedDict
from collections import defaultdict  

# useful functions

def ShowCommands():
    print("Type 'all' to see the top 20 available players")
    print("Type 'qb' to see the top 10 available ")
    print("Type 'rb' to see the top 10 available ")
    print("Type 'wr' to see the top 10 available ")
    print("Type 'te' to see the top 10 available ")
    print("Type 'def' to see the top 10 available ")
    print("Type 'k' to see the top 10 available ")

    print("\nWhen you're ready to draft a player or someone else has drafted a player, type 'draft'\n")

    print("Type 'q' to exit the live draft\n")

def ShowStatLine(position):
    correctStats = {
        "all": f'     {"Name":20}{"Pos.":<6}{"Team":<6}{"Rank":<6}{"Tier":<6}{"SoS":<6}{"Comp.":<8}',
        "qb": f'     {"Name":20}{"Team":<6}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"P.Yds":<8}{"P.TD":<6}{"Int":<4}{"R.Yds":<8}{"R.TD":<6}{"Comp.":<8}',
        "rb": f'     {"Name":20}{"Team":<6}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"Ru.Yds":<8}{"Ru.TD":<6}{"Target":<8}{"Recep":<8}{"Re.Yds":<8}{"Re.TD":<6}{"Comp":<8}',
        "wr": f'     {"Name":20}{"Team":<6}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"Target":<8}{"Recep":<8}{"Yds":<8}{"TD":<4}{"Comp":<8}',
        "te": f'     {"Name":20}{"Team":<6}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"Target":<8}{"Recep":<8}{"Yds":<8}{"TD":<4}{"Comp":<8}',
        "def": f'     {"Name":5}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"Sack":<6}{"FR":<4}{"Int":<4}{"TD":<4}{"K.TD":<6}{"Comp":<8}',
        "k": f'     {"Name":20}{"Team":<6}{"Rank":<8}{"Tier":<6}{"SoS":<6}{"FGM":<4}{"FGA":<4}{"FG%":<6}{"EPM":<4}{"EPA":<4}{"Comp":<8}'
    }

    return correctStats[position]

def ShowAll(bestAll, response, players):
    i = 1
    print(ShowStatLine(response))
    print()
    for vals in bestAll.values():

        for player in vals:
            if player.name in players:
                print(f'{str(i) + ".":5}', end= "")
                player.showStats()
                i = i+1

        if i == 21:
            break
        
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

# draft mode
def AddToTeam(myTeam, All):
    response = input("Please type player's full name, as it appears on list\n")
    
    while(True):
        # checks if they want to go back
        if response == "back":
            break

        # looks for player in players
        if response in All:
            myTeam[response] = All[response]
            print(f'\nAdded {response} to your team. Great Pick!')
            RemovePlayer(All, response)
            break
        
        # couldn't find player, prompt again
        else:
            response = input("Could not find player, either retype player's full name as it appears on the list or type 'back' to go back\n")

def RemovePlayer(All, response):
    del All[response]

# get all the players
players, QBs, RBs, WRs, TEs, Ks, DEFs = sort.RunAll()

bestAll = defaultdict(list)
bestQBs = defaultdict(list)
bestRBs = defaultdict(list)
bestWRs = defaultdict(list)
bestTEs = defaultdict(list)
bestKs = defaultdict(list)
bestDEFs = defaultdict(list)

for player in players.values():
    bestAll[player.composite].append(player)
for player in QBs.values():
    bestQBs[player.composite].append(player)
for player in RBs.values():
    bestRBs[player.composite].append(player)
for player in WRs.values():
    bestWRs[player.composite].append(player)
for player in TEs.values():
    bestTEs[player.composite].append(player)
for player in Ks.values():
    bestKs[player.composite].append(player)
for player in DEFs.values():
    bestDEFs[player.composite].append(player)

bestAll = OrderedDict(sorted(bestAll.items()))
bestQBs = OrderedDict(sorted(bestQBs.items()))
bestRBs = OrderedDict(sorted(bestRBs.items()))
bestWRs = OrderedDict(sorted(bestWRs.items()))
bestTEs = OrderedDict(sorted(bestTEs.items()))
bestKs = OrderedDict(sorted(bestKs.items()))
bestDEFs = OrderedDict(sorted(bestDEFs.items()))

myTeam = {}

# This is where the program begins

print("\n\n\n\n**********Fantasy Football Ultimate Draft Algorithm**********")
print("\n\nWelcome to the ultimate fantasy football draft algorithm! Let's get started.\n")

print("Type 'all' to see the top 20 available players")
print("Type 'qb' to see the top 10 available ")
print("Type 'rb' to see the top 10 available ")
print("Type 'wr' to see the top 10 available ")
print("Type 'te' to see the top 10 available ")
print("Type 'def' to see the top 10 available ")
print("Type 'k' to see the top 10 available ")

print("\nWhen you're ready to draft a player or someone else has drafted a player, type 'draft'\n")

print("Type 'q' to exit the live draft\n")

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
    elif response == "draft":
        print("Was this player drafted by you or someone else?\n")
        print("Type: 'me' if you drafted the player")
        print("Type: 'other' if someone else drafted the player")
        
        response = input()

        if response == "me":
            AddToTeam(myTeam, players)
        else:
            response = input("Who just got drafted? Please type in the name of the player as it appears on list\n")
            RemovePlayer(players, response)