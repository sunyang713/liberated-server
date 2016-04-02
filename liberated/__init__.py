import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, g, Response
import yaml
from liberated.configureEngine import configureEngine
# from make_json_app import make_json_app
# app = make_json_app(__name__)
# tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# app = Flask(__name__.split('.')[0], template_folder=tmpl_dir) # @1st-param: from flask docs b/c this is a package now.
app = Flask(__name__.split('.')[0])
import liberated.responses

engine = configureEngine()
#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database,
# containing meaningful data. This is only an example showing you how to run queries in your
# database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
    id serial,
    name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


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
