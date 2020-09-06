from data.positions import *

# this global dict is a look up table to get the abbreviations for defenses, which
# are given in one website as the team's entire name, so that a team's abbr. is always its name
abbr = {
    '49ers' : 'SF',
    'Steelers' : 'PIT',
    'Ravens' : 'BAL',
    'Bills' : 'BUF',
    'Patriots' : 'NE',
    'Rams' : 'LAR',
    'Bears' : 'CHI',
    'Chiefs' : 'KC',
    'Vikings' : 'MIN',
    'Saints' : 'NO',
    'Chargers' : 'LAC',
    'Broncos' : 'DEN',
    'Jets' : 'NYJ',
    'Eagles' : 'PHI',
    'Seahawks' : 'SEA',
    'Titans' : 'TEN',
    'Packers' : 'GB',
    'Cowboys' : 'DAL',
    'Colts' : 'IND',
    'Buccaneers' : 'TB',
    'Browns' : 'CLE',
    'Texans' : 'HOU',
    'Jaguars' : 'JAC',
    'Falcons' : 'ATL',
    'Redskins' : 'WAS',
    'Panthers' : 'CAR',
    'Lions' : 'DET',
    'Raiders' : 'LV',
    'Giants' : 'NYG',
    'Dolphins' : 'MIA',
    'Cardinals' : 'ARI',
    'Bengals' : 'CIN'
}

# This dictionary acts as a look up table for position multiplier for composite calculations
posMultiplier = {
    "QB": 1.3,
    "RB": 0.85,
    "WR": 1,
    "TE": 1.4,
    "DEF": 1.4,
    "K": 3.0,
}

# this function reads QBs.txt and sorts stats from 2019-2020 Quarterbacks
def ReadQB(players):
    f = open("Stats/QBs.txt", "r")

    words = []
    QBs = {}

    # run through the file to pull data
    for line in f:
        words.clear()
        words = line.split()
        if len(words) != 0:

            # create a new Player and fill in relevant data
            p = Player()

            p.position = "QB"
            p.pastPosRank = words[0]
            
            # special case here since some player names are long
            if(len(words) == 16):
                name = words[1] + ' ' + words[2]
                
                # this deletes a value so the rest of the read can go normally
                del words[3]
            else:
                name = words[1] + ' ' + words[2]

            p.name = name.replace('.', '')
        
            p.proTeam = words[3]
            p.games = words[4]
            p.pastPoints = words[13]
            p.pastPPG = words[14]

            players[p.name] = p
            
            q = QB()

            # this statement initializes all the values shared by q and p with values in p
            q.__dict__.update(p.__dict__)

            q.passComp = words[5]
            q.passAtt = words[6]
            q.passYard = words[7]
            q.passTD = words[8]
            q.passInt = words[9]
            q.rushAtt = words[10]
            q.rushYard = words[11]
            q.rushTD = words[12]

            QBs[q.name] = q

    f.close()
    return players, QBs

# This function behaves similarly to ReadQB, except for RBs
def ReadRB(players):
    f = open("Stats/RBs.txt", "r")

    words = []
    RBs = {}

    # iterate through the file
    for line in f:
        words.clear()
        words = line.split()
        if(len(words) != 0):
            p = Player()
            
            p.position = "RB"
            p.pastPosRank = words[0]
            
            # special case here since some player names are long
            if(len(words) == 15):
                name = words[1] + ' ' + words[2]
                
                # this deletes a value so the rest of the read can go normally
                del words[3]
            else:
                name = words[1] + ' ' + words[2]
            
            p.name = name.replace('.', '')
            p.proTeam = words[3]
            p.games = words[4]
            p.pastPoints = words[12]
            p.pastPPG = words[13]

            players[p.name] = p


            r = RB()
            
            # initialize r with all of p's values
            r.__dict__.update(p.__dict__)

            r.rushAtt = words[5]
            r.rushYard = words[6]
            r.rushTD = words[7]
            r.recTarget = words[8]
            r.receptions = words[9]
            r.recYard = words[10]
            r.recTD = words[11]

            RBs[r.name] = r

    f.close()
    return players, RBs

# same as above, but with WRs
def ReadWR(players):
    f = open("Stats/WRs.txt", 'r')
    
    words = []
    WRs = {}

    for line in f:
        words.clear()
        words = line.split()
        
        if(len(words) != 0):
            p = Player()

            p.position = "WR"
            p.pastPosRank = words[0]

            # special case here since some player names are long
            if(len(words) == 15):
                name = words[1] + ' ' + words[2]
                
                # this deletes a value so the rest of the read can go normally
                del words[3]
            else:
                name = words[1] + ' ' + words[2]

            p.name = name.replace('.', '')
            p.proTeam = words[3]
            p.games = words[4]
            p.pastPoints = words[12]
            p.pastPPG = words[13]

            players[p.name] = p


            wr = WR()
            wr.__dict__.update(p.__dict__)

            wr.recTarget = words[5]
            wr.receptions = words[6]
            wr.recYard = words[7]
            wr.recTD = words[8]
            wr.rushAtt = words[9]
            wr.rushYard = words[10]
            wr.rushTD = words[11]

            WRs[wr.name] = wr

    f.close()
    return players, WRs

