import os
import google.generativeai as genai
import json
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
import jwt
from data import db_manager


load_dotenv()

# 2. Вземаме ключа от системната среда
api_key = os.getenv("GEMINI_API_KEY")

# 3. Конфигурираме Gemini
genai.configure(api_key=api_key)


cloudinary.config(
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
  api_key = os.getenv("CLOUDINARY_API_KEY"),
  api_secret = os.getenv("CLOUDINARY_API_SECRET")
)

scenes_bp = Blueprint('scenes_bp', __name__)


def gemini_extract_params(user_description):
    model = genai.GenerativeModel('models/gemini-flash-lite-latest')
    
    prompt = f"""
    Analyze this room description for an acoustic simulation app: "{user_description}"
    Return ONLY a JSON object with these keys:
    - audio_purpose (string: vocal, music, or speech)
    - room_size_m2 (integer: suggested size in square meters)
    - reverb_type (string: dry, studio, or hall)
    - complexity (integer 1-50: based on the description)
    - materials (list of strings)
    
    IMPORTANT: Return only valid JSON. No markdown, no comments.
    """

    try:
        response = model.generate_content(prompt)
        
        # Почистване на текста
        text_content = response.text.strip()
        
        # Махаме евентуални markdown тагове, които моделът може да сложи
        if "```json" in text_content:
            text_content = text_content.split("```json")[1].split("```")[0].strip()
        elif "```" in text_content:
            text_content = text_content.split("```")[1].strip()

        # Превръщаме в истински Python речник
        data = json.loads(text_content)
        return data

    except Exception as e:
        print(f"AI Analysis Error: {e}")
        # Връщаме дефолтни данни, ако AI се провали, за да не гърми приложението
        return {
            "audio_purpose": "speech This is default data something is not ok!!!!!!!",
            "room_size_m2": 20,
            "reverb_type": "studio",
            "complexity": 10,
            "materials": ["plaster", "carpet"]
        } #this fucntion is for tesing the Gemini AI and the adding the audio to the DB
 


@scenes_bp.route('/generate-scene', methods=['POST'])
def generate_scene():
    try:
     
        label = request.form.get('label')
        description = request.form.get('description')
        audio_file = request.files.get('audio')
        user_token = request.form.get('user_id')

       
        

        user_id = get_user_id_from_token(user_token)

        User = db_manager.get_user_by_id(user_id)



        print(f"Качване на аудио: {audio_file.filename}...")
        audio_upload = cloudinary.uploader.upload(audio_file, resource_type="video", folder="acustica/audio")
        audio_url = audio_upload['secure_url']

        Audio =  db_manager.addAudioFile(audio_file.name, audio_url, User )
     

        ai_data = gemini_extract_params(description)


        room_id = db_manager.addScene(Audio, label, ai_data, User)

        return jsonify({
            "status": "success",
            "scene_name": label,
            "audio_url": audio_url,
            # "model_url": model_url, when we start to create the 3d models we will add them to the cloudinary 
            "ai_logic": ai_data,
            "audio_id": Audio.id
        }), 201

    except Exception as e:
        print(f"Грешка: {e}")
        return jsonify({"error": str(e)}), 500
    





def get_user_id_from_token(token):
    try:
        
        payload = jwt.decode(token, "19012007", algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return "Expired" # Токенът е изтекъл
    except jwt.InvalidTokenError:
        return "Invalid" # Токенът е невалиден