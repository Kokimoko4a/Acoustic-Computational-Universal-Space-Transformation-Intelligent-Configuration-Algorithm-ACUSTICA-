import json
import google.generativeai as genai

class SceneGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-flash-lite-latest')

    def create_3d_file_content(self, scene_data):
        """
        Тази функция кара AI да генерира структурата на 3D сцената.
        Резултатът ще бъде записан като .json файл в облака.
        """
        settings = scene_data.get('settings', {})
        
        prompt = f"""
        Create a 3D scene definition for a room with:
        - Area: {settings.get('room_size_m2')} m2
        - Materials: {settings.get('materials')}
        - Purpose: {settings.get('audio_purpose')}
        
        Return a JSON representing the 3D world (coordinates, objects, scales).
        This JSON will be saved as a file and loaded by the 3D engine.
        """
        
        response = self.model.generate_content(prompt)
        # Чистим текста от евентуални ```json тагове
        return response.text.strip().replace('```json', '').replace('```', '')

# Пример как ще го ползваш:
# generator = SceneGenerator(YOUR_API_KEY)
# file_content = generator.create_3d_file_content(data_from_db)
# upload_to_cloud(file_content, "scene_123.json")