import psycopg2
from config import load_config  

def insert_data(sql, data):
    connection = None
    try:
        params = load_config()
        connection = psycopg2.connect(**params)
        crsr = connection.cursor()

        # crsr.execute("SHOW client_encoding;")
        encoding = crsr.fetchone()[0]
        # print(f"Current client encoding: {encoding}")

        if encoding != 'UTF8':
            connection.set_client_encoding('UTF8')
            print("Forced client encoding to UTF8")

        crsr.executemany(sql, data)
        connection.commit()

        print("[DEBUG] Data inserted successfully!")
        return True
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"[ERROR] {error}")
        return False
    finally:
        if crsr:
            crsr.close()
        if connection:
            connection.close()