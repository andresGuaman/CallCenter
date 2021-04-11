from modulos.app import app, mongo
from flask import Flask, jsonify, request, session
from passlib.hash import pbkdf2_sha256

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signout(self):
    session.clear()
    return 'sesión cerrada'
  
  def login(self):
    user = {
      "correo": request.get_json(),
      "password": request.get_json()
    }

    '''correo = mongo.db.usuarios.find_one({
      "correo": email
    })
    password = mongo.db.usuarios.find_one({
      "password": passw
    })'''

    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    user = mongo.db.usuarios.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.get_json('password'), user['password']):
      #return self.start_session(correo)
      return jsonify({ "sesion": "correcta" })
    
    return jsonify({ "error": "Credenciales Incorrecta" }), 401