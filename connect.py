import psycopg2
from config import load_config


def connect(config):
    try:
        print('Connecting to the postgreSQL database...')
        connection = psycopg2.connect(**config)
        return connection
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
if __name__ == "__main__":
    config = load_config()
    connect(config)