from html_calendar import HTML_Calendar
from datetime import date
from flask import Response, abort, g, redirect, render_template, request
from database import get_users, insert_user
from liberated import app

@app.route('/')
def index():
    return render_template('index.jinja')


@app.route('/users')
def users():
    users = get_users()
    return render_template('users.jinja', users = users)


@app.route('/add_user', methods=['POST'])
def add_user():
    data = dict( (key, value[0]) for (key, value) in dict(request.form).items() )
    insert_user(**data)
    return redirect('/users')


@app.route('/another')
def another():
    return render_template('another.jinja')


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
    abort(501)
    name = request.form['name']
    g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
    return redirect('/')


@app.route('/calendar', defaults={'year': date.today().year, 'month': date.today().month, 'test': date.today().day})
@app.route('/calendar/<int:year>/<int:month>')
@app.route('/calendar/<int:test>', defaults={'year': date.today().year, 'month': date.today().month})
def calendar(year, month, test):
    calendar = HTML_Calendar(6) # specify first weekday; 6 corresponds to Sunday.
    return render_template('calendar.jinja', calendar=calendar.formatmonth(year, month), test=test)



@app.route('/login')
def login():
    abort(501)
    this_is_never_executed()



