"""
This module is responsible for executing all database tasks and queries.
"""

from liberated import engine
from flask import g, jsonify

# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#     id serial,
#     name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")

def get_users():
    # a database query
    # conn.execute returns a "ResultProxy." See http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.ResultProxy
    # Basically it's a pseudo data structure that holds the 'table' you just retrieved.
    # You can iterate over the rows with a for-loop and transform it to a manageable python-native data structure.
    # But careful, each element is still of type 'schema.Column' (SQLAlchemy), so you need to deconstruct further.
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
    print type(first_name)
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

