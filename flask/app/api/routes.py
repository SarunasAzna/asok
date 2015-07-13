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
        insertDatabase(data)
        # FIXME(FIXED): should return something meaningful to frontend to indicate the
        # success/failure
        # 
        return jsonify(data=data)


## Function for sqlite database reading.
def readDatabase():
   
    # FIXME(FIXED): we are reading from the database- there's nothing to save \Justas
    # Save (commit) the changes
    # 
    #conn.commit()

    # FIXME(FIXED): could try using "with" statement to automatically close the
    # connection. E.g.
    # with sqlite.connect('...') as conn:
    #    pass
    # Fixed
    #conn.close()
    with sqlite3.connect('./app/api/locations/locations.db') as conn:
        c = conn.cursor()
        locs = []
        for row in c.execute('SELECT * FROM locations ORDER BY lat'):
            loc = OrderedDict({'title': row[0],
                               'description': row[1],
                               'lat': row[2],
                               'lng': row[3]})
            locs.append(loc)      


    return locs



## Function for sqlite database updatings.
# @return Array : array with new locations information dictionarys
def insertDatabase(location):
  
    with sqlite3.connect('./app/api/locations/locations.db') as conn:
        c = conn.cursor()
        locs = []
        newLocs = (location['title'],
                location['description'],
                location['lat'],
                location['lng'])
        # FIXME(FIXED): executemany? We're only inserting a single location
        c.execute('INSERT INTO locations VALUES (?,?,?,?)', newLocs)
        # FIXME(FIXED): why do we want to retrieve locations after inserting?
        # Save (commit) the changes
        conn.commit()     

    return locs






