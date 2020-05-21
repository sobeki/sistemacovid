from flask import jsonify,render_template
from app import app
from app.snipets import *

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