import os
from flask import request, jsonify
from app import app, mongo

ROOT_PATCH = os.environ.get('ROOT_PATCH')

@app.route('/usuario/inicio', methods = ['GET'])
def inicio():
    if request.method == 'GET':
        data = mongo.db.usuarios.find({})
        lista = list(data)
        if data == None:
            data =[]
        return jsonify({'transacción':True, 'data':lista})
