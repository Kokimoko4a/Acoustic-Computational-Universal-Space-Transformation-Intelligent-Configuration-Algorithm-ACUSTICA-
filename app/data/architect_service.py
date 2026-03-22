import json
import time
import requests
import tempfile
import os
import google.generativeai as genai

class SceneGenerator:
    """
    Професионален генератор за Acustica AI.
    Анализира аудио записи (локални или от URL) и текстови параметри, 
    за да създаде прецизен 3D модел.
    """
    def __init__(self, api_key):
        # Конфигуриране на Google AI SDK
        genai.configure(api_key=api_key)
        
        # Използваме пълното системно име на модела, за да избегнем 404 грешки в v1beta
        self.model_name = 'models/gemini-flash-lite-latest'
        self.model = genai.GenerativeModel(self.model_name)

    def create_3d_file_content(self, scene_data, audio_source=None):
        """
        Основен метод за генериране на 3D сцена.
        audio_source може да бъде локален път или URL (напр. от Cloudinary).
        """
        settings = scene_data.get('settings', {})
        room_name = scene_data.get('name', 'Unnamed Scene')
        
        prompt_parts = []
        temp_file_path = None

        # 1. ОБРАБОТКА НА АУДИО (Локален файл или URL)
        if audio_source:
            try:
                # Проверка дали източникът е URL
                if audio_source.startswith(('http://', 'https://')):
                    print(f"Система: Изтегляне на аудио от облака: {audio_source}")
                    response = requests.get(audio_source, stream=True, timeout=30)
                    response.raise_for_status()
                    
                    # Създаваме временен файл по сигурен начин
                    suffix = os.path.splitext(audio_source.split('?')[0])[1] or ".mp3"
                    fd, temp_file_path = tempfile.mkstemp(suffix=suffix)
                    
                    try:
                        with os.fdopen(fd, 'wb') as tmp:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    tmp.write(chunk)
                        upload_path = temp_file_path
                    except Exception as e:
                        os.close(fd)
                        raise e
                else:
                    upload_path = audio_source

                # Качваме файла в Google AI Studio
                print(f"Система: Качване на файл в Google AI за анализ...")
                audio_file = genai.upload_file(path=upload_path)
                
                # Експоненциално изчакване за обработка
                print("Система: Изчакване на AI анализ на звука...")
                while audio_file.state.name == "PROCESSING":
                    time.sleep(3)
                    audio_file = genai.get_file(audio_file.name)
                
                if audio_file.state.name == "FAILED":
                    raise Exception("AI обработката на аудио файла беше неуспешна.")

                prompt_parts.append(audio_file)
                audio_context = (
                    "СЛУШАЙ внимателно прикаченото аудио. Анализирай акустичните параметри: "
                    "реверберация (RT60), честотен диапазон и ехо. Определи реалните размери "
                    "на помещението и материалите на повърхностите въз основа на звука."
                )
            except Exception as e:
                audio_context = f"Предупреждение: Проблем с аудиото ({str(e)}). Генериране само по текст."
                print(f"Грешка при подготовка на аудио: {e}")
            finally:
                # Почистване на временния файл
                if temp_file_path and os.path.exists(temp_file_path):
                    try:
                        os.remove(temp_file_path)
                        print("Система: Временният файл е изтрит.")
                    except Exception as e:
                        print(f"Предупреждение: Неуспешно изтриване: {e}")
        else:
            audio_context = "Няма предоставено аудио. Генерирай сцената по стандартни изчисления."

        # 2. ТЕХНИЧЕСКИ ПРОМПТ
        main_prompt = f"""
        Act as a Senior Acoustic Engineer and 3D Architect.
        Scene Title: {room_name}
        
        INPUT DATA:
        - Target Area: {settings.get('room_size_m2', 20)} m2
        - Desired Materials: {settings.get('materials', [])}
        - Complexity: {settings.get('complexity', 10)}/50
        - Audio Analysis Instruction: {audio_context}

        ENGINE RULES:
        1. Precise Math: Width * Depth MUST be approximately {settings.get('room_size_m2')} m2.
        2. Acoustic Design: 
           - 'audio_source': Place it at the coordinates where the sound seems to originate.
           - 'acoustic_panel': If you hear excessive echo, place these on the walls.
           - 'pillar': Add structural pillars if complexity > 30.
        3. Materials: Map to rendering materials like 'wood', 'concrete', 'fabric', 'glass', 'brick'.

        OUTPUT SPECIFICATION:
        Return ONLY a raw JSON object.
        {{
            "metadata": {{ 
                "name": "{room_name}", 
                "audio_report": "Твоят анализ на акустиката на български",
                "rt60_estimate_ms": int 
            }},
            "geometry": {{ "width": float, "height": float, "depth": float }},
            "entities": [
                {{
                    "type": "wall|floor|ceiling|pillar|audio_source|acoustic_panel",
                    "position": {{ "x": float, "y": float, "z": float }},
                    "rotation": {{ "x": float, "y": float, "z": float }},
                    "scale": {{ "x": float, "y": float, "z": float }},
                    "material": "string"
                }}
            ]
        }}
        """
        prompt_parts.append(main_prompt)

        # 3. ГЕНЕРИРАНЕ
        try:
            response = self.model.generate_content(prompt_parts)
            return self._sanitize_output(response.text.strip())
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})

    def _sanitize_output(self, text):
        """Извлича чист JSON от отговора на модела."""
        if "```" in text:
            parts = text.split("```")
            for part in parts:
                if "{" in part and "}" in part:
                    text = part
                    if text.strip().startswith("json"):
                        text = text.strip()[4:]
                    break
        return text.strip()