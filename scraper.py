import requests                 # used to access websites
from bs4 import BeautifulSoup   # used to parse html data
import os                       # used to delete files

# function that gets stats of players from 2019-2020
def PastStats(url, filename, position):
  
  filename = "Stats/" + filename
  f = open(filename, "a+")        # opened in append mode because function is called for multiple pages of same position
  players = []
  mod = 0                         # figures out modulus for printing purposes

  # goes to the website
  page = requests.get(url)

  # puts content into soup
  soup = BeautifulSoup(page.text, 'html.parser')

  # sorts through soup to find necessary info
  rows = (soup.find_all(class_='sort1'))

  # gets the actual string text from the website
  for row in rows:
    for string in row.strings:
      players.append(string)
      
  # figure out what position it is for printing purposes
  # basically, each position has different amounts of data, this fixes that
  if position == "QB" or position == "DEF":
    mod = 14
  elif position == "RB" or position == "WR":
    mod = 13
  elif position == "TE":
    mod = 10
  elif position == "K":
    mod = 11
  else:
    print("Bad Position")
    return -1
  
  # this prints out one player and all of his data on a single line, then goes to the next
  count = 0
  for obj in players:
    if count % mod == 0:
      f.write('\n')
    
    f.write(obj + " ")
    count = count + 1
  f.close()

# function to get players in tiers
def FutureTiers(url, filename):
  
  # grab the page and parse the data into soup
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')

  filename = "Stats/" + filename

  f = open(filename, "w")

  # this gets all the players names and their tier and prints to file
  rows = soup.find_all(class_=['full-name', 'grey', 'sticky-cell sticky-cell-one'])

  # this find all gets the avg ranking of each player
  numbers = soup.find_all(class_='view-options ranks')

  # this deletes the header row output
  del numbers[0:6]
  
  avgs = []

  # this code block takes all objects in numbers and only keeps those that are the averages
  # % 6 is used because there are 6 pieces of data per player, but I only want the average
  i = 4
  for avg in numbers:
    if i % 6 == 0:
      avgs.append(avg.text)
    i += 1

  # actually prints to file
  i = 0
  for row in rows:
    if 'Tier' in row.text:
      f.write('\n')
      f.write(row.text)
    else:
      # if row.text is numeric, then it's a new player, so I start a new line
      if row.text.isnumeric():
        f.write('\n')
        f.write(avgs[i])
        f.write(' ')
        i += 1
      f.write(row.text + ' ')
  
  f.close()


# will remain commented out until websites are fixed

# program to get strength of schedule
def SoS(url, filename):
  page = requests.get(url, verify=False)
  soup = BeautifulSoup(page.text, 'html.parser')

  
  filename = "Stats/" + filename

  f = open(filename, "w")

  i = 0

  rows = soup.find_all(class_='c')
  for row in rows:
    if row.text == '' or row.text == '\n':
      pass
    else:
      l = row.text.split('\n')
      for stat in l:
        if stat == '':
          continue

        if i%12 == 0 and i != 0:
          f.write('\n')
        
        f.write(stat)
        f.write(' ')
        i = i + 1
  
  f.close()


# main begins here

# make function calls here
# first, QBs
# also, this website has multiple pages, so we call the same function with multiple websites
if os.path.exists("Stats/QBs.txt"):
  os.remove("Stats/QBs.txt")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=10&LeagueID=26955", "QBs.txt", "QB")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=10&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=1", "QBs.txt", "QB")


# then RBs
if os.path.exists("Stats/RBs.txt"):
  os.remove("Stats/RBs.txt")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=20&LeagueID=26955", "RBs.txt", "RB")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=20&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=1", "RBs.txt", "RB")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=20&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=2", "RBs.txt", "RB")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=20&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=3", "RBs.txt", "RB")

# now WRs
if os.path.exists("Stats/WRs.txt"):
  os.remove("Stats/WRs.txt")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=30&LeagueID=26955", "WRs.txt", "WR")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=30&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=1", "WRs.txt", "WR")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=30&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=2", "WRs.txt", "WR")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=30&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=3", "WRs.txt", "WR")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=30&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=4", "WRs.txt", "WR")

# TEs
if os.path.exists("Stats/TEs.txt"):
  os.remove("Stats/TEs.txt")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=40&LeagueID=26955", "TEs.txt", "TE")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=40&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=1", "TEs.txt", "TE")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=40&LeagueID=26955&order_by=FFPts&sort_order=DESC&cur_page=2", "TEs.txt", "TE")

# Ks
if os.path.exists("Stats/Ks.txt"):
  os.remove("Stats/Ks.txt")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=80&LeagueID=26955", "Ks.txt", "K")

# DEFs
if os.path.exists("Stats/DEFs.txt"):
  os.remove("Stats/DEFs.txt")
PastStats("https://fftoday.com/stats/playerstats.php?Season=2019&GameWeek=&PosID=99&LeagueID=26955", "DEFs.txt", "DEF")

# List of Players 1-311 in tiers
FutureTiers("https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php", "Tiers.txt")

# this website also does tiers by position, so the next few calls are for that
FutureTiers("https://www.fantasypros.com/nfl/rankings/qb-cheatsheets.php", "QB_Tiers.txt")
FutureTiers("https://www.fantasypros.com/nfl/rankings/rb-cheatsheets.php", "RB_Tiers.txt")
FutureTiers("https://www.fantasypros.com/nfl/rankings/wr-cheatsheets.php", "WR_Tiers.txt")
FutureTiers("https://www.fantasypros.com/nfl/rankings/te-cheatsheets.php", "TE_Tiers.txt")
FutureTiers("https://www.fantasypros.com/nfl/rankings/k-cheatsheets.php", "K_Tiers.txt")
FutureTiers("https://www.fantasypros.com/nfl/rankings/dst-cheatsheets.php", "DEF_Tiers.txt")

# Below will be strength of schedule websites, but they're currently broken
# so will be added later

# Calls Strength of Schedule for full season
SoS("https://fftoolbox.fulltimefantasy.com/football/strength_of_schedule.cfm?type=d", "Sos_Full.txt")
SoS("https://fftoolbox.fulltimefantasy.com/football/strength_of_schedule.cfm?type=a", "Sos_Season.txt")
SoS("https://fftoolbox.fulltimefantasy.com/football/strength_of_schedule.cfm?type=f", "Sos_Playoff.txt")