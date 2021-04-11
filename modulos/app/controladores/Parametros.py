from flask import request, jsonify
from modulos.app import app, mongo
import os

ROOT_PATCH = os.environ.get('ROOT_PATCH')

@app.route('/catalogo/ver', methods = ['GET'])
def listar():
    if request.method == 'GET':
        data = mongo.db.catalogos.find({})
        lista = list(data)
    return jsonify({'transacción':True,'message':'Consula exitosa', 'data':lista})

@app.route('/catalogo/nuevo', methods = ['POST'])
def nuevo():
    if request.method == 'POST':
        data = request.get_json()
        save = mongo.db.catalogos.insert_one(data)
        return jsonify({'transacción':True,'message':'Consula exitosa', 'data':list(data)})

@app.route('/catalogo/nuevo/estado_administrador', methods = ['POST'])
def estado_administrador():
    if request.method == 'POST':
        data = request.get_json()
        respu = clasi(data)
        if respu[0] == True:
            return jsonify({'Correcto':True, 'message':respu[1]})
        else:
            return jsonify({'Correcto':True, 'message':respu[1]})



def clasi(data) -> tuple:
    if data.get('prioridad_ticket') or data.get('tipo_caso') or data.get('estado_ticket') or data.get('estado_administrador') or data.get('rol_administrador'):
        if data.get('prioridad_ticket'):
            prioridad = data.get('prioridad_ticket')
            pri = mongo.db.catalogos.update({},{"$push":{"prioridad_ticket":{"$each":prioridad}}})

        if data.get('tipo_caso'):
            caso = data.get('tipo_caso')
            ca = mongo.db.catalogos.update({},{"$push":{"tipo_caso":{"$each":caso}}})

        if data.get('estado_ticket'):
            ticket = data.get('estado_ticket')
            tic = mongo.db.catalogos.update({},{"$push":{"estado_ticket":{"$each":ticket}}})

        if data.get('estado_administrador'):
            est_admin = data.get('estado_administrador')
            ad = mongo.db.catalogos.update({},{"$push":{"estado_administrador":{"$each":est_admin}}})

        if data.get('rol_administrador'):
            rol = data.get('rol_administrador')
            ro = mongo.db.catalogos.update({},{"$push":{"rol_administrador":{"$each":rol}}})

        return (True, "Exito")
    else:
        return(False, "sin datos")
