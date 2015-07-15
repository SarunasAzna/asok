from flask.ext.script import Manager
from app.core import create_app
import sqlite3
import flask_script
import os




manager = Manager(create_app)

# FIXME(FIXED): routes.py file is not the place for this- you should make it a command
# in manage.py file. We are already using Flask-script library which provides a
# way to create custom commands https://flask-script.readthedocs.org/en/latest/
# 
## Function for sqlite database creation.
# Old database should be deleted.
@manager.command
def create_database():
    # FIXME: shouldn't we close the connection? Try doing it with "with"
    # statement
    # FIXED
    # promt for creating default database
    choise = flask_script.prompt_bool("Do you want to create new (default) database? "
                                        "All previous changes will be lost.",
                                        default=True, 
                                        yes_choices="y",
                                        no_choices="n")
    database = './app/api/locations/locations.db'
    if choise == True:
        try:
            os.remove(database)
        except OSError:
            pass
        with sqlite3.connect(database) as conn:
            c = conn.cursor()
            # Create table
            c.execute('''CREATE TABLE locations
                    (id INTEGER PRIMARY KEY, title TEXT, description TEXT,  lat TEXT, lng TEXT)''')
            locations = [(1, 'Vilnius', 'Capital of Lithuania', 54.6833, 25.2833),
                     (2, 'Aarhus', 'Second largest city in Denmark', 56.1572, 10.2107),
                     (3, 'Hell', 'Norwegian hell', 63.4444, 10.9225),
                     (4, 'Fucking', 'Fucking, Austria', 48.0672, 12.8636)]
            c.executemany('INSERT INTO locations VALUES (?,?,?,?,?)', locations) 
            conn.commit()


if __name__ == '__main__':
    manager.run()

