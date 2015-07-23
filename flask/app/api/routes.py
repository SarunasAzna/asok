"""First Flask module"""
from . import api
from flask import jsonify, request
import sqlite3
from collections import OrderedDict
import json


@api.route('/')
def index():
    """ Test function """
    return jsonify(data='hello there')


@api.route('/locations', methods=['GET', 'POST'])
def locations():
    """Function for GET and POST."""
    if request.method == 'GET':
        locs = read_database()
        return jsonify(locations=locs)
    elif request.method == 'POST':
        data = request.data.decode('utf-8')
        data = json.loads(data)
        insert_database(data, data['delete'])
        # FIXME(FIXED): should return something meaningful to frontend to
        # indicate the success/failure
        return jsonify(data=data)


@api.route('/locations/<location_id>', methods=['GET', 'PUT', 'DELETE'])
def location(location_id):
    """Fuction editing locations"""

    # ^^^^^ FIXME: the docstring above is misleading. This function isn't only
    # for editing.

    if request.method == 'GET':
        loc = read_location(location_id)
        return jsonify(location=loc)
    elif request.method == 'PUT':
        data = request.data.decode('utf-8')
        data = json.loads(data)
        insert_database(data, data['delete'])
        return jsonify(data=data)
    elif request.method == 'DELETE':
        delete_location(location_id)
        return location_id


def read_location(location_id):
    """Function for reading one location info."""
    loc = "No location with id: %s" % (location_id)
    with sqlite3.connect('./app/api/locations/locations.db') as conn:
        curs = conn.cursor()
        try:
            curs.execute(
                '''SELECT * FROM locations WHERE id = ? ''',
                (location_id,))
            for row in curs:
                loc = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'lat': row[3],
                    'lng': row[4]}
        except:
            loc = 'except is working'
    return loc


def read_database(location_id=False):
    """Function for sqlite database reading."""
    # FIXME(FIXED): we are reading from the database- there's nothing to save
    # Save (commit) the changes
    #
    # conn.commit()
    # FIXME(FIXED): could try using "with" statement to automatically close
    # the connection. E.g.
    # with sqlite.connect('...') as conn:
    #    pass
    # Fixed
    # conn.close()
    with sqlite3.connect('./app/api/locations/locations.db') as conn:
        curs = conn.cursor()
        locs = []
        for row in curs.execute('SELECT * FROM locations ORDER BY id'):
            loc = OrderedDict({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'lat': row[3],
                'lng': row[4]})
            locs.append(loc)
    return locs


def insert_database(location, delete=False):
    """Function for sqlite database updates."""
    with sqlite3.connect('./app/api/locations/locations.db') as conn:
        curs = conn.cursor()

        # FIXME: correct, but you should use "if not delete"
        if delete == False:
            locs = (location['id'],
                    location['title'],
                    location['description'],
                    location['lat'],
                    location['lng'])
            # FIXME: try/except construct should be
            # used to catch genuine errors rather than for flow control.
            try:
                # FIXME(FIXED): executemany? We're only inserting a
                # single location
                curs.execute('INSERT INTO locations VALUES (?,?,?,?,?)', locs)
                # FIXME(FIXED): why do we want to retrieve locations after
                # inserting?
            except:
                curs.execute(
                    '''UPDATE locations SET title = ?, description = ?, \
                        lat = ?, lng = ? WHERE id = ? ''',
                    (locs[1], locs[2], locs[3], locs[4], locs[0]))
        else:
            # FIXME: Is this every used? Why do we have "delete_location" then?
            curs.execute(
                '''DELETE FROM locations WHERE id = ? ''',
                (location["id"],))

            # Save (commit) the changes
            conn.commit()


def delete_location(location_id):
    """Function for deleting location by id."""
    with sqlite3.connect('./app/api/locations/locations.db') as conn:
        curs = conn.cursor()
        curs.execute(
            '''DELETE FROM locations WHERE id = ? ''',
            (location_id,))
        # Save (commit) the changes
        conn.commit()
