# This module is responsible for executing all database tasks and queries.

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

