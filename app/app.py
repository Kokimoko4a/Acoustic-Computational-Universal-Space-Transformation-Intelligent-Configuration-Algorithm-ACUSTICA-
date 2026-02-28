import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask
from flask_cors import CORS # 1. Внеси това
from routes.user_routes import user_bp
from routes.scenes_routes import scene_bp


app = Flask(__name__)

# 2. Активирай CORS за цялото приложение
CORS(app) 

app.register_blueprint(user_bp)
app.register_blueprint(scene_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)




    