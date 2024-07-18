from flask import Blueprint, request, jsonify
import uuid

usuarios_bp = Blueprint('usuarios', __name__)

def init_usuarios_bp(db, User):
    @usuarios_bp.route('', methods=['POST'])
    def agregar_usuario():
        data = request.get_json()
        usuario = {}
        interfaz = ['nombre']
        values = [data.get(item).lower() for item in interfaz if data.get(item)]
        check = len(values) == len(interfaz)
        if check:
            for k, value in zip(interfaz, values):
                usuario[k] = value
            
            usuarios = db.get(User.usuarios.exists())['usuarios']
            usuario['id'] = str(uuid.uuid4())
            usuario['monto'] = []
            usuarios.append(usuario)
            db.update({"usuarios" : usuarios}, User.usuarios.exists())

            return jsonify({'mensaje':'Usuario agregado'}), 201

        else:
            return jsonify({'error': 'Bad Request', 'mesaje': 'nombre requerido'}), 400
        

    @usuarios_bp.route('', methods=['GET'])
    def obtener_usuarios():
        usuarios = db.get(User.usuarios.exists())
        return jsonify(usuarios), 200
    
    return usuarios_bp