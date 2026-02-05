import psycopg2

def add_user(username = 'kaloyan.rusev', email = 'kaloyan@abv.bg', first_name = 'Kaloyan', last_name = 'Rusev', age = 19):
    try:
        # 1. Отваряме връзката
        connection = psycopg2.connect(
            host="localhost",
            database="ACUSTICA",
            user="postgres",
            password="123abc456",
            port="5432"
        )
        
        cursor = connection.cursor()

        # 2. Подготвяме SQL заявката
        # Използваме %s за сигурност (предпазва от SQL Injection)
        insert_query = "INSERT INTO users (username, email,first_name, last_name, age) VALUES (%s, %s, %s, %s, %s);"
        record_to_insert = (username, email , first_name, last_name, age)

        # 3. Изпълняваме командата
        cursor.execute(insert_query, record_to_insert)

        # 4. КРИТИЧНА СТЪПКА: commit()
        # В PostgreSQL промените не се записват автоматично. 
        # Трябва да потвърдиш, че искаш да ги запазиш.
        connection.commit()

        print(f"Потребител {username} беше добавен успешно!")

    except Exception as e:
        print(f"Възникна грешка: {e}")
    finally:
        # Винаги затваряме връзката, дори ако е имало грешка
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # Пробвай да добавиш себе си
    add_user("Koki", "koki@example.com")