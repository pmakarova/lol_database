import psycopg2
from config import load_config

def drop_tables():
    commands = (
    """DROP TABLE IF EXISTS team_composition CASCADE""",
    """DROP TABLE IF EXISTS champion_summoner CASCADE""",
    """DROP TABLE IF EXISTS team CASCADE""",
    """DROP TABLE IF EXISTS match CASCADE""",
    """DROP TABLE IF EXISTS ability CASCADE""",
    """DROP TABLE IF EXISTS skin CASCADE""",
    """DROP TABLE IF EXISTS lore CASCADE""",
    """DROP TABLE IF EXISTS champion CASCADE""",
    """DROP TABLE IF EXISTS summoner CASCADE""",
    """DROP TABLE IF EXISTS spell CASCADE""",
    """DROP TABLE IF EXISTS map CASCADE""",
    """DROP TABLE IF EXISTS rarity CASCADE""",
    """DROP TABLE IF EXISTS champion_class CASCADE"""
    )
    try:
        config = load_config()
        connection = psycopg2.connect(**config)
        crsr = connection.cursor()
        for command in commands:
            crsr.execute(command)
        connection.commit()
    except(psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == "__main__":

    drop_tables()