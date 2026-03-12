import os
import google.generativeai as genai
import json
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
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
    - materials (list as you percieve)
    
    Do not use any markdown formatting or extra words. Just the JSON.
    """

    response = model.generate_content(prompt)

    clean_text = response.text.strip().replace('```json', '').replace('```', '')
    return json.loads(clean_text) #this fucntion is for tesing the Gemini AI and the adding the audio to the DB
 


@scenes_bp.route('/generate-scene', methods=['POST'])
def generate_scene():
    try:
     
        label = request.form.get('label')
        description = request.form.get('description')
        audio_file = request.files.get('audio')

        #here add the user id retrieveing from the front end and test again because in the db you save the publisher id in the audio file table in the DB
        

        print(f"Качване на аудио: {audio_file.filename}...")
        audio_upload = cloudinary.uploader.upload(audio_file, resource_type="video", folder="acustica/audio")
        audio_url = audio_upload['secure_url']

        audio_id =  db_manager.addAudioFile(audio_file.name, audio_url, )
        

        ai_data = gemini_extract_params(description)

        return jsonify({
            "status": "success",
            "scene_name": label,
            "audio_url": audio_url,
            # "model_url": model_url, when we start to create the 3d models we will add them to the cloudinary 
            "ai_logic": ai_data,
            "audio_id": audio_id
        }), 201

    except Exception as e:
        print(f"Грешка: {e}")
        return jsonify({"error": str(e)}), 500