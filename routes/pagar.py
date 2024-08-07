from flask import Blueprint, request, jsonify
from .secrets import secrets_for_pagar
import uuid

pagar_bp = Blueprint('pagar', __name__)

def init_pagar_bp(db, User):

    @pagar_bp.route('/reset', methods=['POST'])
    def full_reset():
        data = request.get_json()
        secreto_from_front = data.get('secreto')
        if secrets_for_pagar and (secreto_from_front == secrets_for_pagar()):
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
        interfaz = ['id', 'nombre', 'deuda_total', 'pago_del_usuario' , 'fecha', 'monto']
        values = [ data.get(item) for item in interfaz if data.get(item) ]
        check = len(values) == len(interfaz)
        if check:
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

            total = pago['deuda_total'] - pago['pago_del_usuario']
            
            #actualizo el total del usuario
            usuario['monto'] = [] if total <= 0 else [total] 
            db.update({'usuarios':usuarios}, User.usuarios.exists())
            
            return jsonify({'mensaje':'Pago realizado'}), 201

        else:
            return jsonify({'error': 'DTO no compatible'}), 400
        
    
    return pagar_bp
