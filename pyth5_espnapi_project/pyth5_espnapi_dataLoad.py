# ESPN API Load
#
# This application will connect to ESPN's API schedule endpoint for any college
# football team mapped in the application's lookup table, then read the the JSON data
# returnted by the API and load the following columns into a normalized SQLite database.
#
# Year
# Date
# Location
# Opponent
# Result
# Score
# Record (overall)
# Record (conference)
# High Passer
# High Passing Yards
# High Rusher
# High Rushing Yards
# High Receiver
# High Receiving Yards
#
# The purpose of the app will be to analyze this data going back 10 years and 
# visualize it in the form various Top 10 GOAT lists.
#
#
# Imports
#
import datetime
import json
import sqlite3
import ssl
import traceback
import urllib.request, urllib.parse

# Base url that can be used to construct the endpoint
#
ESPN_API_ROSTER     = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/'
ESPN_API_SCHEDULE   = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/'
ESPN_API_STATISTICS = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/'

ESPN_URL_ROSTER     = 'https://www.espn.com/college-football/team/roster/_/id/'
ESPN_URL_SCHEDULE   = 'https://www.espn.com/college-football/team/schedule/_/id/'
ESPN_URL_STATISTICS = 'https://www.espn.com/college-football/team/stats/_/id/'

ESPN_URL_TEAM       = 'https://www.espn.com/college-football/team/_/id/'

CURRENT_YEAR        = datetime.datetime.now().year
PREVIOUS_YEAR       = CURRENT_YEAR - 1

# Convenience Methods
#
# Contstruct the API endpoints. Format should be like the examples below:
#
# https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/251/roster
#
def getTeamRosterEndpoint(espnId):
    return ESPN_API_ROSTER + espnId + '/roster'

# https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/251/schedule
#
def getTeamScheduleEndpoint(espnId):
    return ESPN_API_SCHEDULE + espnId + '/schedule'

# https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/251/statistics
#
def getTeamStatisticsEndpoint(espnId):
    return ESPN_API_STATISTICS + espnId + '/statistics'

# https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/251/schedule?season=2024
#
def getTeamSeasonRosterEndpoint(espnId, year):
    return ESPN_API_ROSTER + espnId + '/schedule?season=' + year

# https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/251/schedule?season=2024
#
def getTeamSeasonScheduleEndpoint(espnId, year):
    return ESPN_API_SCHEDULE + str(espnId) + '/schedule?season=' + str(year)

# https://site.api.espn.com/apis/site/v2/sports/football/college-football/teams/251/schedule?season=2024
#
def getTeamSeasonStatisticsEndpoint(espnId, year):
    return ESPN_API_STATS + espnId + '/statistics?season=' + year

# https://www.espn.com/college-football/team/roster/_/id/251
#
def getTeamRosterUrl(espnId):
    return ESPN_URL_ROSTER + espnId

# https://www.espn.com/college-football/team/schedule/_/id/251
#
def getTeamScheduleUrl(espnId):
    return ESPN_URL_SCHEDULE + espnId

# https://www.espn.com/college-football/team/stats/_/id/251
#
def getTeamStatisticsUrl(espnId):
    return ESPN_URL_STATISTICS + espnId

# https://www.espn.com/college-football/team/roster/_/id/251/season/2024
#
def getTeamSeasonRosterUrl(espnId, year):
    return ESPN_URL_ROSTER + espnId + '/season/' + year

# https://www.espn.com/college-football/team/schedule/_/id/251/season/2024
#
def getTeamSeasonScheduleUrl(espnId, year):
    return ESPN_URL_SCHEDULE + espnId + '/season/' + year

# https://www.espn.com/college-football/team/stats/_/id/251/season/2024
#
def getTeamSeasonStatisticsUrl(espnId, year):
    return ESPN_URL_STATISTICS + espnId + '/season/' + year

# https://www.espn.com/college-football/team/_/id/251
#
def teamUrl():
    return ESPN_URL_TEAM + espnId

# Ignore SSL certificate errors
#
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Connect to the database
#
connection = sqlite3.connect('teamstatsdb.sqlite')
cursor     = connection.cursor()

# Prompt for team or default to Texas
#
teamName = input('Enter team name: ')
if len(teamName) < 1:
    teamName = 'Texas'

# Prompt for sport or default to Football
#
sportName = input('Enter sport: ')
if len(sportName) < 1:
    sportName = 'Football'

# Get sport
#
cursor.execute('SELECT id FROM sport WHERE name = ? LIMIT 1', (sportName, ))
sportId = cursor.fetchone()[0]

