from flask import request, jsonify
from modulos.app import app, mongo
import os

#VARIABLES

ROOT_PATCH = os.environ.get('ROOT_PATCH')

@app.route('/ticket', methods = ['GET'])
def data():
    if request.method == 'GET':
        dat = mongo.db.tickets.find({})
        lista = list(dat)
        if dat == None:
            return jsonify({'transacción':True, 'message':'No hay datos en la coleccion solicitada', 'data':lista})
        return jsonify({'transacción':True, 'message':'Consulta exitosa', 'data':lista})
