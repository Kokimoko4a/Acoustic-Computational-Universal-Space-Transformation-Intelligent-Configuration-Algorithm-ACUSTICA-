import psycopg2
from psycopg2 import sql

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