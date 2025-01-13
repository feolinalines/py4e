# Musical Track Database
#
# This application will read roster data in JSON format, parse the
# file, and then produce an SQLite database that contains a User,
# Course, and Member table and populate the tables from the data file.
#
# You can base your solution on this code:
#       http://www.py4e.com/code3/roster/roster.py
# this code is incomplete as you need to modify the program to store
# the role column in the Member table to complete the assignment.
#
# Imports
#
import json
import sqlite3

# Connect to our database
#
conn = sqlite3.connect('rosterdb.sqlite')
cur  = conn.cursor()

# Cleanup any existing data and create/re-create
# our schma
#
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER PRIMARY KEY,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER PRIMARY KEY,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

# Prompt for file or default to our assignment copy
#
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data.json'

#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:

    name  = entry[0]
    title = entry[1]
    role  = entry[2]

    print((name, title, role))

    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        ( user_id, course_id, role ) )

    conn.commit()