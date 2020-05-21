from datetime import datetime
from app.model import Casos,Recuperados,Mortes,Pais
from app import db

def queryTypeChecker(_type):
    obj = {}
    if ('casos' in _type) or ('cases' in _type):
        obj = {
            'Class': Casos, 
            'pais_relationship': 'pais_caso_relationship'
            }
    if ('recuperados' in _type) or ('recovered' in _type):
        obj = {
            'Class': Recuperados,
            'pais_relationship': 'pais_recuperados_relationship'
            }
    if ('mortes'in _type) or ('deaths' in _type):
        obj = {
            'Class': Mortes,
            'pais_relationship': 'pais_mortes_relationship'
            }
    print (obj)
    return obj or False



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
        print (queryType)
        quantidadeByPaisByType = queryType['Class'].query.filter(Pais.nome_pais==nome_pais).join(getattr(Pais,queryType['pais_relationship'])).order_by(queryType['Class'].quantidade.desc()).first().quantidade
        print (quantidadeByPaisByType)
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
def getQueryByDataAndPaisRoute(data, nome_pais, _type):
    try:
        queryType = queryTypeChecker(_type)
        search_created = datetime.strptime(data, '%m-%d-%y')
        print (queryType)
        type_in_pais = queryType['Class'].query.filter(Pais.nome_pais==nome_pais).join(getattr(Pais,queryType['pais_relationship'])).filter_by(data=search_created).first()
        
        
        if type_in_pais:
            
            return {
                'country': nome_pais,
                'data':search_created,
                'count':type_in_pais.quantidade
                }
    except Exception as e: 
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

