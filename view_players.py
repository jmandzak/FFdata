from data.statsio import RunAll
from collections import OrderedDict     # to sort by key
from collections import defaultdict     # to easily make a dictionary of lists

# put all players into new dictionaries
# this acts essentially as a c++ multimap, storing all players
# with keys as composite and vals as lists of players with that composite

players, QBs, RBs, WRs, TEs, Ks, DEFs = RunAll()

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

f = open("best.txt", 'w')

# some printing for testing purposes
for vals in bestAll.values():
    for player in vals:

        if player.composite != 10000:
            f.write(f'{player.projRank:<5}{player.position:5}{player.name:25}{player.composite}')
            f.write('\n')
