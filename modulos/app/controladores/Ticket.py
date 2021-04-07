from flask import request, jsonify
from modulos.app import app, mongo
import os

#VARIABLES

ROOT_PATCH = os.environ.get('ROOT_PATCH')

@app.route('/detalle/caso/<string:ticket>', methods = ['GET'])
def detalleTicket(ticket):
    if request.method == 'GET':
        data = mongo.db.tickets.find({'ticket_id': ticket})
        lista = list(data)
        if data == None:
            data =[]
        return jsonify({'transacción':True,'message':'Consula exitosa(detalle)', 'data':lista})