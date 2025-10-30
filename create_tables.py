import psycopg2
from config import load_config

def create_tables():
    commands = (
        """
        CREATE TABLE champion_class(
            id SERIAL PRIMARY KEY,
            class VARCHAR(15) NOT NULL,
            class_description VARCHAR(1024) NOT NULL 
        );
        """,
        """
        CREATE TABLE champion(
            id SERIAL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            class INTEGER NOT NULL,
            champion_description VARCHAR(256) NOT NULL,
            difficulty INTEGER NOT NULL,
            release_date DATE NOT NULL,
            FOREIGN KEY (class) REFERENCES champion_class(id) 
            ON UPDATE CASCADE ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE lore(
            id SERIAL PRIMARY KEY,
            champion_name INTEGER NOT NULL,
            title VARCHAR(128) NOT NULL,
            text VARCHAR(512) NOT NULL,
            text_length INTEGER NOT NULL,
            FOREIGN KEY (champion_name) REFERENCES champion(id) 
            ON UPDATE CASCADE ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE summoner(
            id SERIAL PRIMARY KEY,
            nickname VARCHAR(128) NOT NULL,
            level INTEGER NOT NULL,
            registration_date DATE NOT NULL,
            honor INTEGER NOT NULL
        );
        """,
        """
        CREATE TABLE spell(
            id SERIAL PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            reloading INTEGER NOT NULL,
            spell_description VARCHAR(256) NOT NULL
        );
        """,
        """
        CREATE TABLE rarity(
            id SERIAL PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            rarity_description VARCHAR(256) NOT NULL,
            another_form BOOLEAN DEFAULT FALSE
        );
        """,
        """
        CREATE TABLE skin(
            id SERIAL PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            champion INTEGER NOT NULL,
            rarity_type INTEGER NOT NULL,
            another_form BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (champion) REFERENCES champion(id),
            FOREIGN KEY (rarity_type) REFERENCES rarity(id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE ability(
            id VARCHAR(64) PRIMARY KEY NOT NULL,
            name VARCHAR(128) NOT NULL,
            ability_description VARCHAR(256) NOT NULL,
            champion INTEGER NOT NULL,
            cost_burn VARCHAR(128) NOT NULL,
            FOREIGN KEY (champion) REFERENCES champion(id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE map(
            id SERIAL PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            map_description VARCHAR(256) NOT NULL,
            lanes_count INTEGER NOT NULL
        );
        """,
        """
        CREATE TABLE match(
            id SERIAL PRIMARY KEY,
            map INTEGER NOT NULL,
            patch DOUBLE PRECISION NOT NULL,
            duration INTEGER NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY (map) REFERENCES map(id) 
            ON UPDATE CASCADE ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE team(
            team_id SERIAL PRIMARY KEY,
            match_id INTEGER NOT NULL,
            team_type BOOLEAN NOT NULL,
            FOREIGN KEY (match_id) REFERENCES match(id) 
            ON UPDATE CASCADE ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE champion_summoner(
            champion_id INTEGER NOT NULL,
            summoner_id INTEGER NOT NULL,
            champion_level INTEGER NOT NULL,
            PRIMARY KEY (champion_id, summoner_id),
            FOREIGN KEY (champion_id) REFERENCES champion(id),
            FOREIGN KEY (summoner_id) REFERENCES summoner(id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE team_composition(
            team_id INTEGER NOT NULL,
            champion_id INTEGER NOT NULL,
            summoner_id INTEGER NOT NULL,
            spell1_id INTEGER NOT NULL,
            spell2_id INTEGER NOT NULL,
            PRIMARY KEY (team_id, champion_id, summoner_id),
            FOREIGN KEY (team_id) REFERENCES team(team_id), 
            FOREIGN KEY (champion_id, summoner_id) REFERENCES champion_summoner(champion_id, summoner_id),
            FOREIGN KEY (spell1_id) REFERENCES spell(id),
            FOREIGN KEY (spell2_id) REFERENCES spell(id)   
            ON UPDATE CASCADE ON DELETE CASCADE
        );
        """,
        
    )
    try:
        params = load_config()
        connection = psycopg2.connect(**params)
        crsr = connection.cursor()
        for command in commands:
            crsr.execute(command)
            print("Table created successfully.")
        connection.commit()
    except(psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        if crsr:
            crsr.close()
        if connection:
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    create_tables()