from flask import request, jsonify
from modulos.app import app, mongo
import os

#VARIABLES

ROOT_PATCH = os.environ.get('ROOT_PATCH')
DOMINIO_CORREO_ISTA = '@tecazuay.edu.ec'

@app.route('/usuario/lista', methods = ['GET'])
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
        response = validar_usuario(data)

        if response[0]:
            save = mongo.db.usuarios.insert_one(data)
            return jsonify({'transaccion':True, 'message':response[1] ,'data':list(data)})
        else:
            return jsonify({'transaccion':False, 'message':response[1] ,'data':list(data)})

#Validaciones

def validar_usuario(data) -> tuple:

    if validar_email(data.get('correo')) == False:
        return (False, 'Correo incorrecto')

    if validar_nombres([data.get('nombre'), data.get('apellido')]):
        return (False, 'Nombre o apellido incorreto')

    if validar_password(data.get('password')):
        return (False, 'Contraseña incorrecta')

    return (True, 'Datos correctos')

def validar_nombres(nombres: list) -> bool:

    if list[0] and list[1]:

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