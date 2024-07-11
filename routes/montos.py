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
            usuario_existe = db.get(doc_id = data.get('id'))
            print(usuario_existe)
            if not usuario_existe or usuario_existe['nombre'] != data.get('nombre'):
                return jsonify({'error': 'Bad Request', 'mesaje': 'usuario no existe en su base de datos'}), 400
             
            usuario = usuario_existe
            nuevoMonto = usuario['monto'] + data.get('monto')
            db.update({'monto' : nuevoMonto}, doc_ids=[data.get('id')])
            return jsonify({'mensaje':'Monto actualizado'}), 201

        else:
            return jsonify({'error': 'Bad Request', 'mesaje': 'nombre requerido'}), 400

    @montos_bp.route('/<int:id>/<string:nombre>', methods=['PUT'])
    def modificar_monto_existente_del_cliente(id, nombre):
        usuario = db.get(doc_id = id)
        if not usuario or usuario['nombre'] != nombre:
            return jsonify({"message" : "el usuario no existe en su Base de datos"}), 400

        if request.is_json:
            data = request.get_json()
            nuevosMontos = data.get('monto', [])
            db.update({'monto' : nuevosMontos}, doc_ids=[id])
            return jsonify({"message" : "Montos recividos y actualizados"}), 200
        return jsonify({"error" : "Invalido"}), 400


    
    return montos_bp