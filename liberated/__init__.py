import os
from flask import Flask, g, Response, abort
from liberated.configure_engine import configure_engine
from make_json_app import make_json_app

# Instantiate the application.
app = make_json_app(__name__.split('.')[0])

# Instantiate the database 'engine.'
engine = configure_engine()

@app.before_request
def before_request():
    """
    Setup a database connection at the beginning of every request.
    """
    try:
        g.conn = engine.connect()
    except:
        print "uh oh, problem connecting to database"
        import traceback; traceback.print_exc()
        g.conn = None
        abort(500)


@app.teardown_request
def teardown_request(exception):
    """
    Close the database connection at the end of the request.
    """
    db = getattr(g, 'conn', None)
    if db is not None:
        db.close()

# Import route responses.
import liberated.responses
