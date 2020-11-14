import sqlalchemy
import os

# PostgreSQL settings
inv_vars = os.environ
username = inv_vars['username']
password = inv_vars['password']
host = inv_vars['host']
port = '5432'
database = inv_vars['database']
db_url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(username, password, host, port, database)


def getConnection():
    engine = sqlalchemy.create_engine(db_url)
    return engine.connect()