from flask import Response, abort, g, redirect, render_template, request
from database import get_users, insert_user, get_attends, get_workouts, insert_workout, get_leaderboard
from liberated import app
import pdb

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
    

@app.route('/attends')
def attends():
    attends = get_attends()
    return render_template('attends.html', attends = attends)


@app.route('/workouts')
def workouts():
    workouts = get_workouts()
    return render_template('workouts.html', workouts = workouts)


@app.route('/add_workout', methods=['POST'])
def add_workout():
    data = dict( (key, value[0]) for (key, value) in dict(request.form).items() )
    insert_workout(**data)
    return redirect('/workouts')


@app.route('/leaderboard', methods=['GET','POST'])
def leaderboard():

    data = dict( (key, value[0]) for (key, value) in dict(request.form).items() )
    if not data:
        women, men = get_leaderboard("2015-12-25 2016-02-01")
    else:
        women, men = get_leaderboard(**data)

    return render_template('leaderboard.html', women = women, men = men)


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

