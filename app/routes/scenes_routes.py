from flask import Blueprint, request, jsonify


scene_bp = Blueprint('scene', __name__)


def extract_scene_parameters(text):
    text = text.lower()
    
    # Дефинираме база данни с ключови думи (настройки)
    # Тези Key-Value двойки ще се попълват според думите в текста
    params = {
        "audio_type": "general",      # Музика, говор, шум
        "audience_type": "standard",  # Публика: малка, голяма, професионалисти
        "vibe": "neutral",            # Атмосфера: суха, ехтяща, интимна
        "room_scale": "medium"        # Мащаб: малък, огромен
    }

    # Първичен анализ (Keyword Extraction)
    if any(word in text for word in ["концерт", "рок", "оркестър", "свири"]):
        params["audio_type"] = "musical_performance"
        params["room_scale"] = "large"
    
    if any(word in text for word in ["подкаст", "лекция", "говор"]):
        params["audio_type"] = "speech"
        params["room_scale"] = "small"
        params["vibe"] = "dry"

    if "много" in text or "голяма" in text or "публика" in text:
        params["audience_type"] = "crowded"
    
    if "ехо" in text or "катедрала" in text:
        params["vibe"] = "reverberant"

    return params


@scene_bp.route('/createScene', methods=['POST'])
def createScene():
    raw_data = request.get_json();
#in the future we will integrate AI for the dictionary creating



