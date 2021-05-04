from bson.objectid import ObjectId
from dns.rdatatype import NULL
from flask import request, jsonify
from modulos.app import app, mongo
import os
import io
from datetime import datetime
from botocore import client
import boto3
import base64

#VARIABLES
ACCES_KEY=""
SECRET_KEY=""
bucket_name="callcenters3"

from botocore import UNSIGNED
from botocore.client import Config
from botocore.exceptions import ClientError

client = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
client._request_signer.sign = (lambda *args, **kwargs:None)


ROOT_PATCH = os.environ.get('ROOT_PATCH')

@app.route('/detalle/tickets/', methods = ['GET'])
def consultotal():
    if request.method == 'GET':
        dat = mongo.db.tickets.find({})
        lista = list(dat)
        if dat == None:
            return jsonify({'transacción':True, 'message':'No hay datos en la coleccion solicitada', 'data':lista})
        return jsonify({'transacción':True, 'message':'Consulta exitosa', 'data':lista})    


@app.route('/detalle/correo/<string:correo>', methods = ['GET'])
def consultacorreo(correo):
    if request.method == 'GET':
        print(correo)
        dat = mongo.db.tickets.find({"usuario_email":correo})
        lista = list(dat)
        if dat == None:
            return jsonify({'transacción':True, 'message':'No hay datos en la coleccion solicitada', 'data':lista})
        return jsonify({'transacción':True, 'message':'Consulta exitosa', 'data':lista})    

@app.route('/detalle/tipocaso/<string:tipo_caso>', methods = ['GET'])
def consultatipocaso(tipo_caso):
    if request.method == 'GET':
        dat = mongo.db.tickets.find({"tipo_caso":tipo_caso})
        lista = list(dat)
        if dat == None:
            return jsonify({'transacción':True, 'message':'No hay datos en la coleccion solicitada', 'data':lista})
        return jsonify({'transacción':True, 'message':'Consulta exitosa', 'data':lista})    

@app.route('/detalle/estado/<string:estado>', methods = ['GET'])
def consultaestado(estado):
    if request.method == 'GET':
        dat = mongo.db.tickets.find({"estado":estado})
        lista = list(dat)
        if dat == None:
            return jsonify({'transacción':True, 'message':'No hay datos en la coleccion solicitada', 'data':lista})
        return jsonify({'transacción':True, 'message':'Consulta exitosa', 'data':lista})    


@app.route('/detalle/ticket/<string:ticket>', methods = ['GET'])
def detalleTicket(ticket):
    if request.method == 'GET':
        data = mongo.db.tickets.find({'ticket_id': ticket})
        lista = list(data)
        if data == None:
            data =[]
        return jsonify({'transacción':True,'message':'Consula exitosa(detalle)', 'data':lista})
    
@app.route('/detalle/caso/<string:correo>', methods = ['GET'])
def data(correo):
    if request.method == 'GET':
        print(correo)
        dat = mongo.db.tickets.find({"usuario_email":correo})
        lista = list(dat)
        if dat == None:
            return jsonify({'transacción':True, 'message':'No hay datos en la coleccion solicitada', 'data':lista})
        return jsonify({'transacción':True, 'message':'Consulta exitosa', 'data':lista})
    
@app.route('/ticket/crear-ticket', methods=['POST'])
def crear_ticket():
    data=request.get_json()
    guardar = mongo.db.tickets.insert_one(data)
    transformarimagen(data["_id"],data["imagenes"])
    turno_ticket(data["tipo_caso"], data["_id"])
    fecha(data["_id"],data["fecha"])
    return jsonify({"transaccion":True, "mensaje":"ticket creado"})

