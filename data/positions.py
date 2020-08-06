# here are all of the class definitions

# this class will hold all strength of schedule stats
class Team:
    def __init__(self):
        self.name = ""

        self.QBfull = 32
        self.QBseason = 32
        self.QBplayoff = 32

        self.RBfull = 32
        self.RBseason = 32
        self.RBplayoff = 32

        self.WRfull = 32
        self.WRseason = 32
        self.WRplayoff = 32

        self.TEfull = 32
        self.TEseason = 32
        self.TEplayoff = 32

        self.DEFfull = 32
        self.DEFseason = 32
        self.DEFplayoff = 32

        self.Kfull = 32
        self.Kseason = 32
        self.Kplayoff = 32

class Player:
    def __init__(self):
        # traits
        self.name = ""
        self.proTeam = ""
        self.position = ""

        # current overall rank
        self.projRank = 500
        self.avgRank = 500

        # current position rank
        self.newPosRank = 500
        self.avgPosRank = 500

        # current tier
        self.tier = 0
        self.posTier = 0

        # current strength of schedule
        self.fullSos = 32
        self.seasonSos = 32
        self.playoffSos = 32

        # past rank
        self.pastPosRank = 0

        # past stats
        self.pastPoints = 0.0
        self.pastPPG = 0.0
        self.games = 0
        
        # composite
        self.composite = 10000.0    # this is the money number that figures out a player's actual value
        

    def showStats(self):
        print(f'{self.name:25}', end="")
        print(f'{self.position:<6}{self.proTeam:<6}{self.avgRank:<6}{self.tier:<6}{self.fullSos:<6}{self.composite:<8}')
    
# all position classes are inherited from player so they have all the values in the player class
class QB(Player):
    def __init__(self):
        super().__init__()
        self.passComp = 0
        self.passAtt = 0
        self.passYard = 0
        self.passTD = 0
        self.passInt = 0
        self.rushAtt = 0
        self.rushYard = 0
        self.rushTD = 0
    
    def showPosStats(self):
        print(f'{self.name:25}', end="")
        print(f'{self.proTeam:<6}{self.avgRank:<8}{self.tier:<6}{self.fullSos:<6}{self.passYard:<8}{self.passTD:<6}{self.passInt:<4}{self.rushYard:<8}{self.rushTD:<6}{self.composite:<8}')

class RB(Player):
    def __init__(self):
        super().__init__()
        self.rushAtt = 0
        self.rushYard = 0
        self.rushTD = 0
        self.recTarget = 0
        self.receptions = 0
        self.recYard = 0
        self.recTD = 0

    def showPosStats(self):
        print(f'{self.name:25}', end="")
        print(f'{self.proTeam:<6}{self.avgRank:<8}{self.tier:<6}{self.fullSos:<6}{self.rushYard:<8}{self.rushTD:<6}{self.recTarget:<8}{self.receptions:<8}{self.recYard:<8}{self.recTD:<6}{self.composite:<8}')

class WR(Player):
    def __init__(self):
        super().__init__()
        self.recTarget = 0
        self.receptions = 0
        self.recYard = 0
        self.recTD = 0
        self.rushAtt = 0
        self.rushYard = 0
        self.rushTD = 0

    def showPosStats(self):
        print(f'{self.name:25}', end="")
        print(f'{self.proTeam:<6}{self.avgRank:<8}{self.tier:<6}{self.fullSos:<6}{self.recTarget:<8}{self.receptions:<8}{self.recYard:<8}{self.recTD:<4}{self.composite:<8}')

class TE(Player):
    def __init__(self):
        super().__init__()
        self.recTarget = 0
        self.receptions = 0
        self.recYard = 0
        self.recTD = 0

    def showPosStats(self):
        print(f'{self.name:25}', end="")
        print(f'{self.proTeam:<6}{self.avgRank:<8}{self.tier:<6}{self.fullSos:<6}{self.recTarget:<8}{self.receptions:<8}{self.recYard:<8}{self.recTD:<4}{self.composite:<8}')

class K(Player):
    def __init__(self):
        super().__init__()
        self.FGM = 0
        self.FGA = 0
        self.FGpercent = 0.0
        self.EPM = 0
        self.EPA = 0

    def showPosStats(self):
        print(f'{self.name:25}', end="")
        print(f'{self.proTeam:<6}{self.avgRank:<8}{self.tier:<6}{self.fullSos:<6}{self.FGM:<4}{self.FGA:<4}{self.FGpercent:<6}{self.EPM:<4}{self.EPA:<4}{self.composite:<8}')

class Defense(Player):
    def __init__(self):
        super().__init__()
        self.games = 16
        self.sack = 0
        self.FR = 0
        self.intercept = 0
        self.TD = 0
        self.PA = 0
        self.passYPG = 0.0
        self.rushYPG = 0.0
        self.safety = 0
        self.kickTD = 0

    def showPosStats(self):
        print(f'{self.name:5}', end="")
        print(f'{self.avgRank:<8}{self.tier:<6}{self.fullSos:<6}{self.sack:<6}{self.FR:<4}{self.intercept:<4}{self.TD:<4}{self.kickTD:<6}{self.composite:<8}')
