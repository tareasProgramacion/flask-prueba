from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
mongo = MongoClient('localhost',27017)
bd = mongo.CristhianBonillaDB
@app.route('/',methods=['GET'])
def index():
  
  return render_template('index.html',data={'a':1})


@app.route('/usuario',methods=['GET','POST'])
def usuario():
  data = {}
  if request.method == 'POST':
    usuario = {}
    usuario['cedula'] = request.form['cedula']
    usuario['nombre'] = request.form['nombre']
    usuario['apellido'] = request.form['apellido']
    if len(usuario['cedula']) != 10:
      data['mensaje'] = 'La cédula debe tener 10 dígitos'
      data['color'] = 'danger'
    else:
      bd.usuarios.insert_one(usuario)
      data['mensaje'] = 'Usuario agregado'
      data['color'] = 'success'
  data['usuarios'] = cargarUsuarios()
  return render_template('usuario.html',data=data)

@app.route('/usuario/editar/<id>',methods=['GET','POST'])
def usuarioEditar(id):
  data = {}
  if request.method == 'POST':
    usuario = {}
    usuario['cedula'] = request.form['cedula']
    usuario['nombre'] = request.form['nombre']
    usuario['apellido'] = request.form['apellido']
    if len(usuario['cedula']) != 10:
      data['mensaje'] = 'La cédula debe tener 10 dígitos'
      data['color'] = 'danger'
    else:
      bd.usuarios.update_one({'_id':ObjectId(id)},{
        '$set':{
          'cedula': request.form['cedula'],
          'nombre': request.form['nombre'],
          'apellido': request.form['apellido']
        }
      })
      data['mensaje'] = 'Usuario editado'
      data['color'] = 'success'
  else:
    data['usuario'] = bd.usuarios.find_one({'_id':ObjectId(id)})
    data['usuario']['_id'] = str(data['usuario']['_id'])
  data['usuarios'] = cargarUsuarios()
  return render_template('usuario.html',data=data)

@app.route('/usuario/eliminar/<id>',methods=['GET'])
def usuarioEliminar(id):
  bd.usuarios.delete_one({'_id':ObjectId(id)})
  return redirect('/usuario')

def cargarUsuarios():
  lista = []
  for i in bd.usuarios.find():
    i['_id'] = str(i['_id'])
    lista.append(i)
  return lista


@app.route('/banco',methods=['GET','POST'])
def banco():
  data = {}
  if request.method == 'POST':
    try:
      banco = {}
      banco['nombre'] = request.form['nombre']
      banco['pais'] = request.form['pais']
      banco['tasaInteres'] = float(request.form['tasaInteres'])
      bd.bancos.insert_one(banco)
      data['mensaje'] = 'Banco agregado'
      data['color'] = 'success'
    except:
      data['mensaje'] = 'Ocurrio un error'
      data['danger'] = 'success'
  data['bancos'] = cargarBancos()
  return render_template('banco.html',data=data)

@app.route('/banco/eliminar/<id>',methods=['GET'])
def bancoEliminar(id):
  bd.bancos.delete_one({'_id':ObjectId(id)})
  return redirect('/banco')

def cargarBancos():
  lista = []
  for i in bd.bancos.find():
    i['_id'] = str(i['_id'])
    lista.append(i)
  return lista

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=5000, debug=True)