# Get ESPN's id for the team from the database which is needed to access the correct API endpoint
#
cursor.execute('SELECT id, espn_id FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, sportId))
teamId, espnId = cursor.fetchone()

# Loop through the previous 10 years of statistics
#
yearIterator = 1
while yearIterator <= 20:

    yearToLookAt = CURRENT_YEAR - yearIterator

    teamSeasonScheduleEndpoint = getTeamSeasonScheduleEndpoint(espnId, yearToLookAt)

    try:
        print('Retrieving', teamSeasonScheduleEndpoint)
        teamScheduleHandleForYear = urllib.request.urlopen(teamSeasonScheduleEndpoint, context=ctx)
        teamScheduleDataForYear   = teamScheduleHandleForYear.read().decode()
        print('Retrieved', len(teamScheduleDataForYear), 'characters')
    except Exception as e:
        print("Unable to open API endpoint: " + teamSeasonScheduleEndpoint)
        print("Exception:")
        traceback.print_exc()
        quit()

    # Read the JSON from the endpoint
    #
    teamScheduleJsonForYear = json.loads(teamScheduleDataForYear)

    # Data falls into 3 main categories in the JSON returned by ESPN's API
    # Team data is mostly static, whereas Season and Game (Events) data differ
    # depending on the year requested in the endpoint
    #
    teamData   = teamScheduleJsonForYear['team']
    seasonData = teamScheduleJsonForYear['season']
    eventsData = teamScheduleJsonForYear['events']

    # Debug code
    #
    # print(json.dumps(teamScheduleJsonForYear, indent=4))
    # print(json.dumps(teamData,   indent=4))
    # print(json.dumps(seasonData, indent=4))
    # print(json.dumps(eventsData, indent=4))

    # Store any missing team data in the database (will not update existing values)
    #
    cursor.execute('SELECT display_name FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, sportId))
    displayName = cursor.fetchone()[0]

    cursor.execute('SELECT nickname FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, sportId))
    nickname = cursor.fetchone()[0]

    cursor.execute('SELECT abbreviation FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, sportId))
    abbreviation = cursor.fetchone()[0]

    cursor.execute('SELECT color FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, sportId))
    color = cursor.fetchone()[0]

    cursor.execute('SELECT espn_url_roster FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, sportId))
    espnUrlRoster = cursor.fetchone()[0]

    cursor.execute('SELECT espn_url_schedule FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, sportId))
    espnUrlSchedule = cursor.fetchone()[0]

    cursor.execute('SELECT espn_url_statistics FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, sportId))
    espnUrlStatistics = cursor.fetchone()[0]

    cursor.execute('SELECT espn_url_team FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, sportId))
    espnUrlTeam = cursor.fetchone()[0]

    cursor.execute('SELECT espn_url_logo FROM team WHERE short_name = ? AND sport_id = ? LIMIT 1', (teamName, sportId))
    espnUrlLogo = cursor.fetchone()[0]

    try:
        connection.execute("BEGIN TRANSACTION")

        if displayName is None:
            displayName = teamData['displayName']
            cursor.execute('UPDATE team set display_name = ? WHERE short_name = ? AND sport_id = ?', (displayName, teamName, sportId))

        if nickname is None:
            nickname = teamData['name']
            cursor.execute('UPDATE team set nickname = ? WHERE short_name = ? AND sport_id = ?', (nickname, teamName, sportId))

        if abbreviation is None:
            abbreviation = teamData['abbreviation']
            cursor.execute('UPDATE team set abbreviation = ? WHERE short_name = ? AND sport_id = ?', (abbreviation, teamName, sportId))

        if color is None:
            color = teamData['color']
            cursor.execute('UPDATE team set color = ? WHERE short_name = ? AND sport_id = ?', (color, teamName, sportId))

        if espnUrlRoster is None:
            espnUrlRoster = getTeamRosterUrl(str(espnId))
            cursor.execute('UPDATE team set espn_url_roster = ? WHERE short_name = ? AND sport_id = ?', (espnUrlRoster, teamName, sportId))

        if espnUrlSchedule is None:
            espnUrlSchedule = getTeamScheduleUrl(str(espnId))
            cursor.execute('UPDATE team set espn_url_schedule = ? WHERE short_name = ? AND sport_id = ?', (espnUrlSchedule, teamName, sportId))

        if espnUrlStatistics is None:
            espnUrlStatistics = getTeamStatisticsUrl(str(espnId))
            cursor.execute('UPDATE team set espn_url_statistics = ? WHERE short_name = ? AND sport_id = ?', (espnUrlStatistics, teamName, sportId))

        if espnUrlTeam is None:
            espnUrlTeam = teamData['clubhouse']
            cursor.execute('UPDATE team set espn_url_team = ? WHERE short_name = ? AND sport_id = ?', (espnUrlTeam, teamName, sportId))

        if espnUrlLogo is None:
            espnUrlLogo = teamData['logo']
            cursor.execute('UPDATE team set espn_url_logo = ? WHERE short_name = ? AND sport_id = ?', (espnUrlLogo, teamName, sportId))

        connection.commit()

    except Exception as e:
        print("Exception:")
        traceback.print_exc()
        connection.rollback()

    # Store any season data for the year requested in the database
    #
    cursor.execute('SELECT id FROM season WHERE team_id = ? AND sport_id = ? and YEAR = ? LIMIT 1', (teamId, sportId, yearToLookAt))

    try:
        seasonId = cursor.fetchone()[0]
    except:
        cursor.execute('''INSERT INTO season (team_id, sport_id, year) VALUES (?, ?, ?)''', (teamId, sportId, yearToLookAt))
        connection.commit
        seasonId = cursor.lastrowid

    # Store any season data for the year requested in the database
    #
    for event in eventsData:
        # First check whether the event actually happened! After testing with historical data
        # a lot of games were postponed or canceled in 2020 due to covid, and sometimes inclement weather
        # can also cause this to happen, causing problems with the incoming JSON not comforming as
        # expected. So ignore any event that doesn't have a status of STATUS_FINAL
        #
        status = event['competitions'][0]['status']['type']['name']

        if status == 'STATUS_FINAL':
            seasonType               = event['seasonType']['type']
            seasonTypeName           = event['seasonType']['name']
            weekNumber               = event['week']['number']
            weekName                 = event['week']['text']
            eventDate                = event['date']
            eventShortName           = event['shortName']
            eventName                = event['name']

            homeCompetitor           = event['competitions'][0]['competitors'][0]
            awayCompetitor           = event['competitions'][0]['competitors'][1]

            homeTeamId               = homeCompetitor['team']['id']
            homeTeamName             = homeCompetitor['team']['location']
            homeTeamScore            = homeCompetitor['score']['displayValue']
            homeTeamRecordOverall    = homeCompetitor['record'][0]['displayValue']
            homeTeamRecordConference = homeCompetitor['record'][1]['displayValue']

            awayTeamId               = awayCompetitor['team']['id']
            awayTeamName             = awayCompetitor['team']['location']
            awayTeamScore            = awayCompetitor['score']['displayValue']
            awayTeamRecordOverall    = awayCompetitor['record'][0]['displayValue']
            awayTeamRecordConference = awayCompetitor['record'][1]['displayValue']

            if homeTeamScore > awayTeamScore:
                score = homeTeamScore + "-" + awayTeamScore
            else:
                score = awayTeamScore + "-" + homeTeamScore

            isLeaders = True

            if homeTeamId == str(espnId):
                if homeTeamScore > awayTeamScore:
                    result = "W"
                recordOverall    = homeTeamRecordOverall
                recordConference = homeTeamRecordConference

                # For some teams there are no leader stats for whatever reason
                # so need to deal with that
                #
                try:
                    leaders      = homeCompetitor['leaders']
                except:
                    isLeaders    = False

            elif awayTeamId == str(espnId):
                if awayTeamScore > homeTeamScore:
                    result = "W"
                recordOverall    = awayTeamRecordOverall
                recordConference = awayTeamRecordConference

                # For some teams there are no leader stats for whatever reason
                # so need to deal with that
                #
                try: 
                    leaders     = awayCompetitor['leaders']
                except:
                    isLeaders   = False
            else:
                result = "L"

            if leaders:
                highPasserLastName      = leaders[0]['leaders'][0]['athlete']['lastName']
                highPasserDisplayName   = leaders[0]['leaders'][0]['athlete']['displayName']
                highPasserYards         = leaders[0]['leaders'][0]['value']
                highRusherLastName      = leaders[1]['leaders'][0]['athlete']['lastName']
                highRusherDisplayName   = leaders[1]['leaders'][0]['athlete']['displayName']
                highRusherYards         = leaders[1]['leaders'][0]['value']
                highReceiverLastName    = leaders[2]['leaders'][0]['athlete']['lastName']
                highReceiverDisplayName = leaders[2]['leaders'][0]['athlete']['displayName']
                highReceiverYards       = leaders[2]['leaders'][0]['value']

                # Look up players to see if they exist in the database and create a record for them, if there is none
                #
                cursor.execute('SELECT id FROM player WHERE team_id = (select id from team where espn_id = ?) and last_name = ? and display_name = ? LIMIT 1', (espnId, highPasserLastName, highPasserDisplayName))

                try:
                    highPasserId = cursor.fetchone()[0]
                except:
                    cursor.execute('''INSERT INTO player (team_id, last_name, display_name)
                        VALUES ((select id from team where espn_id = ?), ?, ?)''', (espnId, highPasserLastName, highPasserDisplayName))
                    connection.commit
                    highPasserId = cursor.lastrowid

                cursor.execute('SELECT id FROM player WHERE team_id = (select id from team where espn_id = ?) and last_name = ? and display_name = ? LIMIT 1', (espnId, highRusherLastName, highRusherDisplayName))

                try:
                    highRusherId = cursor.fetchone()[0]
                except:
                    cursor.execute('''INSERT INTO player (team_id, last_name, display_name)
                        VALUES ((select id from team where espn_id = ?), ?, ?)''', (espnId, highRusherLastName, highRusherDisplayName))
                    connection.commit
                    highRusherId = cursor.lastrowid

                cursor.execute('SELECT id FROM player WHERE team_id = (select id from team where espn_id = ?) and last_name = ? and display_name = ? LIMIT 1', (espnId, highReceiverLastName, highReceiverDisplayName))

                try:
                    highReceiverId = cursor.fetchone()[0]
                except:
                    cursor.execute('''INSERT INTO player (team_id, last_name, display_name)
                        VALUES ((select id from team where espn_id = ?), ?, ?)''', (espnId, highReceiverLastName, highReceiverDisplayName))
                    connection.commit
                    highReceiverId = cursor.lastrowid

                # Debug code
                #
                # print(json.dumps(event, indent=4))
                print(str(weekNumber) + " | " + weekName + " | " + seasonTypeName + " | " + eventDate + " | " + eventShortName + " | " + eventName + " | "  + str(homeTeamId) + " | "  + str(homeTeamScore) + " | " 
                    + str(awayTeamId) + " | " + str(awayTeamScore) + " | "  + result + " | "  + recordOverall + " | "  + recordConference + " | "  + highPasserLastName + " | "  + highPasserDisplayName + " | "
                    + str(highPasserYards) + " | " + highRusherLastName + " | "  + highRusherDisplayName + " | "  + str(highRusherYards) + " | "  + highReceiverLastName + " | "  + highReceiverDisplayName + " | "
                    + str(highReceiverYards) + " | ")

                # First check to see if there is an entry in the database for this event and create one if there is not
                # or update null values in the existing record, if there is.
                #
                cursor.execute('SELECT id FROM event WHERE season_id = ? AND week_number = ? LIMIT 1', (seasonId, weekNumber))

                try:
                    eventId = cursor.fetchone()[0]
                except:
                    cursor.execute('''INSERT INTO event (season_id, season_type_id, season_type_name, week_number, week_name, date_time, short_name, name, home_team_id, home_team_score, away_team_id, away_team_score,
                            result, score, record_overall, record_conference, high_passer_id, high_passing_yards, high_rusher_id, high_rushing_yards, high_receiver_id, high_receiving_yards)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (seasonId, seasonType, seasonTypeName, weekNumber, weekName, eventDate, eventShortName, eventName, homeTeamId,
                            homeTeamScore, awayTeamId, awayTeamScore, result, score, recordOverall, recordConference, highPasserId, highPasserYards, highRusherId, highRusherYards, highReceiverId, highReceiverYards))
                    connection.commit
            else:
                # First check to see if there is an entry in the database for this event and create one if there is not
                # or update null values in the existing record, if there is.
                #
                cursor.execute('SELECT id FROM event WHERE season_id = ? AND week_number = ? LIMIT 1', (seasonId, weekNumber))

                try:    
                    eventId = cursor.fetchone()[0]
                except:
                    cursor.execute('''INSERT INTO event (season_id, season_type_id, season_type_name, week_number, week_name, date_time, short_name, name, home_team_id, home_team_score, away_team_id, away_team_score,
                            result, score, record_overall, record_conference)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (seasonId, seasonType, seasonTypeName, weekNumber, weekName, eventDate, eventShortName, eventName, homeTeamId,
                            homeTeamScore, awayTeamId, awayTeamScore, result, score, recordOverall, recordConference))
                    connection.commit

    yearIterator += 1

    connection.commit()

cursor.close()