import datetime
from flask import Flask,jsonify,render_template
from sqlalchemy.sql import func, and_
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/coronavirus'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)

pais_casos = db.Table('pais_casos',
    db.Column('pais_id', db.Integer, db.ForeignKey('pais._id')),
    db.Column('casos_id', db.Integer, db.ForeignKey('casos._id'))
)
pais_recuperados = db.Table('pais_recuperados',
    db.Column('pais_id', db.Integer, db.ForeignKey('pais._id')),
    db.Column('recuperados_id', db.Integer, db.ForeignKey('recuperados._id'))
)
pais_mortes = db.Table('pais_mortes',
    db.Column('pais_id', db.Integer, db.ForeignKey('pais._id')),
    db.Column('mortes_id', db.Integer, db.ForeignKey('mortes._id'))
)
class Pais(db.Model):
    _id = db.Column( db.Integer, primary_key=True)
    nome_pais = db.Column( db.String(100),nullable=False, unique=True)
    pais_caso_relationship = db.relationship('Casos', secondary=pais_casos, backref=db.backref('paisCasos',lazy='dynamic'))
    pais_recuperados_relationship = db.relationship('Recuperados', secondary=pais_recuperados, backref=db.backref('paisRecuperados',lazy='dynamic'))
    pais_mortes_relationship = db.relationship('Mortes', secondary=pais_mortes, backref=db.backref('paisMortes',lazy='dynamic'))
    def __init__(self,nome_pais):
        self.nome_pais = nome_pais

class Casos(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer(),nullable=False)
    data = db.Column( db.DateTime(100),nullable=False )
    
    def __init__(self,quantidade,data):
        self.quantidade = quantidade
        self.data = data

class Mortes(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer(),nullable=False)
    data = db.Column( db.DateTime(100),nullable=False )
    def __init__(self,quantidade,data):
        self.quantidade = quantidade
        self.data = data

class Recuperados(db.Model):
    _id = db.Column( db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer(),nullable=False)
    data = db.Column( db.DateTime(100),nullable=False )
    def __init__(self,quantidade,data):
        self.quantidade = quantidade
        self.data = data

def queryTypeChecker(_type):
    obj = {}
    if 'casos' in _type:
        obj = {
            'Class': Casos, 
            'pais_relationship': 'pais_caso_relationship'
            }
    if 'recuperados' in _type:
        obj = {
            'Class': Recuperados,
            'pais_relationship': 'pais_recuperados_relationship'
            }
    if 'mortes' in _type:
        obj = {
            'Class': Mortes,
            'pais_relationship': 'pais_mortes_relationship'
            }
            
    return obj or False

def as_dict(Class):
       return {Class.name: getattr(Class, Class.name) for c in Class.__table__.columns}

def getQueryTotalWorld(_type):
    queryType = queryTypeChecker(_type)
    q = Pais.query.all()
    nome_paises = []
    totalQuantity = 0
    for pais in q:
        nome_pais = pais.nome_pais
        nome_paises.append(nome_pais)
        quantidadeByPaisByType = queryType['Class'].query.filter(Pais.nome_pais==nome_pais).join(getattr(Pais,queryType['pais_relationship'])).order_by(queryType['Class'].quantidade.desc()).first()
        if quantidadeByPaisByType is None:
            continue
        totalQuantity = quantidadeByPaisByType.quantidade + totalQuantity
    
    return {
        'countries': nome_paises, 
        'totalQuantity': totalQuantity
        }

def getQueryQuantidadeTotalByPais(nome_pais, _type):
    try:
        queryType = queryTypeChecker(_type)
        quantidadeByPaisByType = queryType['Class'].query.filter(Pais.nome_pais==nome_pais).join(getattr(Pais,queryType['pais_relationship'])).order_by(queryType['Class'].quantidade.desc()).first().quantidade
        return {
            'country': nome_pais,
            'totalQuantity': quantidadeByPaisByType
        }
    except Exception as e:
        return False
def getQueryByDataAndPais(data, nome_pais, _type):
    queryType = queryTypeChecker(_type)
    type_in_pais = Pais.query.filter_by(nome_pais=nome_pais).join(getattr(Pais,queryType['pais_relationship'])).filter_by(data=data).first()
    if type_in_pais:
        return type_in_pais
        
    return False

def insert_query(data, quantidade, nome_pais, _type):

    insert_obj_type = queryTypeChecker(_type)
    query_pais = Pais.query.filter_by(nome_pais=nome_pais).first()
    if not query_pais:
        pais = Pais(nome_pais=nome_pais)
        db.session.add(pais)
        query_pais = pais

    resultByType = getQueryByDataAndPais(data, query_pais.nome_pais, _type )
 
    if not resultByType:
        newRegisterAtTable = insert_obj_type['Class'](data=data, quantidade=quantidade) #novo obj da tabela, depende do tipo q foi pedido
        method_call = getattr(query_pais, insert_obj_type['pais_relationship']) #dinamicamente escolher metodo para chamar       
        method_call.append(newRegisterAtTable) #inserir nova relacao de tabela pais_X
        db.session.add(newRegisterAtTable) #inserir novo registro de acordo com tipo de tabela
        db.session.commit()
    else:
       
        method_call = getattr(resultByType, insert_obj_type['pais_relationship']) #dinamicamente escolher metodo para chamar       
        method_call[0].quantidade = quantidade #inserir nova relacao de tabela pais_X
        db.session.commit()

    db.session.commit()



@app.route('/cases', methods=['GET'])
def all_cases():
    cases = getQueryTotalWorld('casos')
    return jsonify(cases)

@app.route('/cases/<country>', methods=['GET'])
def all_cases_country(country):
    cases = getQueryQuantidadeTotalByPais(country, 'casos')
    if cases:
        return jsonify(cases)
    return jsonify({"error":"400"})

@app.route('/recovered', methods=['GET'])
def all_recovered():
    recovered = getQueryTotalWorld('recuperados')
    return jsonify(recovered)

@app.route('/recovered/<country>', methods=['GET'])
def all_recovered_country(country):
    recovered = getQueryQuantidadeTotalByPais(country, 'recuperados')
    if recovered:
        return jsonify(recovered)
    return jsonify({"error":"400"})

@app.route('/deaths', methods=['GET'])
def all_deaths():
    deaths = getQueryTotalWorld('mortes')
    return jsonify(deaths)

@app.route('/deaths/<country>', methods=['GET'])
def all_deaths_country(country):
    deaths = getQueryQuantidadeTotalByPais(country, 'mortes')
    if deaths:
        return jsonify(deaths)
    return jsonify({"error":"400"})

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=4555)
