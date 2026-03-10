import os
import google.generativeai as genai
import json
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify


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
    - materials (list as you percieve)
    
    Do not use any markdown formatting or extra words. Just the JSON.
    """

    response = model.generate_content(prompt)

    clean_text = response.text.strip().replace('```json', '').replace('```', '')
    return json.loads(clean_text) #this fucntion is for tesing the Gemini AI



@scenes_bp.route('/generate-scene', methods=['POST'])
def generate_scene():
    try:
        # 1. Вземаме данните от формата
        label = request.form.get('label')
        description = request.form.get('description')
        audio_file = request.files.get('audio')
        
        # 2. Качваме аудиото в Cloudinary
        # Използваме resource_type="video", защото Cloudinary така третира аудиото
        print(f"Качване на аудио: {audio_file.filename}...")
        audio_upload = cloudinary.uploader.upload(audio_file, resource_type="video", folder="acustica/audio")
        audio_url = audio_upload['secure_url']

        # 3. ТУК ЩЕ СЕ ГЕНЕРИРА 3D МОДЕЛА (засега може да е просто пример)
        # Ако имаш готов файл на диска, качваш го като "raw"
        # model_upload = cloudinary.uploader.upload("path/to/model.glb", resource_type="raw", folder="acustica/models")
        # model_url = model_upload['secure_url']

        # 4. Викаме Gemini за параметрите
        # (използваме функцията gemini_extract_params, която вече написахме)
        ai_data = gemini_extract_params(description)

        # 5. Връщаме всичко към фронтенда
        return jsonify({
            "status": "success",
            "scene_name": label,
            "audio_url": audio_url,
            # "model_url": model_url,
            "ai_logic": ai_data
        }), 201

    except Exception as e:
        print(f"Грешка: {e}")
        return jsonify({"error": str(e)}), 500