import json
import google.generativeai as genai

class SceneGenerator:
    
    def __init__(self, api_key):
        
        genai.configure(api_key=api_key)
        
        
        self.model = genai.GenerativeModel('models/gemini-flash-lite-latest')
        

    def create_3d_file_content(self, scene_data):
        
       
        settings = scene_data.get('settings', {})
        room_name = scene_data.get('name', 'Unnamed Scene')
        
       
        prompt = f"""
        Act as a 3D Graphics Engine Architect. Generate a scene definition for: {room_name}.
        
        DATABASE PARAMETERS:
        - Total Area: {settings.get('room_size_m2')} square meters
        - Materials: {settings.get('materials', [])}
        - Complexity Level: {settings.get('complexity', 10)} (from 1 to 50)
        - Reverb/Acoustics: {settings.get('reverb_type', 'hall')}

        YOUR TASK:
        Create a 3D scene layout. Return ONLY a raw JSON object (no markdown, no talk).
        
        THE JSON STRUCTURE MUST BE:
        {{
            "metadata": {{ "name": "{room_name}", "version": "1.1" }},
            "geometry": {{
                "width": float, 
                "height": float, 
                "depth": float
            }},
            "entities": [
                {{
                    "type": "wall|floor|ceiling|pillar|audio_source",
                    "position": {{ "x": float, "y": float, "z": float }},
                    "rotation": {{ "x": float, "y": float, "z": float }},
                    "scale": {{ "x": float, "y": float, "z": float }},
                    "material": "string"
                }}
            ]
        }}

        ENGINE REQUIREMENTS:
        1. Coordinate System: Y is Up. Set floor position at y=0.
        2. Math: Calculate width and depth so that (width * depth) equals approximately {settings.get('room_size_m2')}.
        3. Logic: If complexity > 30 (yours is {settings.get('complexity')}), add support pillars along the perimeter.
        4. Audio: Place one "audio_source" entity at a logical location (e.g., center of the room).
        """
        
        try:
            
            response = self.model.generate_content(prompt)
            
            
            content = response.text.strip()
            
        
            if "```" in content:
                
                lines = content.split("```")
                for line in lines:
                    if "{" in line and "}" in line:
                        content = line
                        if content.startswith("json"):
                            content = content[4:]
                        break
            
            return content.strip()
            
        except Exception as e:
        
            return json.dumps({
                "status": "error",
                "message": f"Грешка при генериране: {str(e)}"
            })