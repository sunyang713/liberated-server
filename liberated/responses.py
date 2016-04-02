from flask import request, render_template, g, redirect, Response
from liberated import app
from database import get_users, insert_user

#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the '/' path using a GET request
#
# If you wanted the user to go to, for example, localhost:4111/foobar/ with POST or GET then you could use:
#
#       @app.route('/foobar/', methods=['POST', 'GET'])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
    """
    request is a special object that Flask provides to access web request information:

    request.method:   'GET' or 'POST'
    request.form:     if the browser submitted a form, this contains the data in the form
    request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

    See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
    """

    # DEBUG: this is debugging code to see what request looks like
    # print request.args

    # a database query
    cursor = g.conn.execute('SELECT name FROM test')
    names = []
    for result in cursor:
        names.append(result['name'])  # can also be accessed using result[0]
    cursor.close()

    context = dict(data = names)

    return render_template('index.html', **context)


@app.route('/users')
def users():
    users = get_users()
    return render_template('users.html', users = users)


@app.route('/add_user', methods=['POST'])
def add_user():
    data = dict( (key, value[0]) for (key, value) in dict(request.form).items() )
    print data
    insert_user(**data)
    return redirect('/users')


@app.route('/another')
def another():
    return render_template('another.html')


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
    return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()

