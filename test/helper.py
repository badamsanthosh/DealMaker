from django.db import connection


def get_database_name():
    return connection.get_connection_params()['database']
