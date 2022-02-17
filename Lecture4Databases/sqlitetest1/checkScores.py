#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('scores.db')
for row in conn.execute('SELECT * FROM Scores'):
        print row