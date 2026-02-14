from flask import Blueprint, request, jsonify
import jwt
import datetime
# ПРЕМАХНИ "ACUSTICA.app" от началото
from data.db_manager import create_user_in_db
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
    
    