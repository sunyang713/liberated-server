# This module is responsible for executing all database tasks and queries.
from flask import g
from sqlalchemy import exc

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

# def get_attends(first_name, last_name, start, end):
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

# crashes on empty input for rx_male and rx_female

# def insert_workout(w_name, description, rx_male, rx_female, level):
#     if not rx_male:
#         rx_male = None
#     if not rx_female:
#         rx_female = None
#     try: 
#         cursor = g.conn.execute(
#             """
#             INSERT INTO workouts (w_name, description, rx_male, rx_female, level)
#                 VALUES ('{w_name}', '{description}', '{rx_male}', '{rx_female}', '{level}');
#             """
#             .format(
#                 w_name = w_name,
#                 description = description,
#                 rx_male = rx_male,
#                 rx_female = rx_female,
#                 level = level
#             )
#         )
#     except exc.SQLAlchemyError:
#         pass

def insert_workout(w_name, description, rx_male, rx_female, level):
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