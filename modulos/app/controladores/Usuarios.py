from flask import request, jsonify
from modulos.app import app, mongo
import os

ROOT_PATCH = os.environ.get('ROOT_PATCH')

@app.route('/usuario/inicio', methods = ['GET'])
def inicio():
    if request.method == 'GET':
        data = mongo.db.usuarios.find({})
        lista = list(data)
        if data == None:
            data =[]
        return jsonify({'transacción':True, 'data':lista})

@app.route('/usuario/crear', methods = ['POST'])
def create():

    if request.method == 'POST':
        
        data = request.get_json()
        save = mongo.db.usuarios.insert_one(data)

        print (data)
        
        if valicacion_ususario(data):
            return jsonify({'transaccion':True, 'message':'User created successfully' ,'data':list(data)})
        else:
            return jsonify({'transaccion':False, 'message':'Datos Incorrectos' ,'data':list(data)})

#Validaciones

def valicacion_ususario(data):

    return True