# same as above
def ReadTE(players):
    f = open("Stats/TEs.txt", 'r')

    words = []
    TEs = {}

    for line in f:
        words.clear()
        words = line.split()
        if(len(words) != 0):
            p = Player()

            p.position = "TE"
            p.pastPosRank = words[0]
            
            # special case here since some player names are long
            if(len(words) == 12):
                name = words[1] + ' ' + words[2]
                
                # this deletes a value so the rest of the read can go normally
                del words[3]
            else:
                name = words[1] + ' ' + words[2]

            p.name = name.replace('.', '')
            p.proTeam = words[3]
            p.games = words[4]
            p.pastPoints = words[9]
            p.pastPPG = words[10]

            players[p.name] = p


            te = TE()
            te.__dict__.update(p.__dict__)

            te.recTarget = words[5]
            te.receptions = words[6]
            te.recYard = words[7]
            te.recTD = words[8]

            TEs[te.name] = te
    
    f.close()
    return players, TEs

# same as above
def ReadK(players):
    f = open("Stats/Ks.txt", 'r')

    words = []
    Ks = {}

    for line in f:
        words.clear()
        words = line.split()
        if(len(words) != 0):
            p = Player()

            p.position = "K"
            p.pastPosRank = words[0]
            
            # special case here since some player names are long
            if(len(words) == 13):
                name = words[1] + ' ' + words[2]
                
                # this deletes a value so the rest of the read can go normally
                del words[3]
            else:
                name = words[1] + ' ' + words[2]

            p.name = name.replace('.', '')
            p.team = words[3]
            p.games = words[4]
            p.pastPoints = words[10]
            p.pastPPG = words[11]

            players[p.name] = p


            k = K()
            k.__dict__.update(p.__dict__)

            k.FGM = words[5]
            k.FGA = words[6]
            k.FGpercent = words[7]
            k.EPM = words[8]
            k.EPA = words[9]

            Ks[k.name] = k

    f.close()
    return players, Ks

#same as above
def ReadDEF(players):
    f = open("Stats/DEFs.txt", 'r')

    words = []
    DEFs = {}

    for line in f:
        words.clear()
        words = line.split()
        if(len(words) != 0):
            p = Player()

            p.position = "DEF"
            p.pastPosRank = words[0]

            name = words[1]
            
            # here we access the look up table declared to get the abbreviation
            name = abbr[name]

            p.name = name
            p.games = words[2]
            p.pastPoints = words[12]
            p.pastPPG = words[13]

            players[p.name] = p


            d = Defense()
            d.__dict__.update(p.__dict__)

            d.sack = words[3]
            d.FR = words[4]
            d.intercept = words[5]
            d.TD = words[6]
            d.PA = words[7]
            d.passYPG = words[8]
            d.rushYPG = words[9]
            d.safety = words[10]
            d.kickTD = words[11]

            DEFs[d.name] = d
    
    f.close()
    return players, DEFs


