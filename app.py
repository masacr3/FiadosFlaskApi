from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db
from routes.usuarios import init_usuarios_bp
from routes.montos import init_montos_bp
#from routes.objetivos import init_objetivos_bp

app = Flask(__name__)

# Configurar CORS para permitir solo un origen específico en todas las rutas
CORS(app)

# Inicializar TinyDB
db, user = init_db()

usuarios_bp = init_usuarios_bp(db, user)
montos_bp = init_montos_bp(db,user)
#objetivos_bp = init_objetivos_bp(db, user)

app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(montos_bp, url_prefix='/montos')
#app.register_blueprint(objetivos_bp, url_prefix='/objetivos')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)