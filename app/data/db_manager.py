import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import bcrypt
from models.Audio import Audio
from models.User import User


db_params = {
        "dbname": "ACUSTICA",
        "user": "postgres",
        "password": "123abc456",
        "host": "localhost"
    }



def get_db_connection():
  
  

    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except Exception as e:
        print(f"Грешка при връзка с базата: {e}")
        return None




def create_user_in_db(user_data, hashed_pw):
    # Данните за връзка (най-добре е да са в .env файл, но за сега тук)
    db_params = {
        "dbname": "ACUSTICA",
        "user": "postgres",
        "password": "123abc456",
        "host": "localhost"
    }

    try:
        # Използваме 'with', за да гарантираме затваряне на връзката
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
         
                query = """
                    INSERT INTO users (username, email, password_hash, first_name, last_name, age)
                    VALUES (%s, %s, %s, %s, %s, %s) 
                    RETURNING id;
                """
                
                cur.execute(query, (
                    user_data.username,
                    user_data.email,
                    hashed_pw,
                    user_data.first_name,
                    user_data.last_name,
                    user_data.age
                ))
                
                # Вземаме върнатото ID
                user_id = cur.fetchone()[0]
                
                # commit-ът става автоматично заради 'with conn'
                return user_id

    except Exception as e:
        print(f"Критична грешка при запис в базата: {e}")
        return None



def get_user_by_email(email):
    
    # Използваме RealDictCursor, за да получим резултата като речник (dict)
    conn = get_db_connection() # Твоята функция за свързване
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        return user
    except Exception as e:
        print(f"Грешка при търсене: {e}")
        return None
    finally:
        cur.close()
        conn.close()


def get_user_by_id(id):

   conn = get_db_connection() 
   cur = conn.cursor(cursor_factory=RealDictCursor)
    
   try:
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        user_dict = cur.fetchone() # Това е речникът
        
        if user_dict:
            # ТУК Е МАГИЯТА:
            # **user_dict разпакетира речника и го подава на класа User
            return User(**user_dict) 
            
        return None
   except Exception as e:
        print(f"Грешка при търсене: {e}")
        return None
   finally:
        cur.close()
        conn.close() # this needs fixing 



def verify_password(plain_password, hashed_password):
    # Сравняваме чистия текст от формата с хеша от базата
    # plain_password идва от Input-а, hashed_password идва от Postgres
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))






def addScene(sceneData):

    query = "INSERT INTO scenes (audio_id, scene_label, room_settings, user_id)" \
                "VALUES (%s, %s, %s, %s)" \
                "RETURNING id;"
    

  

def addAudioFile(audio_file_name, audio_url, curr_user):



    Audio_Curr = Audio(
        user=curr_user, 
        file_name=audio_file_name, 
        file_path=audio_url
    )

    # 2. Дефинираме заявката правилно (3 колони = 3 стойности)
    query = """
        INSERT INTO audio_files (file_name, file_path, user_id)
        VALUES (%s, %s, %s)
        RETURNING id;
    """

    try:
        # Използваме context manager за връзката и курсора
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                # Подаваме точно 3 параметъра в кортежа
                cur.execute(query, (
                    Audio_Curr.file_name,
                    Audio_Curr.file_path,
                    Audio_Curr.user.id  # Вземаме ID-то от вложения обект
                ))
                
                # Вземаме генерираното ID от RETURNING клаузата
                result = cur.fetchone()
                
                if result:
                    audio_file_id = result[0]
                    # С 'with' блок commit-ът става автоматично при успех
                    print(f"Успешен запис! Audio ID: {audio_file_id}")
                    return audio_file_id
                
        return None

    except Exception as e:
        # Ако тук гръмне, значи или няма такава колона, или връзката е прекъснала
        print(f"Критична грешка при запис в базата: {e}")
        # Тук е добре да помислиш за rollback, но 'with' го прави вместо теб
        return None