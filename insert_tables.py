import psycopg2
from config import load_config  

def insert_data(sql, data):
    connection = None
    crsr = None
    try:
        params = load_config()
        connection = psycopg2.connect(**params)
        crsr = connection.cursor()

        # 🔍 ОТЛАДКА: вставляем по одной строке чтобы видеть ошибку
        for i, row in enumerate(data):
            try:
                crsr.execute(sql, row)
            except Exception as e:
                print(f"❌ ОШИБКА в строке {i}:")
                print(f"   Данные: {row}")
                print(f"   Ошибка: {e}")
                # Покажем типы данных
                print(f"   Типы: {[type(x) for x in row]}")
                raise  # повторно выбрасываем исключение
        
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