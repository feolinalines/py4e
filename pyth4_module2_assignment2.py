# Counting Organizations
#
# This application will read the mailbox data (mbox.txt) and count the number
# of email messages per organization (i.e. domain name of the email address)
# using a database with the following schema to maintain the counts.
#
# Imports
#
import re
import sqlite3

# Connect to our SQLite3 database
#
conn = sqlite3.connect('pyth4_module2_assignment2.sqlite')
cur = conn.cursor()

# DB Cleanup
#
cur.execute('DROP TABLE IF EXISTS Counts')

# Create the Counts table
#
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

# Prompt for file to examine and import org and count
# from each line. Add a row if the org isn't found, or
# update the count if it does.
#
fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'code3/mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()

    # We need to extract the org domain from the email address to store
    #
    email   = pieces[1]
    orgList = re.findall(r'@([A-Za-z0-9.-]+)', email)
    org     = orgList[0]

    # Update or insert org record
    #
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

# Print out our counted results
# 
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()