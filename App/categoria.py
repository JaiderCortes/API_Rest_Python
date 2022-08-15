from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bdpythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Creacion de Tabla Cateegoria
class categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(200))

    def __init__(self, cat_nom, cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp

db.create_all()

#Esquema Categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desp')

#Una sola respuesta
categoria_schema = CategoriaSchema()

#Muchas respuestas
categorias_schema = CategoriaSchema(many = True)

#####GET#####
@app.route('/categoria', methods = ['GET'])
def getCategorias():
    all_categorias = categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

#####GET por Id#####
@app.route('/categoria/<id>', methods = ['GET'])
def getCategoriasPorId(id):
    categoriaId = categoria.query.get(id)
    return categoria_schema.jsonify(categoriaId)

#####POST#####
@app.route('/categoria', methods = ['POST'])
def insertCategoria():
    data = request.get_json(force = True)
    cat_nom = data['cat_nom']
    cat_desp = data['cat_desp']
    nuevoRegistro = categoria(cat_nom, cat_desp)
    db.session.add(nuevoRegistro)
    db.session.commit()
    return categoria_schema.jsonify(nuevoRegistro)

#####PUT#####
@app.route('/categoria/<id>', methods = ['PUT'])
def updateCategoria(id):
    updateCat = categoria.query.get(id)
    cat_nom = request.json['cat_nom']
    cat_desp = request.json['cat_desp']

    updateCat.cat_nom = cat_nom
    updateCat.cat_desp = cat_desp

    db.session.commit()
    return categoria_schema.jsonify(updateCat)

#####DELETE#####
@app.route('/categoria/<id>', methods = ['DELETE'])
def deleteCategoria(id):
    deleteCat = categoria.query.get(id)
    db.session.delete(deleteCat)
    db.session.commit()
    return categoria_schema.jsonify(deleteCat)

#Mensaje de bienvenida por método GET
@app.route('/', methods = ['GET'])
def index():
    return jsonify({'Mensaje':'API Rest con Python'})

if __name__ == '__main__':
    app.run(debug = True)