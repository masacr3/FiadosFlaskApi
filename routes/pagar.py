from flask import Blueprint, request, jsonify
from .secrets import secrets_for_pagar
import uuid

pagar_bp = Blueprint('pagar', __name__)

def init_pagar_bp(db, User):

    @pagar_bp.route('/reset', methods=['POST'])
    def full_reset():
        data = request.get_json()
        secreto_from_front = data.get('secreto')
        if secreto_from_front == secrets_for_pagar():
            db.update({"pagos" : []}, User.pagos.exists())
            return jsonify({"mensaje" : "Se ha reseteado DB pagar"}), 200
        else:
            return jsonify({"error" : "no tiene los permisos nesesarios para esta operacion"}), 403


    @pagar_bp.route('', methods=['GET'])
    def obtener_todos_los_pagos():
        listaDePagos = db.get(User.pagos.exists())
        return jsonify(listaDePagos), 200
    

    @pagar_bp.route('', methods=['POST'])
    def agregar_pago_del_usuario():
        data = request.get_json()
        interfaz = ['id', 'nombre', 'deuda_total', 'pago_del_usuario' , 'fecha']
        values = [ data.get(item) for item in interfaz if data.get(item) ]
        check = len(values) == len(interfaz)
        if check:
            # usuario_existe = db.get(doc_id = data.get('id'))
            # if not usuario_existe or usuario_existe['nombre'] != data.get('nombre'):
            #     return jsonify({'error':'Bad Request', 'mesaje':'usuario no existe en su base de datos'}), 400
            
            usuarios = db.get(User.usuarios.exists())['usuarios']
            usuario = None
            for u in usuarios:
                if u['id'] == data.get('id') and u['nombre'] == data.get('nombre'):
                    usuario = u
                    break
            
            if not usuario:
                return jsonify({'error':'Bad Request', 'mesaje':'usuario no existe en su base de datos'}), 400

            pagos = db.get(User.pagos.exists())['pagos']
            pago = {}
            for k, value in zip(interfaz, values):
                pago[k] = value

            pago['tiket'] = str(uuid.uuid4())
            pagos.append(pago)
            db.update({"pagos" : pagos}, User.pagos.exists())
            
            return jsonify({'mensaje':'Pago realizado'}), 201

        else:
            return jsonify({'error': 'DTO no compatible'}), 400
        
    
    return pagar_bp