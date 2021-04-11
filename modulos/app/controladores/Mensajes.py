from flask import request, jsonify
from modulos.app import app, mongo
import os

#VARIABLES

ROOT_PATCH = os.environ.get('ROOT_PATCH')

@app.route('/detalle/mensajes/<string:ticket>', methods = ['GET'])
def detallemensajes(ticket):
    if request.method == 'GET':
        data = mongo.db.mensajes.find({'ticket_id': ticket})

        #data = mongo.db.mensajes.aggregate([{'$match': {'ticket_id':ticket}},{'$group':{'_id':'$emisor','contenido':{'$push':'$mensaje'},'imagen':{'$push': '$imagen'}}},{'$sort':{'fecha':-1}}])
        lista = list(data)
        if data == None:
            data =[]
        return jsonify({'transacción':True,'message':'Consula exitosa(mensajes)', 'data':lista})


@app.route('/mensajes/chat', methods = ['POST'])
def insertMensajes():
    if request.method == 'POST':
        data = request.get_json()
        datos = {"ticket_id":data.get('ticket_id'), 
            "fecha":data.get('fecha'), "mensaje":data.get('mensaje'), 
            "imagen":data.get('imagen'), "emisor":data.get('emisor')}
        if datos != 0:
            save = mongo.db.mensajes.insert_one(datos)
            return jsonify({'transaccion':True, 'message':"Consulta Exitosa",'data':list(datos)})
        else:
            return jsonify({'transaccion':False, 'message':"Error al guardar" ,'data':list(datos)})
