from bson.objectid import ObjectId
from dns.rdatatype import NULL
from flask import request, jsonify
from modulos.app import app, mongo
import os

#VARIABLES

ROOT_PATCH = os.environ.get('ROOT_PATCH')

@app.route('/detalle/ticket/<string:ticket>', methods = ['GET'])
def detalleTicket(ticket):
    if request.method == 'GET':
        data = mongo.db.tickets.find({'ticket_id': ticket})
        lista = list(data)
        if data == None:
            data =[]
        return jsonify({'transacción':True,'message':'Consula exitosa(detalle)', 'data':lista})

@app.route('/ticket/crear-ticket', methods=['POST'])
def crear_ticket():
    data=request.get_json()
    guardar = mongo.db.tickets.insert_one(data)
    turno_ticket(data["tipo_caso"], data["_id"])
    return jsonify({"transaccion":True, "mensaje":"ticket creado"})


def turno_ticket(tipo_caso, idturno):
    encontrado = 0
    identifiCaso =tipo_caso[0:3]
    contar = mongo.db.tickets.find({'tipo_caso':tipo_caso,'estado':"Abierto"}).count()
    total = mongo.db.tickets.find().count()
    totalF = int(total)
    for i in range(totalF):
        busquedaid = mongo.db.tickets.find_one({'tipo_caso':tipo_caso,'estado':"Abierto",'ticket_id':identifiCaso+"-"+str(i).zfill(6)})
        if busquedaid:
            print("creo q esta bien"+str(encontrado))
        else:
            encontrado = i 
            actualiza = mongo.db.tickets.update_one({"_id":idturno},{'$set':{"ticket_id":identifiCaso+"-"+str(i).zfill(6)}}) 
            print(str(i).zfill(6))
            break
            
              
    return jsonify({'conteo':contar})    

