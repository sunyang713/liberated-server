# from make_json_app import make_json_app
# app = make_json_app(__name__)
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool

# Flask imports - create <app> instance.
from flask import Flask, g, Response
app = Flask(__name__.split('.')[0])
import liberated.responses


# Create the database connection engine.
from liberated.configure_engine import configure_engine
engine = configure_engine()


@app.before_request
def before_request():
    """
    At the beginning of every web request, setup a database connection.

    The variable g is globally accessible.
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
    At the end of the web request, close the database connection so that
    the database won't run out of memory.
    """
    try:
        g.conn.close()
    except Exception as e:
        pass
