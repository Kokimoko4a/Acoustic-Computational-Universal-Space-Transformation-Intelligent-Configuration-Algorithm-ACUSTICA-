import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask
from flask_cors import CORS 
from routes.user_routes import user_bp
from routes.scenes_routes import scenes_bp


app = Flask(__name__)

# 2. Активирай CORS за ця
CORS(app) 

app.register_blueprint(user_bp)
app.register_blueprint(scenes_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)




    