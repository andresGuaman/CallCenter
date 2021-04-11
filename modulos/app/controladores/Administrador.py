from modulos.app.controladores.Usuarios import DOMINIO_CORREO_ISTA, validar_email, validar_nombres, validar_password
from flask import request, jsonify
from modulos.app import app, mongo
import os

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

@app.route('/administrador/crear-admin', methods=['POST'])
def crear_admin():
    data = request.get_json()
    response = validar_admin(data)
    if response[0]:
      guardar = mongo.db.administradores.insert_one(data)
      return jsonify({"transaccion":True, "mensaje":"los datos se crearon correctamente"})
    else:
        return jsonify({'transaccion':False, 'mensaje':"Erros validacion usuario"})  

def validar_admin(data)->tuple:

    if validar_emailAdmin(data.get('correo')) == False:
        return (False, 'Correo Incorrecto')

    if validar_nombres([data.get('nombre'), data.get('apellido')]) == False:
        return (False, 'Nombre o apellido incorrecto')

    if validar_password(data.get('password')) == False:
        return (False, 'Contraseña Incorrecta')

    if validar_rol(data.get('rol')) == False:
        return (False, "Rol Incorrecto")    
    
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
        if correo.strip() and len(correo) >= 17 and len(correo) < 75 and correo.count('@') == 1:

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



@app.route('/administrador/update-admin/{idadmin}', methods=['POST'])
def update_admin():
    data = request.get_json()
    actualizar = mongo.db.administradores.update(data)
    return jsonify({"trnsaccion":True, "mensaje":"se actualizaron los datos correctamente"})

@app.route('/administrador/delete-admin/{idadmin}', methods=['GET'])
def delete_admin():
    data = request.get_json()
    eliminar = mongo.db.administradores.delete_one(data)
    return jsonify({"transaccion":True, "mensaje":"eliminado correctamente"})

