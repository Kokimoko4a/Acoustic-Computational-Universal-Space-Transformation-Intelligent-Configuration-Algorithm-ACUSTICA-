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



    def generate_plan(self, scene_data, scene_label): # THIS NEEDS TESTING

        settings = scene_data
        room_name = scene_label

        prompt = f"""
        You are a professional acoustic engineer and architect.

        Scene: {room_name}

        INPUT:
        - Target Area: {settings.get('room_size_m2', 20)} m2
        - Materials: {settings.get('materials', [])}
        - Complexity: {settings.get('complexity', 10)}/50

        TASK:
        Create a REALISTIC engineering plan.

        REQUIREMENTS:

        1. DIMENSIONS:
        - Must NOT be square (avoid equal width/depth)
        - width * depth ≈ target area (±5%)
        - height between 2.5 and 3.2
        - use realistic ratios (e.g. 1 : 1.4 : 0.6)

        2. ACOUSTIC ANALYSIS:
        - estimate RT60
        - identify problems (echo, bass buildup, reflections)

        3. SOLUTIONS:
        - specify EXACT number of:
            - acoustic panels
            - bass traps
        - explain placement logic

        4. PLACEMENT STRATEGY:
        - where is audio source
        - where are reflection points
        - where are bass traps (corners!)

        OUTPUT JSON ONLY:

        {{
            "dimensions": {{
                "width": float,
                "depth": float,
                "height": float
            }},
            "acoustic": {{
                "rt60_estimate": int,
                "issues": [string],
                "solutions": {{
                    "acoustic_panels": int,
                    "bass_traps": int
                }}
            }},
            "placement_strategy": {{
                "audio_source_position": "string",
                "panel_placement": "string",
                "bass_traps": "string"
            }}
        }}
        """

        response = self.model.generate_content(prompt)
        return self._sanitize_output(response.text) # THIS NEED TESTING


  