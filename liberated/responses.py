from flask import Response, abort, g, redirect, render_template, request
from database import get_users, insert_user
from liberated import app

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def users():
    users = get_users()
    return render_template('users.html', users = users)


@app.route('/add_user', methods=['POST'])
def add_user():
    data = dict( (key, value[0]) for (key, value) in dict(request.form).items() )
    insert_user(**data)
    return redirect('/users')


@app.route('/another')
def another():
    return render_template('another.html')


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
    abort(501)
    name = request.form['name']
    g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
    return redirect('/')


@app.route('/login')
def login():
    abort(501)
    this_is_never_executed()