def transformarimagen(idticket, imagen):
    idticketactua = str(idticket)
    imagenarray=imagen
    imagen1 = str(imagenarray[0])
    imagen2 = str(imagenarray[1])
    imagen3 = str(imagenarray[2])
    
    for i in range(4):
        if(i==1):
            if(imagen1==NULL):
               nombre1 = " sin imagen"
            else:    
                posicion1 = imagen1.find("4,")
                posicion15 = imagen1.find("]")
                imagenbase64 = imagen1[posicion1+1:posicion15-1]
                urlImagen1 = base64.b64decode(imagenbase64.encode('utf-8').strip())
                idticketactua1 = "IMG1"+idticketactua
                cargarIMG(urlImagen1,idticketactua1)
                nombre1 = idticketactua1
        if(i==2):
            if(imagen2==NULL):
               nombre2 = " sin imagen"
            else:
                posicion2 = imagen2.find("4,")
                posicion25 = imagen2.find("]")
                imagenbase642 = imagen2[posicion2+1:posicion25-1]
                urlImagen2 = base64.b64decode(imagenbase642.encode('utf-8').strip())
                idticketactua2 = "IMG2"+idticketactua
                cargarIMG(urlImagen2,idticketactua2)
                nombre2 = idticketactua2
        if(i==3):
            if(imagen3==NULL):
               nombre3 = " sin imagen"
            else:
                posicion3 = imagen3.find("4,")
                posicion35 = imagen3.find("]")
                imagenbase643 = imagen3[posicion3+1:posicion35-1]
                urlImagen3 = base64.b64decode(imagenbase643.encode('utf-8').strip())
                idticketactua3 = "IMG3"+idticketactua
                cargarIMG(urlImagen3,idticketactua3)
                nombre3 = idticketactua3    
    
    actualiza = mongo.db.tickets.update({"_id":idticket},{'$set':{"imagenes":[[nombre1+".jpeg"],[nombre2+".jpeg"],[nombre3+".jpeg"]]}})  


def cargarIMG(ruta,nombreimagen):
    ruta = io.BytesIO(ruta)
    client.upload_fileobj(ruta, bucket_name, "Ticket/"+nombreimagen+".jpeg",
          ExtraArgs={'ACL':'public-read'})

def fecha(idticket, fechafial):
    fechafin1 = fechafial
    fech2 = datetime.strptime(fechafin1,'%m-%d-%Y %H:%M:%S %p')
    fechas = mongo.db.tickets.update({"_id":idticket},{'$set':{"fecha":fech2}})  


def turno_ticket(tipo_caso, idturno):
    encontrado = 0
    identifiCaso =tipo_caso[0:3].upper()
    contar = mongo.db.tickets.find({'tipo_caso':tipo_caso,'estado':"Abierto"}).count()
    total = mongo.db.tickets.find().count()
    totalF = int(total)
    for i in range(totalF):
        busquedaid = mongo.db.tickets.find_one({'tipo_caso':tipo_caso,'estado':"Abierto",'ticket_id':identifiCaso+"-"+str(i).zfill(6)})
        if busquedaid:
            print("correcto"+str(encontrado))
        else:
            encontrado = i 
            actualiza = mongo.db.tickets.update_one({"_id":idturno},{'$set':{"ticket_id":identifiCaso+"-"+str(i).zfill(6)}}) 
            break
            
              
    return jsonify({'conteo':contar})    

@app.route('/ticket/casos-abiertos', methods=['GET'])
def casos_abiertos():
    
    if request.method == 'GET':

        data = mongo.db.tickets.find({'estado':'Abierto'})

        if data and data != None:
            return jsonify({"transaccion":True, 'mensaje':'Petición correcta','data':list(data)})
        else:
            return jsonify({"transaccion":False, 'mensaje':'No se pudieron cargar los datos', "data":[]})

@app.route('/ticket/asignarme/<string:ticket_id>/<string:usuario>')
def asignarme(ticket_id, usuario):

    if request.method == 'GET' and ticket_id and usuario:

        responsable = mongo.db.administradores.find_one({'usuario':usuario})

        if responsable:

            data = mongo.db.tickets.update_one(
                {
                    '_id': ObjectId(ticket_id)
                },
                {
                    '$addToSet':
                    {
                        'responsable': usuario
                    },
                    '$set':
                    {
                        'estado':'Asignado'
                    }
                })

            return jsonify({"transaccion":True, "mensaje":"Asignado", 'data':[]})
        return jsonify({"transaccion":False, "mensaje":"No asignado", 'data':[]}) 
    return jsonify({"transaccion":False, "mensaje":"No Asignado", 'data':[]})