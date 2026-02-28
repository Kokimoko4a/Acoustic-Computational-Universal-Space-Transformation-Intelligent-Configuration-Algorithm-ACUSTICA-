from flask import Blueprint, request, jsonify
import jwt
import datetime
from data.db_manager import create_user_in_db, get_user_by_email, verify_password
from models.User import User 
import bcrypt

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    # 1. Вземаме данните от лилавата форма
    raw_data = request.get_json()
    
    # 1. Пълно изчистване - оставяме САМО това, което моделът 100% иска
    # (Предполагам това са твоите полета в User модела)
    clean_data = {
        "username": raw_data.get("username"),
        "email": raw_data.get("email"),
        "first_name": raw_data.get("first_name"),
        "last_name": raw_data.get("last_name"),
        "age": raw_data.get("age")
        
    }

    password_raw = raw_data.pop('password', None)
    
    # 2. Валидираме с Pydantic (Твоят модел с exclude=True)
    try:
        new_user = User(**clean_data)
    except Exception as e:
        return f"Грешка в данните: {e}", 400

    # 3. Хешираме паролата точно тук
    password_bytes = password_raw.encode('utf-16') # или utf-8
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    # 4. Пращаме към базата
    user_id = create_user_in_db(new_user, hashed_pw)

    payload = {
        'user_id': user_id, # Вземи реалното ID от базата
        'exp': datetime.datetime.now() + datetime.timedelta(hours=24) # Валиден 24 часа
    }
    
    token = jwt.encode(payload, "19012007", algorithm='HS256')
    
    return jsonify({
        "message": "Потребителят е създаден",
        "access_token": token
    }), 201

@user_bp.route('/login', methods=['POST'])
def login():

    raw_data = request.get_json();
    clean_data = {

        "email" : raw_data.get("email"),
        "password" : raw_data.get("password")
    }



    user = get_user_by_email(clean_data['email'])

    hashed_password_from_db_as_bytes = user['password_hash'].encode('utf-8')

    input_password_bytes = clean_data['password'].encode('utf-16')

    test = user['id']

    if bcrypt.checkpw(input_password_bytes, hashed_password_from_db_as_bytes):
        # Паролата е вярна! Генерираш JWT токен
        payload = {
            'user_id': user['id'],
            'exp': datetime.datetime.now() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, "19012007", algorithm='HS256')
        
        return jsonify({
            "message": "Успешен вход",
            "access_token": token
        }), 200
    else:
        # Грешна парола
        return jsonify({"message": "Невалидни данни за достъп"}), 401
    
   
        



    
    