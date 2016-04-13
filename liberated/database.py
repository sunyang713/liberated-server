# This module is responsible for executing all database tasks and queries.
from collections import defaultdict
from flask import g

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
            VALUES ('{first_name}', '{last_name}', '{email_addr}', '{gender}', '{user_level}');
        '''
        .format(
            first_name=first_name,
            last_name=last_name,
            email_addr=email_addr,
            gender=gender,
            user_level=user_level
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
        SELECT start_time FROM classes
        WHERE start_time >= %s
        AND start_time < %s
        ''',
        (now, next_month)
    )
    classes = []
    for c in cursor:
        classes.append(c['start_time'])

    dates_dict = defaultdict(list)
    for cl in classes:
        dates_dict[str(cl.date())].append(str(cl.time()))

    cursor.close()
    return dates_dict


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


