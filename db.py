import sqlite3 as sql

con = None

try:
    con = sql.connect('rates_story.db')
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')

    data = cur.fetchone()

    print "SQLite version: %s" % data

except sql.Error, e:

    print "Error %s:" % e.args[0]
    exit(1)

finally:

    if con:
        con.close()