from modulos.app.controladores.Usuarios import DOMINIO_CORREO_ISTA, validar_email, validar_nombres, validar_password
from flask import request, jsonify
from modulos.app import app, mongo
from bson.objectid import ObjectId
import os
import re

ROOT_PATCH = os.environ.get('ROOT_PATH')

@app.route('/administrador/listar', methods = ['GET'])
def listar_admin():
    
    if request.method == 'GET':

        data = mongo.db.administradores.find({})
    
        if data and data != None:
            return jsonify({"transaccion":True, 'mensaje':'Transacción exitosa','data':list(data)})
        else:
            return jsonify({"transaccion":False, 'mensaje':'Error de transacción', "data":[]})

@app.route('/administrador/login/<string:data>', methods=['GET'])
def login_admin(data):
    if request.method == 'GET':
        salida = mongo.db.administradores.find({"correo":"'"+data+"'"})
        print(str(salida))
        if salida:
            return jsonify({'transaccion':True, 'mensaje':"el usuario  existe"})    
        else:
            return jsonify({'transaccion':False, 'mensaje':"el usuario no existe"})             

@app.route('/administrador/guardar/<string:action>', methods=['POST'])
def crear_admin(action):

    print (action)

    if action == 'insert':

        data = request.get_json()
        response = validar_admin(data, action)

        if response[0]:
            mongo.db.administradores.insert_one(data)
            return jsonify({"transaccion":True, "mensaje":"Administrador creado correctamente", 'data':data})
        else:
            return jsonify({'transaccion':False, 'mensaje':response[1], 'data':[]})

    if action == 'update':

        data = request.get_json()
        response = validar_admin(data, action)

        if response[0]:
            mongo.db.administradores.update_one(
            {
                '_id': ObjectId(data.get('_id'))
            }, 
            {
                '$set': {
                    "usuario": data.get('usuario'),
                    "correo": data.get('correo'),
                    "nombre": data.get('nombre'),
                    "apellido": data.get('apellido'),
                    "password": data.get('password'),
                    "foto": "",
                    "rol": data.get('rol'),
                    "estado": data.get('estado'),
                }
            })

            return jsonify({"transaccion":True, "mensaje":"Administrador editado correctamente", 'data':data})
        else:
            return jsonify({'transaccion':False, 'mensaje':response[1], 'data':[]})

@app.route('/administrador/eliminar', methods=['POST'])
def delete_admin():

    if request.method == 'POST':
        data = request.get_json()

        if data != None:

            data['_id'] = ObjectId(data.get('_id'))
            mongo.db.administradores.delete_one(data)
            return jsonify({"transaccion":True, "mensaje":"Administrador eliminado correctamente", 'data':data})

#METHODS

def validar_admin(data, action: str)->tuple: #El parámetro action es para saber si se va a insertar o actualizar al administrador

    if validar_emailAdmin(data.get('correo')) == False:
        return (False, 'Correo Incorrecto')

    if validar_nombres([data.get('nombre'), data.get('apellido')]) == False:
        return (False, 'Nombre o apellido incorrecto')

    if validar_password(data.get('password')) == False:
        return (False, 'Contraseña Incorrecta')

    if validar_rol(data.get('rol')) == False:
        return (False, "Rol Incorrecto")

    if validar_usuario(data.get('usuario'), action) == False:
        return (False, "Usuario Incorrecto o repetido")
    
    return (True, 'Datos correctos')

def validar_rol(rol: str) -> bool:
    if rol:
        if rol.strip() and rol.lower() == "administrador" or rol.lower() == "soporte":
            return True
        else:
            return False
    else:
        return False

def validar_emailAdmin(correo: str) -> bool:
    if correo:
        REGEX = r'^(\w|[\.-])+@(\w|[-])+(\.[a-zA-Z]+){1,2}$'

        if re.match(REGEX, correo):
            return True
        else:
            return False
    else:
        return False

def validar_usuario(usuario: str, action: str) -> bool:

    if usuario:

        user_repplaced = usuario.replace('_', 'a').replace('.', 'a').replace('-', 'a')

        if user_repplaced.isalnum() and len(usuario) >= 5 and len(usuario) <= 30:
        
            if action == 'insert':

                user_mongo = mongo.db.administradores.find({'usuario':usuario})

                if user_mongo:
                    return False
                else:
                    return True

            else:
                return True
        else:
            return False
        
    else:
        return False