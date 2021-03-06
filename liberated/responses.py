from datetime import date, datetime
from flask import Response, abort, g, redirect, render_template, request

from liberated import app
from calendars import HTML_Calendar, AttendanceCalendar
from database import *
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh import embed


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
    

@app.route('/workouts')
def workouts():
    workouts = get_workouts()
    return render_template('workouts.jinja', workouts = workouts)


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

    return render_template('leaderboard.jinja', women = women, men = men)

#@app.route('/plot/<color>')
@app.route('/performance')
def performance():

    users = get_users()
    workouts = get_workouts()

    if not request.args:
        performance_message = 'No user selected'
        return render_template(
            'performance.jinja',
            users=users,
            workouts=workouts,
            performance_message=performance_message
        )

    user = request.args.get('user')
    workout = request.args.get('workout')
    first_name = user.split()[0]
    last_name = user.split()[1]


    ## Get query params from form / buttons
    scores, dates = get_performance(first_name, last_name, workout)

    plot = figure(plot_width=600, plot_height=500, x_axis_type="datetime")

    if scores and len(scores) > 1:
        plot.line(dates, scores, line_width=2)
    elif scores:
        plot.circle(dates, scores)

    if scores:
        script, div = embed.components(plot)
        performance_message = ''
    else:
        script = None
        div = None
        performance_message = 'No performance data for %s with %s' % (first_name, workout)


    return render_template(
        'performance.jinja',
        script=script,
        div=div,
        users=users,
        workouts=workouts,
        performance_message=performance_message
    )


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



@app.route('/attendance', defaults={'class_time': None})
@app.route('/attendance/<class_time>')
def attendance(class_time):
    if class_time is None:
        d = date.today()
        year = d.year
        month = d.month
        day = d.day
        time = '00:00:00'
        class_time = '%d-%d-%d ' % (year, month, day) + time
    else:
        x = datetime.strptime(class_time, '%Y-%m-%d %H:%M:%S')
        d = x.date()
        time = x.time()
        year = d.year
        month = d.month
        day = d.day

    class_times, classes = get_class_times(year, month)
    attendance_sheet = get_attendance_sheet(class_time)
    calendar = AttendanceCalendar(class_times, year, month, 6) # specify first weekday; 6 corresponds to Sunday.


    if class_time in classes:
        end_time = classes[class_time]['end_time']
        level = classes[class_time]['class_type']
    else:
        end_time = None
        level = None

    if month is 1:
        prev_month_url = '/attendance/%d-%d-%d ' % (year - 1, 12, day) + str(time)
    else:
        prev_month_url = '/attendance/%d-%d-%d ' % (year, month - 1, day) + str(time)
    if month is 12:
        next_month_url = '/attendance/%d-%d-%d ' % (year + 1, 1, day) + str(time)
    else:
        next_month_url = '/attendance/%d-%d-%d ' % (year, month + 1, day) + str(time)

    users = get_users()
    return render_template(
        'attendance.jinja',
        class_time=class_time,
        calendar=calendar.formatmonth(year, month),
        attendance_sheet=attendance_sheet,
        prev_month_url=prev_month_url,
        next_month_url=next_month_url,
        users=users,
        end_time=end_time, # specific to the current class
        level=level, # specific to the current class
        show_attendance=bool(level != None)
    )

# Example of adding new data to the database
@app.route('/users_attend/<class_time>', methods=['POST'])
def users_attend(class_time):
    for user in request.form:
        tokens = user.split()
        # hardcoded janky parameter shit
        first_name = tokens[0]
        last_name = tokens[1]
        start_time = class_time
        end_time = class_time.split()[0] + ' ' + tokens[3]
        level = tokens[4]
        record_user_attendance(
            first_name,
            last_name,
            start_time,
            end_time,
            level
        )
    return redirect('/attendance/' + class_time)

@app.route('/add_performance', methods=['GET', 'POST'])
def add_performance():
    data = dict( (key, value[0]) for (key, value) in dict(request.form).items() )
    if not data:
        return render_template('add_performance.jinja')
    else:
        insert_performance(**data)
        return render_template('add_performance.jinja')

@app.route('/login')
def login():
    abort(501)
    this_is_never_executed()



