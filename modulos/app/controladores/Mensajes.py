from flask import request, jsonify
from modulos.app import app, mongo
import os

#VARIABLES

ROOT_PATCH = os.environ.get('ROOT_PATCH')

@app.route('/detalle/mensajes/<string:ticket>', methods = ['GET'])
def detallemensajes(ticket):
    if request.method == 'GET':
        data = mongo.db.mensajes.find({'ticket_id': ticket})
        lista = list(data)
        if data == None:
            data =[]
        return jsonify({'transacción':True,'message':'Consula exitosa(mensajes)', 'data':lista})