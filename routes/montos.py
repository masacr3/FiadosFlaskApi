from flask import Blueprint, request, jsonify

montos_bp = Blueprint('montos', __name__)

def init_montos_bp(db, User):

    @montos_bp.route('', methods=['POST'])
    def agregar_monto_al_usuario():
        data = request.get_json()
        interfaz = ['id','nombre','monto']
        values = [data.get(item) for item in interfaz if data.get(item)]
        check = len(values) == len(interfaz)
        if check:
            usuarios = db.get(User.usuarios.exists())['usuarios']
            usuario = None
            for u in usuarios:
                if u['id'] == data.get('id') and u['nombre'] == data.get('nombre'):
                    usuario = u
                    break
            
            if not usuario:
                return jsonify({'error': 'Bad Request', 'mesaje': 'usuario no existe en su base de datos'}), 400
             
            usuario['monto'] += data.get('monto')
            db.update({'usuarios' : usuarios}, User.usuarios.exists())
            return jsonify({'mensaje':'Monto actualizado'}), 201

        else:
            return jsonify({'error': 'Bad Request', 'mesaje': 'nombre requerido'}), 400

    @montos_bp.route('/<string:id>/<string:nombre>', methods=['PUT'])
    def modificar_monto_existente_del_cliente(id, nombre):
        usuarios = db.get(User.usuarios.exists())['usuarios']
        usuario = None
        for u in usuarios:
            if u['id'] == id and u['nombre'] == nombre:
                usuario = u
                break

        if not usuario or usuario['nombre'] != nombre:
            return jsonify({"message" : "el usuario no existe en su Base de datos"}), 400

        if request.is_json:
            data = request.get_json()
            nuevosMontos = data.get('monto', [])
            usuario['monto'] = nuevosMontos
            db.update({'usuarios' : usuarios}, User.usuarios.exists())
            return jsonify({"message" : "Montos recividos y actualizados"}), 200
        return jsonify({"error" : "Invalido"}), 400


    
    return montos_bp