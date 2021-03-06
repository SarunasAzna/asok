# flask assignment

Requirements:
- [python 3.4](https://docs.python.org/3/)
- [pip](https://pip.pypa.io/en/latest/index.html)
- bash, zsh or similar
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (optional)

## Setup project
```bash
virtualenv --no-site-packages -p /usr/bin/python3.4 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run server
```
# Activate venv if not activated
source venv/bin/activate

# ...and run Werkzeug server
python manage.py runserver
```

## Assignment

Here we have a boilerplate flask application with 2 [blueprints](http://flask.pocoo.org/docs/0.10/blueprints/):
- [api blueprint](app/api/__init__.py) - contains api code
- [frontend blueprint](app/frontend/__init__.py) - contains frontend code


 Your task is to fork this repo and make a webapp which can save (HTTP POST) and retrieve (HTTP GET) locations from [sqlite](https://www.sqlite.org/) database and show them on a map. The communication between browser and server should be done via [Ajax](https://developer.mozilla.org/en/docs/AJAX) (you may use a library for that if you want). The task shouldn't take you longer than 1 working day.

**Location structure in database:**
- title
- description
- lat
- lng

**Additional tasks:**
- make it possible to update locations (PUT /api/locations/&lt;locid&gt;)
- make it possible to delete locations (DELETE /api/locations/&lt;locid&gt;)
- write unit and/or end-to-end tests for the REST API with [Flask-Testing](https://pythonhosted.org/Flask-Testing/) or [unittest](https://docs.python.org/3/library/unittest.html) .
- style the page with [Bootstrap](http://getbootstrap.com/)

**Delivery**

Your fork of this assignment should be publicly accessible (e.g. github). Furthermore, you should either host the resulting webapp and send us a link or provide an easy-to-follow instructions, in your code, for setting it up.

## Relevant docs
- [flask](http://flask.pocoo.org/)
- [sqlite](https://docs.python.org/3.4/library/sqlite3.html)
- [google maps markers](https://developers.google.com/maps/documentation/javascript/markers)
