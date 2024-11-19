from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from Busquedas import ejecutar_busquedas
import os

app = Flask(__name__, static_folder='web')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/algorithms', methods=['POST'])
def run_algorithm():
    data = request.json
    mapa = data['Mapa']
    meta = data['Meta']
    inicio = data['Inicio']
    maximo_iteraciones = data['MaximoIteraciones']

    check = ejecutar_busquedas(mapa, meta, inicio, maximo_iteraciones)

    return jsonify(check)

if __name__ == '__main__':
    app.run(debug=True, port=5001)