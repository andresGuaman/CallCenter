from modulos.app import app, mongo
from flask import request, jsonify, session
from bson.objectid import ObjectId

import os

#VARIABLES

ROOT_PATCH = os.environ.get('ROOT_PATCH')
DOMINIO_CORREO_ISTA = '@tecazuay.edu.ec'

@app.route('/usuario/correo/<string:dato>', methods = ['GET'])
def inicio(dato):
    if request.method == 'GET':
        data = mongo.db.usuarios.find({'correo':dato})
        lista = list(data)
        if data == None:
            data =[]
        return jsonify({'transacción':True,'message':'Consula exitosa', 'data':lista})

@app.route('/usuario/password/<email>/<string:passw>', methods = ['GET'])
def login_pass(email, passw):
    if request.method == 'GET':
        data = mongo.db.usuarios.find_one({'correo':email, 'password':passw})
        if data:
            return jsonify({'transacción':True,'message':'Login Correcto', 'data':passw})
        else:
            return jsonify({'transacción':False,'message':'Contraseña incorrecta', 'data':passw})

@app.route('/usuario/eliminar', methods=['POST'])
def delete_usuario():
    if request.method == 'POST':
        data = request.get_json()
        if data != None:
            data['_id'] = ObjectId(data.get('_id'))
            mongo.db.usuarios.delete_one(data)
            return jsonify({"transaccion":True, "mensaje":"Usuario eliminado correctamente", 'data':data})


@app.route('/usuario/list', methods = ['GET'])
def listar_user():
    
    if request.method == 'GET':

        data = mongo.db.usuarios.find({})
    
        if data and data != None:
            return jsonify({"transaccion":True, 'mensaje':'Transacción exitosa','data':list(data)})
        else:
            return jsonify({"transaccion":False, 'mensaje':'Error de transacción', "data":[]})

@app.route("/usuario/update/<string:email>",  methods=['POST'])
def update_one(email):
    
    if request.method == 'POST':
        data = request.get_json()
        result = mongo.db.usuarios.update({'correo': email}, {'correo': email, 'nombre':data.get('nombre'),
        'apellido': data.get('apellido'), 'password':data.get('password')})
        if result: 
            return jsonify({'transaccion':True, 'message':"Modificacion Exitosa",'data':list(data)})
        else:
            return jsonify({'transaccion':False, 'message':"Error al editar" ,'data':list(data)})



@app.route('/usuario/crear', methods = ['POST'])
def create():
    if request.method == 'POST':
        data = request.get_json()
        response = validar_usuario(data)
        if response[0] == True:
            save = mongo.db.usuarios.insert_one(data)
            return jsonify({'transaccion':True, 'message':response[1] ,'data':list(data)})
        else:
            return jsonify({'transaccion':False, 'message':response[1] ,'data':list(data)})


#Validaciones

def validar_usuario(data) -> tuple:
    if data.get('correo'):
        if validar_email(data.get('correo')) == False:
            return (False, 'Correo incorrecto')
    else:
        return (False, 'Correo Vacio')
    if data.get('nombre') and data.get('apellido'):
        if validar_nombres([data.get('nombre'), data.get('apellido')]) == False:
            return (False, 'Nombres incorretos')
    else:
        return (False, 'Nombres vacíos')
    if data.get('password'):
        if validar_password(data.get('password') == False):
            return (False, 'Contraseña incorrecta')
    else:
        return (False, 'Contraseña vacío')
    return (True, 'Datos correctos')


def validar_nombres(nombres: list) -> bool:
    if nombres[0] and nombres[1]:

        for n in nombres:
            if n.strip() and n.isalpha() and n.count(' ') < 1:
                response = True
            else:
                response = False

        return response
    else:
        return False

def validar_email(correo: str) -> bool:
    if correo:
        if correo.strip() and len(correo) >= 17 and len(correo) < 75 and correo.endswith(DOMINIO_CORREO_ISTA) and correo.count('@') == 1:
            try:
                start_email = correo.split('@')[0]
                if start_email.replace('.','').isalpha():
                    return True
                else:
                    return False
            except Exception:
                return False
        else:
            return False
    else:
        return False

def validar_password(password: str) -> bool:

    if password:
        if password.strip() and len(password) > 8 and len(password) < 50:
            return True
        else:
            return False
    else:
        return False
