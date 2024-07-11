from flask import Blueprint, request, jsonify

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
            usuario_existe = db.get(doc_id=data.get('id'))
            if usuario_existe:
                return jsonify({'error': 'Bad Request', 'mesaje': 'nombre ya existe en su base de datos'}), 409
             
            for k, value in zip(interfaz, values):
                usuario[k] = value
            usuario['tabla'] = 'usuarios'
            usuario['monto'] = []
            db.insert(usuario)
            return jsonify({'mensaje':'Usuario agregado'}), 201

        else:
            return jsonify({'error': 'Bad Request', 'mesaje': 'nombre requerido'}), 400
        

    @usuarios_bp.route('', methods=['GET'])
    def obtener_usuarios():
        usuarios = db.search(User.tabla == 'usuarios')
        for user in usuarios:
            user['id'] = user.doc_id
        return jsonify(usuarios), 200
    
    return usuarios_bp