# this function figures out what tier the player is in by position
# as well as the players rank compared to others at his position
def PosTiers(filename, players, posdict, position):
    f = open(filename, 'r')

    words = []

    for line in f:
        words = line.split()

        # handles blank line cases
        if len(words) == 0:
            pass

        # a line with just "tier x" in it indicates a new tier, this assigns it and moves on
        elif 'Tier' in line:
            tier = int(words[1])
        
        # if this else block occurs, the line is an actual player
        else:
            # assign avg
            avg = float(words[0])
            # assign rank
            rank = int(words[1])
            
            # assign team
            teamName = words[len(words)-1]

            # assign name
            if len(words) == 6:
                name = words[2] + ' ' + words[3]
            else:
                name = words[2] + ' ' + words[3]

            name = name.replace('.', '')

            # see if player is in dict already
            if name in players:
                players[name].newPosRank = rank
                players[name].posTier = tier
                players[name].avgPosRank = avg
                players[name].proTeam = teamName
                
                # checks position specific dict
                if name in posdict:
                    posdict[name].newPosRank = rank
                    posdict[name].posTier = tier
                    posdict[name].avgPosRank = avg
                    posdict[name].proTeam = teamName
            
            # try removing suffix
            elif len(name.split()) == 3:
                split = name.split()
                name = split[0] + ' ' + split[1]
                if name in players:
                    players[name].newPosRank = rank
                    players[name].posTier = tier
                    players[name].avgPosRank = avg
                    players[name].proTeam = teamName

                if name in posdict:
                    posdict[name].newPosRank = rank
                    posdict[name].posTier = tier
                    posdict[name].avgPosRank = avg
                    posdict[name].proTeam = teamName

            # try removing punctuation
            elif '.' in name:
                for char in name:
                    if char == '.':
                        name = name.replace(char, '')
                if name in players:
                    players[name].newPosRank = rank
                    players[name].posTier = tier
                    players[name].avgPosRank = avg
                    players[name].proTeam = teamName

                if name in posdict:
                    posdict[name].newPosRank = rank
                    posdict[name].posTier = tier
                    posdict[name].avgPosRank = avg
                    posdict[name].proTeam = teamName


            # annoying case for Mitchell Trubisky
            # one website calls him "Mitch" instead of Mitchell
            elif 'Mitch' in name:
                name = "Mitchell Trubisky"
                if name in players:
                    players[name].newPosRank = rank
                    players[name].posTier = tier
                    players[name].avgPosRank = avg
                    players[name].proTeam = teamName

                if name in posdict:
                    posdict[name].newPosRank = rank
                    posdict[name].posTier = tier
                    posdict[name].avgPosRank = avg
                    posdict[name].proTeam = teamName
            
            # nothing worked, so create a new player
            else:
                p = Player()
                p.name = name
                p.position = position
                p.newPosRank = rank
                p.posTier = tier
                p.proTeam = words[len(words)-1]
                p.avgPosRank = avg
                p.proTeam = teamName
                players[p.name] = p

                if position == 'QB':
                    player = QB()
                elif position == 'RB':
                    player = RB()
                elif position == 'WR':
                    player = WR()
                elif position == 'TE':
                    player = TE()
                else:
                    player = K()
                
                player.__dict__.update(p.__dict__)
                posdict[player.name] = player
            
    f.close()
    return players, posdict
            
# made Def tiers a separate function because it would make the above function too clunky
def DEFTiers(players, DEFs):
    f = open("Stats/DEF_Tiers.txt", 'r')

    words = []

    for line in f:
        words = line.split()

        # handles empty line
        if len(words) == 0:
            pass
        
        # handles line that indicates a new tier
        elif 'Tier' in line:
            tier = int(words[1])
        
        # handles player line
        else:
            avg = float(words[0])
            rank = int(words[1])
            name = words[len(words)-1]

            # Defenses name on this website look like (SF),
            # so we take out the parantheses to get the abbr.
            name = name.replace('(', '')
            name = name.replace(')', '')
            
            players[name].newPosRank = rank
            players[name].proTeam = name
            players[name].posTier = tier
            players[name].avgPosRank = avg

            DEFs[name].newPosRank = rank
            DEFs[name].proTeam = name
            DEFs[name].posTier = tier
            DEFs[name].avgPosRank = avg

    f.close()
    return players, DEFs

# Reads in the overall Tier of all players
def ReadTiers(filename, players, QBs, RBs, WRs, TEs, Ks, DEFs):
    f = open(filename, 'r')

    words = []

    for line in f:
        words = line.split()

        # handles empty lines
        if len(words) == 0:
            pass
        
        # handles new Tier
        elif 'Tier' in words:
            tier = int(words[1])
        
        # handles player info
        else:
            avg = float(words[0])
            rank = int(words[1])

            # figure out name length
            # the ( ) case is for defenses
            if '(' in line:
                name = words[len(words)-1]
            elif len(words) == 6:
                name = words[2] + ' ' + words[3]
                del words[4]
            else:
                name = words[2] + ' ' + words[3]

            name.replace('.', '')
            
            # get rid of ( ) in defenses name
            if '(' in name:
                name = name.replace('(', '')
                name = name.replace(')', '')

            # see if player is in dict already
            if name in players:
                players[name].projRank = rank
                players[name].tier = tier
                players[name].avgRank = avg
                
                if name == "Tyler Bass":
                    players[name].position = 'K'
            
            # try removing suffix
            elif len(name.split()) == 3:
                split = name.split()
                name = split[0] + split[1]
                if name in players:
                    players[name].projRank = rank
                    players[name].tier = tier
                    players[name].avgRank = avg

            # try removing punctuation
            elif '.' in name:
                for char in name:
                    if char == '.':
                        name = name.replace(char, '')
                if name in players:
                    players[name].projRank = rank
                    players[name].tier = tier
                    players[name].avgRank = avg


            # annoying case for mitchell Trubisky
            elif 'Mitch' in name:
                name = "Mitchell Trubisky"
                if name in players:
                    players[name].projRank = rank
                    players[name].tier = tier
                    players[name].avgRank = avg
            
            # nothing worked
            else:
                p = Player()
                p.name = name
                p.projRank = rank
                p.tier = tier
                p.avgRank = avg
                
                if name == "Tyler Bass":
                    p.position = 'K'
                players[p.name] = p


            # at this point, name is either correct or it's not worth
            # creating a specific position as it won't have most data
            if name in QBs:
                QBs[name].projRank = rank
                QBs[name].tier = tier
                QBs[name].avgRank = avg
            elif name in RBs:
                RBs[name].projRank = rank
                RBs[name].tier = tier
                RBs[name].avgRank = avg
            elif name in WRs:
                WRs[name].projRank = rank
                WRs[name].tier = tier
                WRs[name].avgRank = avg
            elif name in TEs:
                TEs[name].projRank = rank
                TEs[name].tier = tier
                TEs[name].avgRank = avg
            elif name in  DEFs:
                DEFs[name].projRank = rank
                DEFs[name].tier = tier
                DEFs[name].avgRank = avg
            elif name in Ks:
                Ks[name].projRank = rank
                Ks[name].tier = tier
                Ks[name].avgRank = avg

    f.close()
    return players, QBs, RBs, WRs, TEs, Ks, DEFs

