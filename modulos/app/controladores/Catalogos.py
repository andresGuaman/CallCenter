from flask import request, jsonify
from modulos.app import app, mongo
import os

ROOT_PATCH = os.environ.get('ROOT_PATH')

@app.route('/catalogos/catalogos-listas', methods = ['GET'])
def listar_admin():
    if request.method == 'GET':
        salida = mongo.db.catalogos.find({})
        lista = list(salida)
        print(str(lista))
        if salida == None:
            salida = []
        return jsonify({"transaccion":True, "data":lista})
 
        