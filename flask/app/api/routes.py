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
        locs = read_database()
        return jsonify(locations=locs)
    elif request.method == 'POST':
        data = request.data.decode('utf-8')
        data = json.loads(data)
        insert_database(data, data['delete'])
        # FIXME(FIXED): should return something meaningful to frontend to indicate the
        # success/failure
        # 
        return jsonify(data=data)


## Function for sqlite database reading.
def read_database():
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
            loc = OrderedDict({'id': row[0],
                                'title': row[1],
                                'description': row[2],
                                'lat': row[3],
                                'lng': row[4]})
            locs.append(loc)      
    return locs

## Function for sqlite database updatings.
# @return Array : array with new locations information dictionarys
def insert_database(location, delete=False):
    with sqlite3.connect('./app/api/locations/locations.db') as conn:
        c = conn.cursor() 
        if delete == False:
            locs = (location['id'],
                    location['title'],
                    location['description'],
                    location['lat'],
                    location['lng'],
                    
                    )
            try:
                 # FIXME(FIXED): executemany? We're only inserting a single location
                c.execute('INSERT INTO locations VALUES (?,?,?,?,?)', locs)
                # FIXME(FIXED): why do we want to retrieve locations after inserting?    
            except:
                c.execute('''UPDATE locations SET title = ?, description = ?, lat = ?, lng = ? WHERE id = ? ''',
                    (locs[1], locs[2], locs[3], locs[4], locs[0]))
        else:
            c.execute('''DELETE FROM locations WHERE id = ? ''', (location["id"],))  
            # Save (commit) the changes
            conn.commit()     







