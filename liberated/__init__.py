import os
from flask import Flask, g, Response
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

@app.teardown_request
def teardown_request(exception):
    """
    Close the database connection at the end of the request.
    """
    try:
        g.conn.close()
    except Exception as e:
        pass

# Import route responses.
import liberated.responses
