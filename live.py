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

def ShowAll(bestAll):
    i = 1
    print(f'     {"name":20}{"Pos.":6}{"Team":6}{"Rank":>6}{"Tier":>6}{"SoS":>6}{"Comp.":>8}')
    for vals in bestAll.values():

        for player in vals:
            print(f'{str(i) + ".":5}', end= "")
            player.showStats()

        print()
        i = i+1
        if i == 11:
            break
        


def ShowQBs(bestQBs):
    pass

def ShowRBs(bestRBs):
    pass

def ShowWRs(bestWRs):
    pass

def ShowTEs(bestTEs):
    pass

def ShowDEFs(bestDEFs):
    pass

def ShowKs(bestKs):
    pass

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

    print("\nAwaiting input...  (type 'help' to see a list of commands')")

    
    response = input()

    if response == "q":
        break
    
    elif response == "help":
        ShowCommands()

    elif response == "all":
        ShowAll(bestAll)