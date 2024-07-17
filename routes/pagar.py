from flask import Blueprint, request, jsonify
import uuid

pagar_bp = Blueprint('pagar', __name__)

def init_pagar_bp(db, User):

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
            usuario_existe = db.get(doc_id = data.get('id'))
            if not usuario_existe or usuario_existe['nombre'] != data.get('nombre'):
                return jsonify({'error':'Bad Request', 'mesaje':'usuario no existe en su base de datos'}), 400
            
            pago = {}
            pagos = db.get(User.pagos.exists())['pagos']

            print(pagos)

            for k, value in zip(interfaz, values):
                pago[k] = value
            
            # Generar un UUID4
            unique_id = uuid.uuid4()

            # Convertir el UUID a una cadena
            unique_id_str = str(unique_id)

            pago['tiket'] = unique_id_str

            pagos.append(pago)

            db.update({"pagos" : pagos}, User.pagos.exists())
            
            return jsonify({'mensaje':'Pago realizado'}), 201

        else:
            return jsonify({'error': 'DTO no compatible'}), 400
        
    
    return pagar_bp