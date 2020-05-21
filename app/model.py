from app import db
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