def GetSos(filename, teams, part):
    f = open(filename, 'r')

    for line in f:
        line = line.split()
        name = line[0]

        # special case for Oakland Raiders
        if name == "OAK":
            name = "LV"
        elif name == "JAX":
            name = "JAC"

        qb = int(line[1])
        rb = int(line[2])
        wr = int(line[3])
        te = int(line[4])
        k = int(line[5])
        df = int(line[6])


        if part == 'full':
            team = Team()

            team.name = name
            team.QBfull = qb
            team.RBfull = rb
            team.WRfull = wr
            team.TEfull = te
            team.Kfull = k
            team.DEFfull = df

            teams[team.name] = team

        elif part == 'season':
            teams[name].QBseason = qb
            teams[name].RBseason = rb
            teams[name].WRseason = wr
            teams[name].TEseason = te
            teams[name].DEFseason = df
            teams[name].Kseason = k

        elif part == 'playoff':
            teams[name].QBplayoff = qb
            teams[name].RBplayoff = rb
            teams[name].WRplayoff = wr
            teams[name].TEplayoff = te
            teams[name].DEFplayoff = df
            teams[name].Kplayoff = k

    team = Team()
    team.name = 'FA'
    
    teams[team.name] = team

    f.close()

    return teams

def AssignSos(players, QBs, RBs, WRs, TEs, Ks, DEFs, teams):
    for player in players.values():
        
        teamName = player.proTeam
        if teamName == '':
            continue

        if player.position == 'QB':
            player.fullSos = teams[teamName].QBfull
            player.seasonSos = teams[teamName].QBseason
            player.playoffSos = teams[teamName].QBplayoff
            QBs[player.name].__dict__.update(player.__dict__)
        
        elif player.position == 'RB':
            player.fullSos = teams[teamName].RBfull
            player.seasonSos = teams[teamName].RBseason
            player.playoffSos = teams[teamName].RBplayoff
            RBs[player.name].__dict__.update(player.__dict__)

        elif player.position == 'WR':
            player.fullSos = teams[teamName].WRfull
            player.seasonSos = teams[teamName].WRseason
            player.playoffSos = teams[teamName].WRplayoff
            WRs[player.name].__dict__.update(player.__dict__)

        elif player.position == 'TE':
            player.fullSos = teams[teamName].TEfull
            player.seasonSos = teams[teamName].TEseason
            player.playoffSos = teams[teamName].TEplayoff
            TEs[player.name].__dict__.update(player.__dict__)

        elif player.position == 'K':
            player.fullSos = teams[teamName].Kfull
            player.seasonSos = teams[teamName].Kseason
            player.playoffSos = teams[teamName].Kplayoff
            Ks[player.name].__dict__.update(player.__dict__)

        elif player.position == 'DEF':
            player.fullSos = teams[teamName].DEFfull
            player.seasonSos = teams[teamName].DEFseason
            player.playoffSos = teams[teamName].DEFplayoff
            DEFs[player.name].__dict__.update(player.__dict__)
            
    return players, QBs, RBs, WRs, TEs, Ks, DEFs

def CalcComposite(players):
    for player in players.values():
        if player.avgPosRank != 500 and player.avgRank != 500:
            player.composite = player.avgPosRank + player.avgRank + player.projRank + player.newPosRank + player.tier + player.posTier + (player.fullSos / 4)
            player.composite *= posMultiplier[player.position]
            player.composite = round(player.composite, 2)

    return players