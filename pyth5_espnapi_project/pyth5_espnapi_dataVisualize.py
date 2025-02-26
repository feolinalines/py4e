# pyth5_espnapi_dataLoad loads the top passer, rusher, and receiver for each game for a given college football team
# for the past 20 years using ESPN's API.
#
# pyth5_espnapi_dataVisualize presents Top 00 lists of the greatest players for each school using 
# these stats. Basically all we are doing for this project is to total up all the "leading" stats
# for a player and then present that in a Top 20 list. It's debateable what constitutes a "great"
# player at the college level, but in today's world where players transfer, or leave early one could
# argue that a player who is consistently a leading contributorr and loyal to one school over a
# number of years is a greater player than one who did the same at two or three schools, or played
# only a year or two before going to the NFL.
#
# Applying this to basketball, a great example of this is someone like Kevin Durant, who is one of
# the greatest players of all time. However, he played only one season at Texas, and did very well
# but should he be considered the greated Texas player of all time because of that, or what he's 
# subsequently done in the NBA over a player like LamMarcus Aldridge or Daniel Gibson who played 
# 3-4 seasons at Texas, and did equally well.
#
# Note: A player's stats only count if the player was a leading passer, rusher, or receiver in a
# game. So it's really a GOAT list of the best of the best of the best.
# 
# Given more time these lists could be expanded to encompass other/more stats. ESPN's public API is
# pretty extensive, however it is also mostly undocumented. Definitely part of the fun of this
# project was to explore it, and find all kinds of useful data.

# Imports
import sqlite3
from   tabulate import tabulate

# Global Variables
#
SPORT_ID    = '1'
FETCH_LIMIT = 20

# Database connection
#
connection = sqlite3.connect('teamstatsdb.sqlite')
cursor     = connection.cursor()

# Prompt for which Top 20 list (or default to Top 20 Passer)
#
listType = input("Select List Type: (1) Top 20 Passers (2) Top 20 Rushers (3) Top 20 Receivers: ")
if len(listType) < 1:
    listType = 1
else:
    listType = int(listType)

# Prompt for team or default to all teams
#
teamName = input("Enter team name or hit 'Enter' for all: ")
if len(teamName) < 1:
    teamName = 'All'

# Get Team id for the team from the database which is needed to access the correct API endpoint (defaulting to Football for now)
#
if teamName != 'All':
    cursor.execute('SELECT id FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, SPORT_ID))  
    teamId = cursor.fetchone()[0]

print(listType)
print(teamName)

# Visualize using tabulate
#
if teamName != 'All':
    headers = ["NAME", "YARDS"]
    # Top 20 GOAT Passer (Specific school)
    #
    if listType == 1:
        cursor.execute('SELECT display_name, SUM(high_passing_yards) FROM event, player WHERE season_id IN (SELECT id  FROM season WHERE team_id = ? AND sport_id = ?) AND event.high_passer_id = player.id GROUP BY event.high_passer_id ORDER BY SUM(high_passing_yards) DESC LIMIT ?;', (teamId, SPORT_ID, FETCH_LIMIT))
        highPasserData = cursor.fetchall()
        print(tabulate(highPasserData, headers=headers, tablefmt="fancy_grid"))

    # Top 20 GOAT Rusher (Specific school)
    #
    elif listType == 2:
        cursor.execute('SELECT display_name, SUM(high_rushing_yards) FROM event, player WHERE season_id IN (SELECT id  FROM season WHERE team_id = ? AND sport_id = ?) AND event.high_rusher_id = player.id GROUP BY event.high_rusher_id ORDER BY SUM(high_rushing_yards) DESC LIMIT ?;', (teamId, SPORT_ID, FETCH_LIMIT))
        highRusherData = cursor.fetchall()
        print(tabulate(highRusherData, headers=headers, tablefmt="fancy_grid"))

    # Top 20 GOAT Receiver (Specific school)
    #
    elif listType == 3:
        cursor.execute('SELECT display_name, SUM(high_receiving_yards) FROM event, player WHERE season_id IN (SELECT id  FROM season WHERE team_id = ? AND sport_id = ?) AND event.high_receiver_id = player.id GROUP BY event.high_receiver_id ORDER BY SUM(high_receiving_yards) DESC LIMIT ?;', (teamId, SPORT_ID, FETCH_LIMIT))
        highRecieverData = cursor.fetchall()
        print(tabulate(highRecieverData, headers=headers, tablefmt="fancy_grid"))
else:
    headers = ["NAME", "TEAM NAME", "YARDS"]
    # Top 20 GOAT Passer (All loaded schools)
    #
    if listType == 1:
        cursor.execute('SELECT player.display_name, team.display_name, SUM(high_passing_yards) FROM event, player, team WHERE season_id IN (SELECT id  FROM season WHERE sport_id = ?) AND event.high_passer_id = player.id AND player.team_id = team.id GROUP BY event.high_passer_id ORDER BY SUM(high_passing_yards) DESC LIMIT ?;', (SPORT_ID, FETCH_LIMIT))
        highPasserData = cursor.fetchall()
        print(tabulate(highPasserData, headers=headers, tablefmt="fancy_grid"))

    # Top 20 GOAT Rusher (All loaded schools)
    #
    elif listType == 2:
        cursor.execute('SELECT player.display_name, team.display_name, SUM(high_rushing_yards) FROM event, player, team WHERE season_id IN (SELECT id  FROM season WHERE sport_id = ?) AND event.high_rusher_id = player.id AND player.team_id = team.id GROUP BY event.high_rusher_id ORDER BY SUM(high_rushing_yards) DESC LIMIT ?;', (SPORT_ID, FETCH_LIMIT))
        highRusherData = cursor.fetchall()
        print(tabulate(highRusherData, headers=headers, tablefmt="fancy_grid"))

    # Top 20 GOAT Receiver (All loaded schools)
    #
    elif listType == 3:
        cursor.execute('SELECT player.display_name, team.display_name, SUM(high_receiving_yards) FROM event, player, team WHERE season_id IN (SELECT id  FROM season WHERE sport_id = ?) AND event.high_receiver_id = player.id AND player.team_id = team.id GROUP BY event.high_receiver_id ORDER BY SUM(high_receiving_yards) DESC LIMIT ?;', (SPORT_ID, FETCH_LIMIT))
        highRecieverData = cursor.fetchall()
        print(tabulate(highRecieverData, headers=headers, tablefmt="fancy_grid"))

cursor.close()