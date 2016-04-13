# This module is responsible for executing all database tasks and queries.
from collections import defaultdict
from flask import g
from sqlalchemy import exc
import pdb

def get_users():
    """
    Queries the database for all rows in the 'users' table.
    Returns a list of the users (each user is an object).
    """
    cursor = g.conn.execute('SELECT * FROM users')
    users = []
    for user in cursor:
        users.append({
            'name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email_addr'],
            'gender': user['gender'],
            'level': user['user_level']
        })
    cursor.close()
    return users

def insert_user(first_name, last_name, email_addr, gender, user_level):
    """
    Insert the parameters as a 'user' into the database.
    """
    cursor = g.conn.execute(
        '''
        INSERT INTO users (first_name, last_name, email_addr, gender, user_level)
            VALUES (%s, %s, %s, %s, %s);
        ''',
        (
            first_name,
            last_name,
            email_addr,
            gender,
            user_level
        )
    )

def get_class_times(year, month):
    """
    Queries the database for all class times per day.
    Returns an ordered dictionary { date: [timeA, timeB, timeC ]}
    """
    now = '%s-%s-01' % (year, month)
    if month < 12:
        next_month = '%s-%s-01' % (year, month + 1)
    else:
        next_month = '%s-%s-01' % (year + 1, 1)
    cursor = g.conn.execute(
        '''
        SELECT start_time, end_time, class_type FROM classes
        WHERE start_time >= %s
        AND start_time < %s
        ''',
        (now, next_month)
    )
    classes = []
    clsss = {}
    for c in cursor:
        classes.append(c['start_time'])
        clsss[str(c['start_time'])] = {
            'end_time': str(c['end_time']),
            'class_type': str(c['class_type'])
        }


    dates_dict = defaultdict(list)
    for cl in classes:
        dates_dict[str(cl.date())].append(str(cl.time()))

    cursor.close()
    return dates_dict, clsss


def get_attendance_sheet(class_time):
    """
    Queries the database for the attendees of a given class.
    Returns a list of the names of the attendees.
    """
    if class_time is None:
        return None

    cursor = g.conn.execute(
        '''
        SELECT u.first_name
        FROM users u, attends a
        WHERE start_time = %s
        AND u.first_name = a.first_name
        AND u.last_name = a.last_name;
        ''',
        class_time
    )
    attendees = []
    for attendee in cursor:
        attendees.append(attendee['first_name'])
    return attendees

def record_user_attendance(first_name, last_name, start_time, end_time, class_type):
    """
    Mark a user as present at a given class_time
    """
    try:
        cursor = g.conn.execute(
            '''
            INSERT INTO attends (first_name, last_name, start_time, end_time, class_type)
                VALUES (%s, %s, %s, %s, %s);
            ''',
            (
                first_name,
                last_name,
                start_time,
                end_time,
                class_type
            )
        )
    except:
        pass


def get_workouts():
    cursor = g.conn.execute('SELECT * FROM workouts')
    workouts = []
    for werk in cursor:
        workouts.append({
            'w_name': werk['w_name'],
            'description': werk['description'],
            'rx_male': werk['rx_male'],
            'rx_female': werk['rx_female'],
            'level': werk['level']
        })
    cursor.close()

    return workouts


def insert_workout(w_name, description, rx_male, rx_female, level):
    # Check for empty string parameters and make null if empty
    if not rx_male:
        rx_male = None
    if not rx_female:
        rx_female = None

    try: 
        cursor = g.conn.execute(
            """
            INSERT INTO workouts (w_name, description, rx_male, rx_female, level)
                VALUES (%s, %s, %s, %s, %s) """, 
                (w_name, description, rx_male, rx_female, level))

    except exc.SQLAlchemyError:
        pass

    cursor.close()

def get_leaderboard(test_period):

    start = test_period.split()[0]
    end = test_period.split()[1]

    # try:
    cursor = g.conn.execute(
        """
        with t as (select * from users natural inner join performs_test
                    where t_date > %s and t_date < %s)

        select first_name,last_name, gender, 
                rank() over (partition by gender order by sum(test_score) desc)
        from t
        group by first_name, gender, last_name
        """, (start, end))

    women = []
    men = []
    for item in cursor:
        if item['gender'] == 'f':
            women.append({
                'rank': item['rank'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                    })
        elif item['gender'] == 'm':
            men.append({
                'rank': item['rank'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                    })
    cursor.close()

    return women, men

def get_performance(first_name, last_name, w_name):
    cursor = g.conn.execute (
        """
        select * from performs
        where first_name = %s and last_name = %s
        and w_name = %s """ (first_name, last_name, w_name))



