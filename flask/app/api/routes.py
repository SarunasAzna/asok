# import blueprint
from . import api
from flask import jsonify, request
import sqlite3
from collections import OrderedDict
import json


@api.route('/')
def index():
    return jsonify(data='hello there')


@api.route('/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'GET':
        locs = readDatabase()

        return jsonify(locations=locs)

    elif request.method == 'POST':
        data = request.data.decode('utf-8')
        data = json.loads(data)
        print(data)
        insertDatabase(data)

        # FIXME: should return something meaningful to frontend to indicate the
        # success/failure
        return jsonify(a="1")


# Function for sqlite database reading.
def readDatabase():
    conn = sqlite3.connect('./app/api/locations/locations.db')
    c = conn.cursor()
    locs = []
    for row in c.execute('SELECT * FROM locations ORDER BY lat'):
        loc = OrderedDict({'title': row[0],
                           'description': row[1],
                           'lat': row[2],
                           'lng': row[3]})
        locs.append(loc)

    # FIXME: we are reading from the database- there's nothing to save \Justas
    # Save (commit) the changes
    conn.commit()

    # FIXME: could try using "with" statement to automatically close the
    # connection. E.g.
    # with sqlite.connect('...') as conn:
    #    pass
    conn.close()
    return locs


# FIXME: routes.py file is not the place for this- you should make it a command
# in manage.py file. We are already using Flask-script library which provides a
# way to create custom commands https://flask-script.readthedocs.org/en/latest/
#
# Function for sqlite database creation.
# Old database should be deleted.
def createDatabase():
    conn = sqlite3.connect('./app/api/locations/locations.db')
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE locations
                 (title text, description text,  lat real, lng real)''')

    # Larger example that inserts many records at a time
    locations = [('Vilnius', 'Capital of Lithuania', 54.6833, 25.2833),
                 ('Aarhus', 'Second largest city in Denmark', 56.1572, 10.2107),
                 ('Hell', 'Norwegian hell', 63.4444, 10.9225),
                 ('Fucking', 'Fucking, Austria', 48.0672, 12.8636)]

    c.executemany('INSERT INTO locations VALUES (?,?,?,?)', locations)
    # FIXME: shouldn't we close the connection? Try doing it with "with"
    # statement


# Function for sqlite database updatings.
# @return Array : array with new locations information dictionarys
def insertDatabase(location):
    conn = sqlite3.connect('./app/api/locations/locations.db')
    c = conn.cursor()
    '''
    # Larger example that inserts many records at a time
    title = raw_input('title: ')
    description = raw_input('description: ')
    lat = raw_input('latitude: ')
    lng = raw_input('longitude: ')
    '''

    newLocs = [(location['title'],
                location['description'],
                location['lat'],
                location['lng'])]

    # FIXME: executemany? We're only inserting a single location
    c.executemany('INSERT INTO locations VALUES (?,?,?,?)', newLocs)

    # FIXME: why do we want to retrieve locations after inserting?
    locs = []
    for row in c.execute('SELECT * FROM locations ORDER BY lat'):
        locs.append(OrderedDict({'title': row[0],
                                 'description': row[1],
                                 'lat': row[2],
                                 'lng': row[3]}))
    # Save (commit) the changes
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    return locs
