import os
import google.generativeai as genai
import json
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify


load_dotenv()

# 2. Вземаме ключа от системната среда
api_key = os.getenv("GEMINI_API_KEY")

# 3. Конфигурираме Gemini
genai.configure(api_key=api_key)

scenes_bp = Blueprint('scenes_bp', __name__)

# Сложи твоя ключ тук
genai.configure(api_key)

def gemini_extract_params(user_description):
    model = genai.GenerativeModel('models/gemini-flash-lite-latest')
    
    
    prompt = f"""
    Analyze this room description for an acoustic simulation app: "{user_description}"
    Return ONLY a JSON object with these keys:
    - audio_purpose (string: vocal, music, or speech)
    - room_size_m2 (integer: suggested size in square meters)
    - reverb_type (string: dry, studio, or hall)
    - complexity (integer 1-10: based on the description)
    - materials (list of 3 strings: e.g., ["wood", "foam", "concrete"])
    
    Do not use any markdown formatting or extra words. Just the JSON.
    """

    response = model.generate_content(prompt)

    clean_text = response.text.strip().replace('```json', '').replace('```', '')
    return json.loads(clean_text)

@scenes_bp.route('/generate-scene', methods=['POST'])
def generate_scene():
    try:
        
        description = request.form.get('description')
        label = request.form.get('label')

        if not description:
            return jsonify({"error": "No description provided"}), 400

        # Питаме Gemini
        ai_data = gemini_extract_params(description)

        # Връщаме резултата обратно
        return jsonify({
            "status": "success",
            "scene_name": label,
            "ai_logic": ai_data
        }), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "AI Engine failed to respond"}), 500