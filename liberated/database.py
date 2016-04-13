# This module is responsible for executing all database tasks and queries.
from flask import g
from sqlalchemy import exc
import pdb

def get_users():
    """
    A database query. <conn.execute> returns a "ResultProxy."
    See http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.ResultProxy
    Basically it's a pseudo data structure that holds the 'table' you just retrieved.
    You can iterate over the rows with a for-loop and transform it to a manageable python-native data structure.
    But careful, each element is still of type 'schema.Column' (SQLAlchemy), so you need to deconstruct further.
    """
    cursor = g.conn.execute('SELECT * FROM users')
    users = [] # My resulting data structure - a 'matrix' corresponding to the table.
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
    cursor = g.conn.execute(
        """
        INSERT INTO users (first_name, last_name, email_addr, gender, user_level)
            VALUES ('{first_name}', '{last_name}', '{email_addr}', '{gender}', '{user_level}');
        """
        .format(
            first_name = first_name,
            last_name = last_name,
            email_addr = email_addr,
            gender = gender,
            user_level = user_level
        )
    )

def get_attends():    
    cursor = g.conn.execute('SELECT * FROM attends')
    attends = []
    for item in cursor:
        attends.append({
            'first_name': item['first_name'],
            'last_name': item['last_name'],
            'start': item['start_time'],
            'end': item['end_time'],
            'class_type': item['class_type']
        })

    cursor.close()

    return attends

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

    for item in cursor:
        print item

    #### need to finish

    



